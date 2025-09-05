import pandas as pd
import numpy as np
from scipy.stats import median_abs_deviation

df = pd.read_csv("telemetry_raw.csv")
def robust_z_score(series):
    mad = median_abs_deviation(series, scale='normal')
    median_val = series.median()
    z = np.abs(series - median_val) / mad
    return z

z_t_verify = robust_z_score(df["t_verify_ns"])
z_jitter = robust_z_score(df["jitter_ns"])


df["score"] = np.maximum(z_t_verify, z_jitter)
tau = 3.0
df["anomaly"] = (df["score"] >= tau).astype(int)

print(df[["t_verify_ns", "jitter_ns", "score", "anomaly"]].head())

for tau in [2.5, 3.0, 3.5, 4.0]:
    n_anomalies = (df["score"] >= tau).sum()
    prop = n_anomalies / len(df)
    print(f"tau={tau}: {n_anomalies} anomalies, {prop:.2%} of dataset")

