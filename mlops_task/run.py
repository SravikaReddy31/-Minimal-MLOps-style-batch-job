import pandas as pd
import numpy as np
import yaml
import argparse
import logging
import json
import time

start_time = time.time()

parser = argparse.ArgumentParser()

parser.add_argument("--input", required=True)
parser.add_argument("--config", required=True)
parser.add_argument("--output", required=True)
parser.add_argument("--log-file", required=True)

args = parser.parse_args()

logging.basicConfig(
    filename=args.log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Job Started")

try:

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    seed = config["seed"]
    window = config["window"]
    version = config["version"]

    np.random.seed(seed)

    logging.info(f"Config Loaded")

    df = pd.read_csv(args.input, header=None)

    df = df[0].str.split(",", expand=True)

    df.columns = df.iloc[0]

    df = df[1:].reset_index(drop=True)

    if "close" not in df.columns:
        raise ValueError("Missing close column")

    df["close"] = pd.to_numeric(df["close"])

    logging.info(f"Rows Loaded: {len(df)}")

    df["rolling_mean"] = df["close"].rolling(window=window).mean()

    logging.info("Rolling Mean Computed")

    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)

    logging.info("Signals Generated")

    rows_processed = len(df)

    signal_rate = float(df["signal"].mean())

    latency_ms = int((time.time() - start_time) * 1000)

    metrics = {
        "version": version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(signal_rate, 4),
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    with open(args.output, "w") as f:
        json.dump(metrics, f, indent=4)

    logging.info("Job Completed Successfully")

    print(json.dumps(metrics, indent=4))

except Exception as e:

    metrics = {
        "version": "v1",
        "status": "error",
        "error_message": str(e)
    }

    with open(args.output, "w") as f:
        json.dump(metrics, f, indent=4)

    logging.error(str(e))

    print(json.dumps(metrics, indent=4))

    raise