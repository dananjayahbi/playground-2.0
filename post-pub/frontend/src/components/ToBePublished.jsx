import React, { useEffect, useState } from "react";
import { message } from "antd";
import ImageGallery from "./ImageGallery";
import api from "../services/api";

const ToBePublished = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchToBePublishedPosts = async () => {
      try {
        const data = await api.getToBePublishedPosts();
        setPosts(data);
      } catch (error) {
        message.error("Error fetching to-be-published posts.");
      }
    };

    fetchToBePublishedPosts();
  }, []);

  const handlePublish = async (post) => {
    try {
      await api.publishPost(post.id);
      message.success("Post published successfully.");
      setPosts(posts.filter((p) => p.id !== post.id));
    } catch (error) {
      message.error("Error publishing post.");
    }
  };

  const handleDelete = async (post) => {
    try {
      await api.deleteToBePublishedPost(post.id);
      message.success("Post deleted.");
      setPosts(posts.filter((p) => p.id !== post.id));
    } catch (error) {
      message.error("Error deleting post.");
    }
  };

  return (
    <ImageGallery
      posts={posts}
      actions={[
        { label: "Publish", type: "primary", onClick: handlePublish },
        { label: "Delete", type: "danger", onClick: handleDelete },
      ]}
    />
  );
};

export default ToBePublished;
