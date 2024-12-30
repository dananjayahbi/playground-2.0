const express = require("express");
const fs = require("fs-extra");
const path = require("path");
const { v4: uuidv4 } = require("uuid");
const bodyParser = require("body-parser");
const axios = require("axios");
const cors = require("cors");

const app = express();
const PORT = 3000;
app.use(cors());

// Folders
const POSTS_DIR = path.join(__dirname, "posts-management");
const DRAFTS_DIR = path.join(POSTS_DIR, "drafts");
const TO_BE_PUBLISHED_DIR = path.join(POSTS_DIR, "to-be-published");
const PUBLISHED_DIR = path.join(POSTS_DIR, "published");
const DATA_FILE = path.join(__dirname, "data/posts.json");
const POSTS_FOLDER = path.join(__dirname, "../posts"); // Path to "posts" folder

// Serve the posts-management folder as static
app.use("/images", express.static(POSTS_DIR));

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
    const defaultData = { drafts: [], toBePublished: [], published: [] };
    savePostsData(defaultData);
    return defaultData;
  }
};
const savePostsData = (data) => fs.writeJsonSync(DATA_FILE, data);

// Sync posts from "../posts" to drafts
app.post("/sync-drafts", (req, res) => {
  fs.readdir(POSTS_FOLDER, (err, files) => {
    if (err) return res.status(500).send("Error reading posts folder.");

    if (files.length === 0) {
      return res.status(200).send({ message: "All synced" });
    }

    files.forEach((file) => {
      const filePath = path.join(POSTS_FOLDER, file);
      const draftPath = path.join(DRAFTS_DIR, file);
      fs.moveSync(filePath, draftPath, { overwrite: true });
    });

    res.status(200).send({ message: "Drafts synced successfully." });
  });
});

// Get drafts
app.get("/drafts", (req, res) => {
  const drafts = fs.readdirSync(DRAFTS_DIR).map((file) => ({
    id: uuidv4(),
    fileName: file,
    path: `http://localhost:${PORT}/images/drafts/${file}`,
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
  const imageUrl = `http://localhost:${PORT}/images/drafts/${fileName}`;
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

// Get to-be-published posts
app.get("/to-be-published", (req, res) => {
  const data = getPostsData();
  const toBePublished = data.toBePublished.map((post) => ({
    ...post,
    path: `http://localhost:${PORT}/images/to-be-published/${post.fileName}`,
  }));
  res.json(toBePublished);
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
      imageUrl: `http://localhost:${PORT}/images/published/${post.fileName}`,
      publishedAt: new Date().toISOString(),
    });

    savePostsData(data);
    res.send("Post published successfully.");
  } catch (error) {
    res.status(500).send("Error publishing post.");
  }
});

// Get published posts
app.get("/published", (req, res) => {
  const data = getPostsData();
  res.json(data.published);
});

// Delete a to-be-published post
app.delete("/to-be-published/:id", (req, res) => {
  const { id } = req.params;
  const data = getPostsData();
  const postIndex = data.toBePublished.findIndex((post) => post.id === id);

  if (postIndex === -1) return res.status(404).send("Post not found.");

  const post = data.toBePublished[postIndex];
  const toBePublishedPath = path.join(TO_BE_PUBLISHED_DIR, post.fileName);

  fs.removeSync(toBePublishedPath);

  data.toBePublished.splice(postIndex, 1);
  savePostsData(data);

  res.send("Post deleted successfully.");
});

// Start Server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
