export const JobStatus = ({ allPassed }) => (
  <>
    <span className="job-item-success">
      {allPassed && "success"}
    </span>
    <span className="job-item-fail">{!allPassed && "fail"}</span>
  </>
)

