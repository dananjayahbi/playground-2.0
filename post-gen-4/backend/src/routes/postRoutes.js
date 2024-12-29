const express = require("express");
const router = express.Router();
const {
    uploadImage,
    getDefaultSettings,
    updateDefaultSettings,
    generatePost,
} = require("../controllers/postController");

// Routes
router.post("/upload", uploadImage);
router.get("/settings", getDefaultSettings);
router.post("/settings", updateDefaultSettings);
router.post("/generate", generatePost);

module.exports = router;
