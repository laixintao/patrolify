import { Button, Card, H4 } from "@blueprintjs/core";
import axios from "axios";
import { useParams } from "react-router-dom";

import { Outlet, Link } from "react-router-dom";

export default function CheckerLayout() {
  let { checkerName } = useParams();

  const triggerCheckerNow = () => {
    axios.post(`/api/v1/checker/${checkerName}/enqueue`).then(resp => {
      const { data } = resp;
      console.log("trigger response: ", data);
    }
    )
  }

  return (
    <div className="body-detail">
      <Link to={`/checker/${checkerName}`}>
        <H4>{checkerName}</H4>
      </Link>

      <Button onClick={triggerCheckerNow} intent="primary">Run this Checker Now!</Button>
      <Card className="job-table-list">
        <Outlet />
      </Card>
    </div>
  );
}
