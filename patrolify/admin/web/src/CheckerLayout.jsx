import { Button, Card, H4 } from "@blueprintjs/core";
import axios from "axios";
import React from "react";
import { useParams } from "react-router-dom";
import "./CheckerLayout.css";

import { Outlet, Link } from "react-router-dom";

export default function CheckerLayout() {
  let { checkerName } = useParams();

  const [message, setMessage] = React.useState("");

  const triggerCheckerNow = () => {
    axios.post(`/api/v1/checker/${checkerName}/enqueue`).then(resp => {
      const { data } = resp;
      console.log("trigger response: ", data);
      setMessage("This Checker has been triggered, now in queue, waiting to be executed...");
    }
    )
  }

  return (
    <div className="body-detail">
      <Link to={`/checker/${checkerName}`}>
        <H4>{checkerName}</H4>
      </Link>

      <Button onClick={triggerCheckerNow} intent="primary">Run this Checker Now!</Button>
      <div className="message">{message}</div>
      <Card className="job-table-list">
        <Outlet />
      </Card>
    </div>
  );
}
