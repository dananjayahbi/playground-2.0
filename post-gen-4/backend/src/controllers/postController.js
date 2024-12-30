const fs = require("fs-extra");
const sharp = require("sharp");
const path = require("path");
const uuid = require("uuid");
const multer = require("multer");

const settingsPath = path.join(__dirname, "../../settings.json");
const uploadsDir = path.join(__dirname, "../uploads");
const postsDir = path.join(__dirname, "../../posts");

// Multer setup for image uploads
const storage = multer.diskStorage({
    destination: uploadsDir,
    filename: (req, file, cb) => {
        cb(null, `${uuid.v4()}-${file.originalname}`);
    },
});

const upload = multer({ storage });

// Ensure directories exist
fs.ensureDirSync(uploadsDir);
fs.ensureDirSync(postsDir);

// Upload Image
const uploadImage = (req, res) => {
    upload.single("image")(req, res, (err) => {
        if (err) {
            return res.status(400).json({ message: "Image upload failed", error: err.message });
        }
        res.json({ message: "Image uploaded successfully", filePath: req.file.path });
    });
};

// Get Default Settings
const getDefaultSettings = (req, res) => {
    if (!fs.existsSync(settingsPath)) {
        const defaultSettings = {
            backgroundImage: "",
            fbWidth: 1080,
            fbHeight: 1350,
            quoteText: "Default Quote",
            signatureText: "Your Name",
            quoteColor: "#000000",
            signatureColor: "#000000",
            backgroundBlur: 5,
        };
        fs.writeJsonSync(settingsPath, defaultSettings);
    }
    const settings = fs.readJsonSync(settingsPath);
    res.json(settings);
};

// Update Default Settings
const updateDefaultSettings = (req, res) => {
    const newSettings = req.body;
    fs.writeJsonSync(settingsPath, newSettings);
    res.json({ message: "Settings updated successfully" });
};

// Generate Post
const generatePost = async (req, res) => {
    try {
        const {
            backgroundImage,
            fbWidth,
            fbHeight,
            quoteText,
            signatureText,
            quoteColor,
            signatureColor,
            backgroundBlur,
        } = req.body;

        const outputFilePath = path.join(postsDir, `post-${uuid.v4()}.jpg`);

        const image = sharp(backgroundImage || path.join(__dirname, "../../default_background.png"))
            .resize(fbWidth, fbHeight)
            .blur(backgroundBlur);

        const svgOverlay = `
            <svg width="${fbWidth}" height="${fbHeight}">
                <text x="50%" y="30%" fill="${quoteColor}" font-size="40" text-anchor="middle">${quoteText}</text>
                <text x="50%" y="90%" fill="${signatureColor}" font-size="20" text-anchor="middle">${signatureText}</text>
            </svg>
        `;

        await image
            .composite([{ input: Buffer.from(svgOverlay), top: 0, left: 0 }])
            .toFile(outputFilePath);

        res.json({ message: "Post generated successfully", filePath: outputFilePath });
    } catch (error) {
        res.status(500).json({ message: "Failed to generate post", error: error.message });
    }
};

module.exports = {
    uploadImage,
    getDefaultSettings,
    updateDefaultSettings,
    generatePost,
};
