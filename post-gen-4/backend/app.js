const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const fs = require("fs-extra");

const app = express();

app.use(bodyParser.json());
app.use(cors());

// Routes
const postRoutes = require("./src/routes/postRoutes");
app.use("/api/posts", postRoutes);

const PORT = 5000;

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
