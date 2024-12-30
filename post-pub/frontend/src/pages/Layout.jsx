import React from "react";
import { Layout, Menu } from "antd";
import { Link } from "react-router-dom";

const { Header, Content, Footer } = Layout;

const AppLayout = ({ children }) => {
  return (
    <Layout>
      <Header>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={["1"]}>
          <Menu.Item key="1">
            <Link to="/">Dashboard</Link>
          </Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: "20px" }}>{children}</Content>
      <Footer style={{ textAlign: "center" }}>Post Manager ©2024</Footer>
    </Layout>
  );
};

export default AppLayout;
