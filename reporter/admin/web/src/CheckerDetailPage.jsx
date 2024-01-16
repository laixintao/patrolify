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
  const latestChecks = data;

  return (
    <Card className="job-table-list">
      <H4>{name}</H4>
      <Divider style={{ margin: 0 }} />

      <div className="job-history-list">
        {Object.keys(latestChecks)
          .sort()
          .reverse()
          .map((cid, index) => (
            <JobItem
              cid={cid}
              index={index}
              key={cid}
              checkDetail={latestChecks[cid]}
            />
          ))}
      </div>
      <p className="hint">
        (Displayed time is the local time of your browser.)
      </p>
    </Card>
  );
};

const JobItem = ({ cid, index, checkDetail }) => {
  return (
    <div key={cid} className="job-link">
      <span> ({index}).</span>
      <Link to={`job/${cid}`}>
        {moment.unix(cid).format("YYYY-MM-DD HH:mm z")}
      </Link>
      <span className="job-item-success">
        {checkDetail.all_passed && "success"}
      </span>
      <span className="job-item-fail">{!checkDetail.all_passed && "fail"}</span>
      <span>{index == 0 && "  (latest)"}</span>
    </div>
  );
};
