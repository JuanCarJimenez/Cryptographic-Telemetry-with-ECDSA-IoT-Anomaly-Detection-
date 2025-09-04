import pandas as pd, numpy as np
from scipy.stats import median_abs_deviation  # Import the correct function
import os

df = pd.read_csv("telemetry_raw.csv")
df["y"] = 0

# Delay Injection
win = df.sample(frac= .02).index
df.loc[win, "t_verify_ns"] = (df.loc[win, "t_verify_ns"] * 1.30).astype(int)
df.loc[win, "y"] = 1

# Invalid Signatures
idx = df.sample(frac=0.04, random_state=1337).index
df.loc[idx, "ok_verify"] = 0
df.loc[idx, "y"] = 1

# Jitter Spike
mad_tv = median_abs_deviation(df["t_verify_ns"])
win2 = df.sample(frac=0.02).index
df.loc[win2, "t_verify_ns"] = df.loc[win2, "t_verify_ns"] + int(5*mad_tv)
df.loc[win2, "y"] = 1

# Chequeo de proporción
prop = df["y"].mean()
print("Proporción anomalías:", round(prop*100, 2), "%")
assert 0.05 <= prop <= 0.08, "Ajusten ventanas/porcentajes para quedar entre 5% y 8%."

# Save file
output_file = "telemetry_labeled.csv"
df.to_csv(output_file, index=False)

# Confirmation message
print(f"Archivo guardado: {os.path.abspath(output_file)}")
