import { Breadcrumb, Breadcrumbs, Icon, Spinner } from "@blueprintjs/core";
import axios from "axios";
import React from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import "./fileexplorer.css"

export default function FileExplorer() {

  let [searchParams, _] = useSearchParams();

  let path = searchParams.get("path");
  let navigate = useNavigate();

  let _prefix = "";

  const BREADCRUMBS = path.split("/").filter(s => s !== "").map(p => {
    if (_prefix !== "") {
      _prefix = _prefix + "/";
    }
    let current = _prefix + p;

    _prefix = current;
    return { to: `/files?path=${current}`, text: p }
  });

  const [content, setContent] = React.useState();
  const [contentLoading, setContentLoading] = React.useState(true);

  React.useEffect(() => {
    setContentLoading(true);
    axios.get("/api/v1/file", { params: { path } }).then(resp => {
      const { data } = resp;
      setContent(data);
      setContentLoading(false);
    })
  }, [path])

  const breadcrumbRenderer = ({ text, to, ...restProps }) => {
    return <Breadcrumb {...restProps} onClick={
      () => { navigate(to) }
    }>{text}</Breadcrumb>
  }

  return <div>
    <Breadcrumbs items={BREADCRUMBS}
      breadcrumbRenderer={breadcrumbRenderer}
    />
    <div className="filecontent-box">
      {contentLoading ? <Spinner /> : <Content content={content} current={path} />}
    </div>
  </div>
}

const Content = ({ content, current }) => {
  const { type } = content;
  if (type === "file") {
    return <FileDisplay content={content.content}></FileDisplay>
  }
  else {
    return <DirectoryDisplay files={content.files} current={current} />
  }
}

const FileDisplay = ({ content }) => {
  return <pre>{content}</pre>;
}

const DirectoryDisplay = ({ files, current }) => {
  return <>{files.map(f => <Item key={f.name} isDir={f.is_dir} name={f.name} current={current}></Item>)}</>;
}

const Item = ({ isDir, name, current }) => {
  let icon = "document";
  if (isDir) {
    icon = "folder-close";
  }
  return <div>

    <Link to={`/files?path=${current}/${name}`}>
      <Icon icon={icon} /> {"  "} {name}
    </Link>

  </div>;
}
