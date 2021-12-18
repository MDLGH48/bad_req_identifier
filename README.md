# bad_req_identifier
Service that identifies abnormal http requests being sent to monitored APIs

# Requirements
- make
- python3.7
- docker + docker-compose

If WINDOWS user: run in vscode devcontainer with python3.7 base image (debian recommended)

# Setup + Run dev (First Time)

```
make startup
```
or
- `python3.7 -m venv env`
- `source env/bin/activate`
- `pip install -r src/requirements.txt`
- `python src/main.py`

# Run dev
```
make run
```
or
- `python src/main.py`

# Run docker on local machine 
(port `8001`)

```
make local_deploy
```
or
```
docker-compose -f ./build_scripts/local/docker-compose.yml up --build  --remove-orphans
```

# TEST
```
make test
```
or
```
export PYTHONPATH="${PYTHONPATH}:src/" && pytest tests/test.py
```

# Documentation
- swagger = `localhost:8001/docs`
- redoc = `localhost:8001/redoc`