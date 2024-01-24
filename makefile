.PHONY: build-frontend release

run-planner:
	poetry run patrolify --redis-url redis://127.0.0.1:6379 --log-to=patrolify-planner.log -vvv planner  --python-checker contrib

run-worker:
	poetry run patrolify --redis-url redis://127.0.0.1:6379 --log-to=patrolify.log -vvv worker --python-checker contrib --result-path results --queue checker --queue reporter

run-scheduler:
	rqscheduler --host localhost --port 6379 --db 0

run-admin:
	poetry run patrolify --redis-url redis://127.0.0.1:6379 --log-to=patrolify-admin.log -vvv admin --port 8084 --python-checker contrib --result-path results

run-admin-web:
	cd patrolify/admin/web && PORT=3004 yarn start

build-frontend:
	cd patrolify/admin/web/; yarn; yarn build --base /static --emptyOutDir --outDir ../frontend_dist/
	mv patrolify/admin/web/node_modules /tmp/a_node_modules

release: build-frontend
	poetry build
