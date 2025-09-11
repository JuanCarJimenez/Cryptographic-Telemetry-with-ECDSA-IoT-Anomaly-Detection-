import pandas as pd
import numpy as np
from scipy.stats import median_abs_deviation

def robust_z_score(series):
    median_val = series.median()
    mad = median_abs_deviation(series, scale='normal')
    return np.abs(series - median_val) / (mad + 1e-9)

def evaluate(df, tau, score_column, anomaly_column):
    positive = (df[score_column] >= tau).astype(int)
    TP = ((positive == 1) & (df[anomaly_column] == 1)).sum()
    FP = ((positive == 1) & (df[anomaly_column] == 0)).sum()
    TN = ((positive == 0) & (df[anomaly_column] == 0)).sum()
    FN = ((positive == 0) & (df[anomaly_column] == 1)).sum()
    precision = TP / (TP + FP + 1e-9)
    recall = TP / (TP + FN + 1e-9)
    f1 = 2 * precision * recall / (precision + recall + 1e-9)
    fpr= FP / (FP + TN + 1e-9)
    print(f"(tau) = {tau:.2f}")
    print(f"Número de anomalias detectadas: {positive.sum()}")
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print(f"Precision: {precision:.3f}, Recall: {recall:.3f}, F1-Score: {f1:.3f}, FPR: {fpr:.3f}\n")

df = pd.read_csv("iot_crypto_telemetry_drift.csv", index_col='time', parse_dates=True)

df['z_jitter'] = robust_z_score(df['jitter_ms'])

w = {
    'ok_verify': 3.0,          
    'handshake_fail': 2.5,     
    'nonce_reuse': 5.0,        
}

df['binary_penalty_score'] = (df['ok_verify'] * w['ok_verify'] +
                              df['handshake_fail'] * w['handshake_fail'] +
                              df['nonce_reuse'] * w['nonce_reuse'])

df['composite_score'] = df['z_jitter'] + df['binary_penalty_score']
df.rename(columns={'composite_score': 'score'}, inplace=True)

output_file = "scores_and_analysis.csv"
df.to_csv(output_file)

print(f"Número de anomalias verdaderas: {df["anomaly"].sum()}")
for tau in [3.0, 3.5, 4.0, 4.5, 5.0]:
    evaluate(df, tau, score_column='score', anomaly_column='anomaly')
