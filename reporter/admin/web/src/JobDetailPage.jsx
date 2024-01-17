import { Spinner } from "@blueprintjs/core";
import axios from "axios";
import React from "react";
import { Link, useParams } from "react-router-dom";
import "./JobDetailPage.css";


export default function JobDetailPage() {

  let { checkerName, checkId, jobId } = useParams();

  const [data, setData] = React.useState({});
  const [loadingDetail, setLoadingDetail] = React.useState(true);

  React.useEffect(() => {
    axios.get(`/api/v1/checker/${checkerName}/${checkId}/${jobId}`).then((resp) => {
      const { data } = resp;
      setData(data);
      setLoadingDetail(false);
    });
  }, [jobId]);

  if (loadingDetail) {
    return <Spinner />;
  }

  return <div className="list-content">
    <p>
      <span className="span-table-key">check target: </span>
      <span className="span-table-value">{data.target.toString()}</span>
    </p>
    <p>
      <span className="span-table-key">reason: </span>
      <pre className="span-table-block">{data.reason.toString()}</pre>
    </p>
    <p>
      <span className="span-table-key">Job ID: </span>
      <span className="span-table-value">{data.job_id.toString()}</span>
      {"  "}
      <span className="span-table-value" style={{ "color": "grey" }}>(parent job:

        <Link to={`/checker/${checkerName}/job/${checkId}/${data.parent_target_id}`}>
          {data.parent_target_id}
        </Link>)
      </span>
    </p>
    <p>
      <span className="span-table-key">passed: </span>
      <span className="span-table-value">{data.check_pass.toString()}</span>
    </p>
    <p>
      <span className="span-table-key">run success(without any exceptions): </span>
      <span className="span-table-value">{data.run_success.toString()}</span>
    </p>

  </div>;
}
