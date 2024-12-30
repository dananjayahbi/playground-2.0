import React, { useState, useEffect } from "react";
import { Tabs } from "antd";
import Drafts from "../components/Drafts";
import ToBePublished from "../components/ToBePublished";
import Published from "../components/Published";

const { TabPane } = Tabs;

const Dashboard = () => {
  return (
    <Tabs defaultActiveKey="1">
      <TabPane tab="Drafts" key="1">
        <Drafts />
      </TabPane>
      <TabPane tab="To Be Published" key="2">
        <ToBePublished />
      </TabPane>
      <TabPane tab="Published" key="3">
        <Published />
      </TabPane>
    </Tabs>
  );
};

export default Dashboard;
