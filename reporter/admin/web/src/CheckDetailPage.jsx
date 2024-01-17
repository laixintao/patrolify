import { Divider, H5, Spinner } from "@blueprintjs/core";
import moment from "moment";
import React from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";


export default function CheckDetailPage() {
  let { checkId, checkerName } = useParams();

  const [checkResult, setCheckResult] = React.useState({});
  const [loadingDetail, setLoadingDetail] = React.useState(true);

  React.useEffect(() => {
    axios.get(`/api/v1/checker/${checkerName}/${checkId}`).then((resp) => {
      const { data } = resp;
      setCheckResult(data);
      setLoadingDetail(false);
    });
  }, []);

  if (loadingDetail) {
    return <Spinner />;
  }

  return <div>
    <H5>
      Job running at {" "}
      {moment.unix(checkId).format("YYYY-MM-DD HH:mm z")}
    </H5>

    <div className="list-content">
      {checkResult.passed.length} passed, {checkResult.not_passed.length} not passed, {checkResult.failed.length} failed to run the check job.
    </div>

    <Divider />

    <div className="list-content">
      <H5>== Success List ==</H5>
      <div>
        {checkResult.passed.map((item, index) => <CheckItem key={index} jobid={item} index={index} result="passed" name={checkResult.job_info[item].target} />)}
      </div>

      {checkResult.passed.length === 0 && <div>No content under this status</div>}
    </div>

    <Divider />
    <div className="list-content">
      <H5>== Not Pass ==</H5>
      <div>
        {checkResult.not_passed.map((item, index) => <CheckItem key={index} jobid={item} index={index} result="not pass" name={checkResult.job_info[item].target} />)}
      </div>
      {checkResult.not_passed.length === 0 && <div>No content under this status</div>}
    </div>

    <Divider />
    <div className="list-content">
      <H5>== Check Failed ==</H5>
      <div>
        {checkResult.failed.map((item, index) => <CheckItem key={index} jobid={item} index={index} result="failed" name={checkResult.job_info[item].target} />)}
      </div>
      {checkResult.failed.length === 0 && <div>No content under this status</div>}
    </div>
  </div>;
}

const CheckItem = ({ jobid, index, result, name }) => {
  return (
    <div key={jobid} className="job-link">
      <span> ({index}).</span>
      <Link to={`${jobid}`}>
        {name}
        {"  "}
      </Link>
      <span className="job-item-success">
        {result === "passed" && "passed"}
      </span>
      <span className="job-item-fail">{result !== "passed" && result}</span>
    </div>
  );
};

