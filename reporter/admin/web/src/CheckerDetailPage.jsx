import { Divider, H4, Card, Spinner } from "@blueprintjs/core";
import axios from "axios";
import React from "react";
import { useParams } from "react-router-dom";
import moment from "moment";
import { Link } from "react-router-dom";
import "./CheckerDetailPage.css";

export default function CheckerDetailPage() {
  let { checkerName } = useParams();

  const [detailInfo, setDetailInfo] = React.useState({});
  const [loadingDetail, setLoadingDetail] = React.useState(true);

  React.useEffect(() => {
    axios.get(`/api/v1/checker/${checkerName}`).then((resp) => {
      const { data } = resp;
      setDetailInfo(data);
      setLoadingDetail(false);
    });
  }, []);

  if (loadingDetail) {
    return <Spinner />;
  }
  return (
    <div className="main-body">
      <CheckerDetail data={detailInfo} name={checkerName} />
    </div>
  );
}

const CheckerDetail = ({ data, name }) => {
  const { latest_check_ids: latestChecks } = data;
  const reversedChecks = [...latestChecks].reverse();
  return (
    <Card className="job-table-list">
      <H4>{name}</H4>
      <Divider style={{ margin: 0 }} />

      <p className="hint">(Displayed time is the local time of your browser.)</p>

      <div className="job-history-list">
        {reversedChecks.map((cid, index) => (
          <div key={cid} className="job-link">
            <span> ({index}).</span>
            <Link to={`job/${cid}`}>
              {moment.unix(cid).format("YYYY-MM-DD HH:mm z")}
            </Link>
          </div>
        ))}
      </div>
    </Card>
  );
};
