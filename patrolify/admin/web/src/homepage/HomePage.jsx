import { Divider, H4, H5, Spinner } from "@blueprintjs/core";
import moment from "moment";

import { Card } from "@blueprintjs/core";

import axios from "axios";
import React from "react";
import { Link } from "react-router-dom";
import "./HomePage.css";
import MonitorStatus from "./MonitorStatus";
import { JobStatus } from "../JobAllStatusSpan";

export default function HomePage() {
  const [checkers, setCheckers] = React.useState([]);
  const [loadingCheckers, setLoadingCheckers] = React.useState(true);

  React.useEffect(() => {
    axios.get("/api/v1/triggers").then((resp) => {
      const { data } = resp;
      setCheckers(data.checkers);
      setLoadingCheckers(false);
    });
  }, []);

  if (loadingCheckers) {
    return <Spinner />;
  }
  return (
    <div className="main-body">
      <div className="body-detail">
        <JobTableList checkers={checkers} />
      </div>
      <div className="monitor-status">
        <MonitorStatus />
      </div>
    </div>
  );
}

function JobTableList({ checkers }) {
  return (
    <Card className="job-table-list">
      <H4>Checker List</H4>
      {checkers.map((c) => (
        <Checker checker={c} key={c.name} />
      ))}
    </Card>
  );
}

const Checker = ({ checker }) => {
  const { latest_report_timestamp, name } = checker;
  let last_check = "never";
  if (latest_report_timestamp !== null) {
    last_check = moment.unix(Number(latest_report_timestamp)).from(moment());
  }

  const [result, setResult] = React.useState({});
  const [loadingResult, setLoadingResult] = React.useState(true);
  React.useEffect(() => {
    axios.get(`/api/v1/checker/${name}/latest-result`).then(resp => {
      const { data } = resp;
      console.log(data);
      setLoadingResult(false);
      setResult(data);
    });
  }, [name])
  return (
    <>
      <Divider style={{ margin: 0 }} />
      <div className="checker-row">
        <Link to={`checker/${name}`}>
          <H5>{name}</H5>
        </Link>
        <p>
          <span className="check-active">⬤ active</span>
          <span className="updated-time">
            last checked {last_check}
          </span>
          {!loadingResult &&
            <JobStatus allPassed={result.all_passed} />
          }
        </p>
      </div>
    </>
  );
};
