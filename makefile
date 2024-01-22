run-planner:
	poetry run reporter --redis-url redis://127.0.0.1:6379 --log-to=reporter-planner.log -vvv planner  --python-checker contrib

run-worker:
	poetry run reporter --redis-url redis://127.0.0.1:6379 --log-to=reporter.log -vvv worker --python-checker contrib --result-path results --queue checker --queue reporter

run-scheduler:
	rqscheduler --host localhost --port 6379 --db 0

run-admin:
	poetry run reporter --redis-url redis://127.0.0.1:6379 --log-to=reporter-admin.log -vvv admin --port 8084 --python-checker contrib --result-path results

run-admin-web:
	cd reporter/admin/web && PORT=3004 yarn start

build:
	cd reporter/admin/web/; yarn build --base /static --emptyOutDir --outDir ../frontend_dist/
