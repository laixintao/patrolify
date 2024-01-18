import { Card, H4 } from "@blueprintjs/core";
import { useParams } from "react-router-dom";

import { Outlet, Link } from "react-router-dom";

export default function CheckerLayout() {
  let { checkerName } = useParams();

  return (
    <div className="body-detail">
      <Link to={`/checker/${checkerName}`}>
        <H4>{checkerName}</H4>
      </Link>
      <Card className="job-table-list">
        <Outlet />
      </Card>
    </div>
  );
}
