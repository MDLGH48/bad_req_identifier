
.ONESHELL:

startup: install env run

install: env
	. env/bin/activate && pip install -r src/requirements.txt

env:
	test -d env || python3.7 -m virtualenv env;

run:
	. env/bin/activate && python src/main.py

local_deploy:
	docker-compose -f ./build_scripts/local/docker-compose.yml up --build  --remove-orphans

test:
	export PYTHONPATH="${PYTHONPATH}:src/" && pytest tests/test.py

clean_pyc:
	find . | grep -E "(__pycache__|\.pyc|.pytest_cache|.coverage|\.pyo$)" | xargs rm -rf

delete_env:
	rm -rf env;