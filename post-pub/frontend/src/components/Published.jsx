import React, { useEffect, useState } from "react";
import { message } from "antd";
import ImageGallery from "./ImageGallery";
import api from "../services/api";

const Published = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPublishedPosts = async () => {
      try {
        const data = await api.getPublishedPosts();
        setPosts(data);
      } catch (error) {
        message.error("Error fetching published posts.");
      }
    };

    fetchPublishedPosts();
  }, []);

  return <ImageGallery posts={posts} />;
};

export default Published;
