import pandas as pd
import numpy as np
import datetime
import random


N = 5000  
time_i = datetime.datetime(2025, 9, 8, 18, 0, 0) 
time_interval = 10
file = "iot_crypto_telemetry.csv" 

jitter_base = 2.0
jitter_normal_scale = 4.0 
signature_fail_p_normal = [0.98, 0.02]
handshake_fail_p_normal = [0.95, 0.05]
nonce_reuse_p_normal = [0.99, 0.01]


jitter_anomaly_scale = 15.0 
signature_fail_p_anomaly = [0.6, 0.4]
handshake_fail_p_anomaly = [0.5, 0.5]
nonce_reuse_p_anomaly = [0.8, 0.2]

data = []
current_time = time_i

for i in range(N):

    time_delta = time_interval + random.uniform(-2, 2)
    current_time += datetime.timedelta(seconds=time_delta)

    if np.random.rand() < 0.075:
        jitter = np.random.gamma(jitter_base, jitter_anomaly_scale)
        sig_fail = np.random.choice([0, 1], p=signature_fail_p_anomaly)
        handshake_fail = np.random.choice([0, 1], p=handshake_fail_p_anomaly)
        nonce_reuse = np.random.choice([0, 1], p=nonce_reuse_p_anomaly)
        anomaly = 1
    else:
        jitter = np.random.gamma(jitter_base, jitter_normal_scale)
        sig_fail = np.random.choice([0, 1], p=signature_fail_p_normal)
        handshake_fail = np.random.choice([0, 1], p=handshake_fail_p_normal)
        nonce_reuse = np.random.choice([0, 1], p=nonce_reuse_p_normal)
        anomaly = 0

    record = {
        'time': current_time,
        'jitter_ms': round(jitter, 2),
        'ok_verify': sig_fail,
        'handshake_fail': handshake_fail,
        'nonce_reuse': nonce_reuse,
        'anomaly' : anomaly
    }
    data.append(record)

df = pd.DataFrame(data)
df.set_index('time', inplace=True)

try:
    df.to_csv(file)
    print(f"Se crearon {N} registros en el archivo {file}.")
    print(df.head())
except Exception as e:
    print(f"Error: {e}")
