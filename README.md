# MLOps Technical Assessment

## Overview

This project implements a simple MLOps-style batch processing pipeline in Python. The application reads configuration from a YAML file, processes OHLCV market data from a CSV file, computes a rolling mean on the `close` price, generates trading signals, and outputs structured metrics and logs.

## Features

* Configuration-driven execution using YAML
* Deterministic execution with random seed support
* Dataset validation and error handling
* Rolling mean calculation
* Binary signal generation
* Structured metrics output in JSON format
* Detailed logging for observability
* Dockerized for deployment and reproducibility

## Project Structure

```text
mlops_task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log
```

## Configuration

Example `config.yaml`

```yaml
seed: 42
window: 5
version: "v1"
```

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Local Execution

Run the application using:

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Docker Build

Build the Docker image:

```bash
docker build -t mlops-task .
```

## Docker Run

Run the Docker container:

```bash
docker run --rm mlops-task
```

## Sample Output

```json
{
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4989,
    "latency_ms": 83,
    "seed": 42,
    "status": "success"
}
```

## Metrics Generated

The application produces the following metrics:

* rows_processed
* signal_rate
* latency_ms
* seed
* version
* status

## Logging

Logs are written to `run.log` and include:

* Job start
* Configuration validation
* Dataset loading
* Rolling mean computation
* Signal generation
* Metrics summary
* Job completion status
* Error messages (if any)

## Error Handling

The application handles:

* Missing input files
* Invalid CSV files
* Empty datasets
* Missing `close` column
* Invalid configuration files
* Runtime exceptions

## Technologies Used

* Python 3.9+
* Pandas
* NumPy
* PyYAML
* Docker
