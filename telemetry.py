from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from time import perf_counter_ns
import pandas as pd, numpy as np, os

np.random.seed(1337)
N = 5000
curve = ec.SECP256R1()
priv = ec.generate_private_key(curve)
pub  = priv.public_key()
sizes = [64,128,256,512]
rows, prev_v = [], None

for i in range(N):
    m = os.urandom(int(np.random.choice(sizes)))
    t0 = perf_counter_ns()
    sig = priv.sign(m, ec.ECDSA(hashes.SHA256()))
    t1 = perf_counter_ns()
    t2 = perf_counter_ns()
    ok = 1
    try:
        pub.verify(sig, m, ec.ECDSA(hashes.SHA256()))
    except Exception:
        ok = 0
    t3 = perf_counter_ns()
    s = (t1 - t0)
    v = (t3 - t2)
    jitter = 0 if prev_v is None else abs(v - prev_v)
    rows.append((s, v, len(m), jitter, ok))
    prev_v = v
df = pd.DataFrame(rows, columns=["t_sign_ns","t_verify_ns","msg_bytes","jitter_ns","ok_verify"])
file_path = "telemetry_raw.csv"
df.to_csv("telemetry_raw.csv", index=False)

if os.path.exists(file_path):
    size = os.path.getsize(file_path)
    print(f"CSV file created: {file_path} ({size} bytes)")
else:
    print("CSV file was not created.")
