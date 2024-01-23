import { H5, Card, H6, Icon, Spinner } from "@blueprintjs/core";
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
    <Card className="worker-card">
      <H5>Total running workers: {data.total_worker_count}</H5>

      {data.workers.map((worker, index) => <Worker worker={worker} key={index} />)}
    </Card>

    <Card className="queue-card">
      <H5>Checker Queue</H5>
      <QueueStatus queue={data.checker_queue} />
    </Card>

    <Card className="queue-card">
      <H5>Reporter Queue</H5>
      <QueueStatus queue={data.reporter_queue} />
    </Card>
    <Card >
      <H5>Redis Info</H5>
      <p>Used memory: {data.redis.used_memory_human}</p>
    </Card>
  </div>
}

const QueueStatus = ({ queue }) => {
  return <div>

    <p>
      {queue.count} jobs pending to be executed, {queue.started_job} in executing.
    </p>

    <p>
      Finished {queue.finished_job}, failed {queue.failed_job}.
    </p>
  </div>;
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
