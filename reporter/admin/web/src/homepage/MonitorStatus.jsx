import { Card, H6, Icon, Spinner } from "@blueprintjs/core";
import moment from "moment";
import React from "react";
import "./MonitorStatus.css";
import axios from "axios";
export default function MonitorStatus() {
  const [data, setData] = React.useState(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    axios.get("/api/v1/monitor-info").then(resp => {
      setData(resp.data);
      setLoading(false);
    })
  }, [])

  if (loading) {
    return <Spinner />
  }
  return <div>
    <Card>
      <p>Total running workers: {data.total_worker_count}</p>

      {data.workers.map((worker, index) => <Worker worker={worker} key={index} />)}
    </Card>
  </div>
}

const Worker = ({ worker }) => {
  return <div className="worker-block">
    <H6>{worker.hostname} PID={worker.pid}</H6>
    <div style={{ display: "flex", gap: "8px", alignItems: "center", marginBottom: "8px" }}>
      <Icon icon={worker.state === "idle" ? "circle" : "social-media"}
        color={worker.state === "idle" ? "green" : "blue"} />
      <span>{worker.state}</span>
    </div>

    <p>
      Work for queues: {worker.queues.join(", ")}.
    </p>

    <p>Finished {worker.successful_job_count} jobs, worked for {moment.duration(worker.total_working_time, 'seconds').humanize()}, birthday was <b>{moment(worker.birth_date).format("YYYY-MM-DD HH:mm z")}</b>, last heartbeat at {moment(worker.last_heartbeat).from(moment())}.</p>
  </div>
}
