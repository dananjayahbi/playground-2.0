import React from "react";
import { Card, Button } from "antd";

const PostCard = ({ post, onAccept, onReject }) => {
  return (
    <Card
      hoverable
      cover={<img alt="post" src={post.path} />}
      style={{ marginBottom: 16 }}
    >
      <Button type="primary" onClick={onAccept} style={{ marginRight: 8 }}>
        Accept
      </Button>
      <Button type="danger" onClick={onReject}>
        Reject
      </Button>
    </Card>
  );
};

export default PostCard;
