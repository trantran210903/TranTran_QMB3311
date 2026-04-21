# NBA Shot Chart Analysis 19_20

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sqlite3
import os

df = pd.read_csv('nbaShots19_20.csv')

# 1. Summary Statistics


print("=== Summary Statistics ===")
print(df[['SHOT_DISTANCE', 'SHOT_MADE_FLAG', 'PERIOD']].describe())
print()

conn = sqlite3.connect(':memory:')
df.to_sql('shots', conn, index=False, if_exists='replace')

by_zone = pd.read_sql("""
    SELECT SHOT_ZONE_BASIC AS zone,
           COUNT(*) AS attempts,
           ROUND(AVG(SHOT_MADE_FLAG) * 100, 1) AS fg_pct
    FROM shots
    GROUP BY SHOT_ZONE_BASIC
    ORDER BY fg_pct DESC
""", conn)

print("=== FG% by Zone ===")
print(by_zone)
print()

plt.figure(figsize=(8, 5))
plt.bar(by_zone['zone'], by_zone['fg_pct'], color='steelblue')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Court Zone')
plt.ylabel('Field Goal %')
plt.title('FG% by Court Zone (2019-20 Season)')
plt.tight_layout()
plt.savefig('fig1_zones_2019_20.png', dpi=150)
plt.close()

# 2. Regression Analysis 

x = df['SHOT_DISTANCE']
y = df['SHOT_MADE_FLAG']

slope, intercept = np.polyfit(x, y, 1)
y_hat = intercept + slope * x

print("=== Regression Output ===")
print(f"Intercept: {intercept:.4f}")
print(f"SHOT_DISTANCE coefficient: {slope:.4f}")
print()

plot_df = df.sample(n=min(15000, len(df)), random_state=42).sort_values('SHOT_DISTANCE')

plt.figure(figsize=(8, 5))
plt.scatter(plot_df['SHOT_DISTANCE'], plot_df['SHOT_MADE_FLAG'], alpha=0.05, color='gray')
plt.plot(plot_df['SHOT_DISTANCE'], intercept + slope * plot_df['SHOT_DISTANCE'], color='red')
plt.xlabel('Shot Distance (ft)')
plt.ylabel('Shot Made (1 = yes, 0 = no)')
plt.title('Shot Distance vs. Shot Outcome (2019-20 Season)')
plt.tight_layout()
plt.savefig('fig2_regression_2019_20.png', dpi=150)
plt.close()

conn.close()
print("Analysis complete.")



