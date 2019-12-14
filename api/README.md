# WUESTbot API

## Getting Started

Setup a virtual environment:

> This needs to be a seperate environment from the one the [bot][bot] uses.

```shell
python3 -m venv venv_api
source venv_api/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

## Run it

To run in development mode (no Prometheus metrics, no gunicorn):

```shell
make run
```

To run in production mode:

```shell
make run/prod
```

You can also start the script without `make`, but `prometheus_multiproc_dir` must
be passed, which needs to be a writable directory:

```shell
./gunicorn.sh .multiporc_dir
```

[bot]: ../README.md
