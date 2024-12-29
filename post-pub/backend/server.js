const express = require("express");
const fs = require("fs-extra");
const path = require("path");
const { v4: uuidv4 } = require("uuid");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
const PORT = 3000;

// Folders
const POSTS_DIR = path.join(__dirname, "posts-management");
const DRAFTS_DIR = path.join(POSTS_DIR, "drafts");
const TO_BE_PUBLISHED_DIR = path.join(POSTS_DIR, "to-be-published");
const PUBLISHED_DIR = path.join(POSTS_DIR, "published");
const DATA_FILE = path.join(__dirname, "data/posts.json");

// Middleware
app.use(bodyParser.json());

// Ensure folders exist
fs.ensureDirSync(DRAFTS_DIR);
fs.ensureDirSync(TO_BE_PUBLISHED_DIR);
fs.ensureDirSync(PUBLISHED_DIR);
fs.ensureFileSync(DATA_FILE);

// Initialize JSON data file
if (!fs.existsSync(DATA_FILE)) {
  fs.writeJsonSync(DATA_FILE, { drafts: [], toBePublished: [], published: [] });
}

// Utility Functions
const getPostsData = () => {
  try {
    return fs.readJsonSync(DATA_FILE);
  } catch (err) {
    // If the file is empty or malformed, initialize it
    const defaultData = { drafts: [], toBePublished: [], published: [] };
    savePostsData(defaultData);
    return defaultData;
  }
};
const savePostsData = (data) => fs.writeJsonSync(DATA_FILE, data);

// Move posts from 'posts' folder to 'drafts'
app.get("/initialize-drafts", (req, res) => {
  const postsFolder = path.join(__dirname, "../posts");
  fs.readdir(postsFolder, (err, files) => {
    if (err) return res.status(500).send("Error reading posts folder.");

    files.forEach((file) => {
      const filePath = path.join(postsFolder, file);
      const draftPath = path.join(DRAFTS_DIR, file);
      fs.move(filePath, draftPath, { overwrite: true });
    });
    res.send("Posts moved to drafts.");
  });
});

// Get drafts
app.get("/drafts", (req, res) => {
  const drafts = fs.readdirSync(DRAFTS_DIR).map((file) => ({
    id: uuidv4(),
    fileName: file,
    path: path.join(DRAFTS_DIR, file),
  }));
  res.json(drafts);
});

// Accept a post (move to to-be-published)
app.post("/accept-post", (req, res) => {
  const { fileName, caption } = req.body;
  const draftPath = path.join(DRAFTS_DIR, fileName);
  const publishPath = path.join(TO_BE_PUBLISHED_DIR, fileName);

  if (!fs.existsSync(draftPath))
    return res.status(404).send("Draft not found.");

  const postId = uuidv4();
  const imageUrl = `http://localhost:${PORT}/images/${fileName}`;
  const publishUrl = `https://graph.facebook.com/v21.0/{page_id}/photos?url=${imageUrl}&caption=${caption}&access_token={access_token}`;

  fs.moveSync(draftPath, publishPath, { overwrite: true });

  const data = getPostsData();
  data.toBePublished.push({ id: postId, fileName, caption, publishUrl });
  savePostsData(data);

  res.json({ id: postId, message: "Post accepted." });
});

// Reject a post (delete from drafts)
app.post("/reject-post", (req, res) => {
  const { fileName } = req.body;
  const draftPath = path.join(DRAFTS_DIR, fileName);

  if (!fs.existsSync(draftPath))
    return res.status(404).send("Draft not found.");

  fs.removeSync(draftPath);
  res.send("Post rejected and deleted.");
});

// Publish a post
app.post("/publish-post", async (req, res) => {
  const { id } = req.body;
  const data = getPostsData();
  const postIndex = data.toBePublished.findIndex((post) => post.id === id);

  if (postIndex === -1) return res.status(404).send("Post not found.");

  const post = data.toBePublished[postIndex];
  try {
    const response = await axios.post(post.publishUrl);
    const publishedPath = path.join(PUBLISHED_DIR, post.fileName);
    const toBePublishedPath = path.join(TO_BE_PUBLISHED_DIR, post.fileName);

    fs.moveSync(toBePublishedPath, publishedPath, { overwrite: true });

    data.toBePublished.splice(postIndex, 1);
    data.published.push({
      ...post,
      facebookPostId: response.data.id,
      publishedAt: new Date().toISOString(),
    });

    savePostsData(data);
    res.send("Post published successfully.");
  } catch (error) {
    res.status(500).send("Error publishing post.");
  }
});

// Serve images
app.use("/images", express.static(DRAFTS_DIR));
app.use("/images", express.static(TO_BE_PUBLISHED_DIR));
app.use("/images", express.static(PUBLISHED_DIR));

// Start Server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
