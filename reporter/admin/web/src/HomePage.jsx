import { Spinner } from "@blueprintjs/core";
import DataTable from "react-data-table-component";

import axios from "axios";
import React from "react";

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
    <div>
      <JobTableList checkers={checkers} />{" "}
    </div>
  );
}

const columns = [
  {
    name: "Name",
    selector: (row) => row.name,
  },
  {
    name: "latest_report_timestamp",
    selector: (row) => row.latest_report_timestamp,
  },
];

function JobTableList({ checkers }) {
  return <DataTable columns={columns} data={checkers} />;
}
