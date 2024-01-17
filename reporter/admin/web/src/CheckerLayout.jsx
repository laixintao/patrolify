import { Card, H4 } from "@blueprintjs/core";
import { useParams } from "react-router-dom";

import { Outlet } from "react-router-dom";

export default function CheckerLayout() {
  let { checkerName } = useParams();

  return (
    <div className="main-body">
      <H4>{checkerName}</H4>
      <Card className="job-table-list">
        <Outlet />
      </Card>
    </div>
  );
}
