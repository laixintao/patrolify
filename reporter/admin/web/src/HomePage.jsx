import { Divider, H4, H5, Spinner } from "@blueprintjs/core";

import { Card } from "@blueprintjs/core";

import axios from "axios";
import React from "react";
import "./HomePage.css";

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
      <JobTableList checkers={checkers} />
    </div>
  );
}

function JobTableList({ checkers }) {
  return (
    <Card>
      <H4>Checker List</H4>
      {checkers.map((c) => (
        <Checker checker={c} key={c.name} />
      ))}
    </Card>
  );
}

const Checker = ({ checker }) => {
  return (
    <>
      <Divider style={{ margin: 0 }} />
      <div className="checker-row">
        <H5>{checker.name}</H5>
        <p>
          <span className="check-active">⬤ active</span>
          <span className="updated-time">Checked 5 minustes ago</span>
        </p>
      </div>
    </>
  );
};
