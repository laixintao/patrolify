run-planner:
	poetry run reporter --redis-url redis://127.0.0.1:6379 --log-to=reporter-planner.log -vvv planner  --python-checker contrib


run-worker:
	poetry run reporter --redis-url redis://127.0.0.1:6379 --log-to=reporter.log -vvv worker --python-checker contrib --result-path results


run-scheduler:
	rqscheduler --host localhost --port 6379 --db 0
