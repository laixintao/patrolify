import { Spinner } from "@blueprintjs/core";
import axios from "axios";
import moment from "moment";
import React from "react";
import { Link, useParams } from "react-router-dom";
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
  const latestChecks = detailInfo;

  return (
    <>
      <div className="list-content">
        {Object.keys(latestChecks)
          .sort()
          .reverse()
          .map((cid, index) => (
            <CheckItem
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
    </>
  );
}

const CheckItem = ({ cid, index, checkDetail }) => {
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
