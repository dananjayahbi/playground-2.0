import React, { useEffect, useState } from "react";
import { message, Modal, Input, Button } from "antd";
import ImageGallery from "./ImageGallery";
import api from "../services/api";

const Drafts = () => {
  const [posts, setPosts] = useState([]);
  const [caption, setCaption] = useState("");
  const [currentPost, setCurrentPost] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  useEffect(() => {
    fetchDrafts();
  }, []);

  const fetchDrafts = async () => {
    try {
      const data = await api.getDrafts();
      setPosts(data);
    } catch (error) {
      message.error("Error fetching drafts.");
    }
  };

  const handleSync = async () => {
    try {
      const response = await api.syncDrafts();
      message.success(response.message);
      fetchDrafts(); // Refresh drafts after syncing
    } catch (error) {
      message.error("Error syncing drafts.");
    }
  };

  const handleAccept = (post) => {
    setCurrentPost(post);
    setModalVisible(true);
  };

  const handleReject = async (post) => {
    try {
      await api.rejectPost(post.fileName);
      message.success("Post rejected.");
      setPosts(posts.filter((p) => p.id !== post.id));
    } catch (error) {
      message.error("Error rejecting post.");
    }
  };

  const handleCaptionSubmit = async () => {
    try {
      await api.acceptPost(currentPost.fileName, caption);
      message.success("Post accepted.");
      setPosts(posts.filter((p) => p.id !== currentPost.id));
      setModalVisible(false);
      setCaption("");
    } catch (error) {
      message.error("Error accepting post.");
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 16, textAlign: "right" }}>
        <Button type="primary" onClick={handleSync}>
          Sync
        </Button>
      </div>
      <ImageGallery
        posts={posts}
        actions={[
          { label: "Accept", type: "primary", onClick: handleAccept },
          { label: "Reject", type: "danger", onClick: handleReject },
        ]}
      />
      <Modal
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={handleCaptionSubmit}
        title="Enter Caption"
      >
        <Input
          placeholder="Enter a caption for the post"
          value={caption}
          onChange={(e) => setCaption(e.target.value)}
        />
      </Modal>
    </div>
  );
};

export default Drafts;
