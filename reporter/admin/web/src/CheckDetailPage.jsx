import { Divider, FormGroup, H5, Icon, InputGroup, Spinner, Tab, Tabs } from "@blueprintjs/core";
import axios from "axios";
import moment from "moment";
import React from "react";
import { Tree } from "react-arborist";
import { Link, useParams } from "react-router-dom";


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
      {checkResult.passed.length} passed, {checkResult.not_passed.length} not passed, {checkResult.failed.length} failed to run the check job (got unhandled exceptions).
    </div>


    <Tabs>
      <Tab id="tree-view" title="Tree View" icon="diagram-tree" panel={<JobTree jobData={checkResult.job_info} head={checkResult.start_job_id}
      />} />
      <Tab id="list-view" title="List by Result" icon="properties" panel={<JobList checkResult={checkResult}

      />} />
    </Tabs>
  </div >;
}

const CheckItem = ({ jobid, index, result, name, showIndex = true }) => {
  return (
    <div key={jobid} className="job-link">
      {showIndex && <span> ({index}).</span>}
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


const JobTree = ({ jobData, head,
}) => {

  const [filterTargetName, setFilterTargetName] = React.useState("");
  const getTree = (data, key) => {
    const node = data[key];

    let result = "passed";
    if (!node.run_success) {
      result = "failed";
    } else if (!node.check_pass) {
      result = "not passed";
    }

    return {
      id: key,
      name: node.target,
      children: node.child_job_ids.map(id => getTree(data, id)),
      result: result,
    };
  }
  const treeHead = getTree(jobData, head);

  const Node = ({ node, style, dragHandle }) => {
    return (
      <div style={style} ref={dragHandle} onClick={() => node.toggle()}>
        <div style={{ display: "flex", fontFamily: "Monaco", alignItems: "center" }}>
          {node.data.children?.length > 0 ? <Icon icon="fork" /> : <Icon icon="star" />}
          <span style={{ marginLeft: "4px" }}>
            <CheckItem jobid={node.data.id} result={node.data.result} name={node.data.name} showIndex={false} />
          </span>
        </div>
      </div >
    );
  }

  return (
    <>
      <div >
        <div className="filters">
          <FormGroup
            label="Filter by target name"
            labelFor="search-target-name"
          >
            <InputGroup id="search-target-name" placeholder="target name, support result like passed, not passed, failed." value={filterTargetName} onChange={e => setFilterTargetName(e.target.value)} />
          </FormGroup>
        </div>
        <Tree initialData={[treeHead]} disableDrag={true} disableEdit={true} disableDrop={true} width="100%"
          searchTerm={filterTargetName}
          searchMatch={
            (node, term) => `${node.data.name} ${node.data.result}`.toLowerCase().includes(term.toLowerCase())
          }
        >
          {Node}
        </Tree>
      </div>
    </>
  );
}

const JobList = ({ checkResult }) => {

  return (
    <>
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
    </>
  );
}
