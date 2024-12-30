import React, { useState } from "react";
import { Card, Image, Button, Empty } from "antd";
import { splitIntoColumns } from "../utils/columnize";

const ImageGallery = ({ posts, actions }) => {
  const [previewVisible, setPreviewVisible] = useState(false);
  const [previewImage, setPreviewImage] = useState("");

  const columns = splitIntoColumns(posts);

  const handlePreview = (src) => {
    setPreviewImage(src);
    setPreviewVisible(true);
  };

  if (posts.length === 0) {
    return (
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <Empty description="No Posts Available" />
      </div>
    );
  }

  return (
    <div style={{ display: "flex", gap: "16px" }}>
      {columns.map((column, colIndex) => (
        <div key={colIndex} style={{ flex: 1 }}>
          {column.map((post) => (
            <Card
              key={post.id}
              hoverable
              cover={
                <img
                  alt="post"
                  src={post.path}
                  onClick={() => handlePreview(post.path)}
                  style={{ cursor: "pointer", width: "100%" }}
                />
              }
              style={{ marginBottom: 16 }}
            >
              <div style={{ textAlign: "center" }}>
                {actions &&
                  actions.map((action, index) => (
                    <Button
                      key={index}
                      type={action.type}
                      onClick={() => action.onClick(post)}
                      style={{ marginBottom: 8 }}
                    >
                      {action.label}
                    </Button>
                  ))}
              </div>
            </Card>
          ))}
        </div>
      ))}
      <Image
        preview={{ visible: previewVisible, src: previewImage }}
        onPreviewClose={() => setPreviewVisible(false)}
        style={{ display: "none" }}
      />
    </div>
  );
};

export default ImageGallery;
