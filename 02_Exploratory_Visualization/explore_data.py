"""
Initial Data Exploration - Before Visualization
DS209 Final Project: Football Player Scout Tool
"""

import pandas as pd
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', None)

# Load both datasets
print("=" * 80)
print("LOADING DATA")
print("=" * 80)

df_full = pd.read_csv('../data/players_data-2024_2025.csv')
df_light = pd.read_csv('../data/players_data_light-2024_2025.csv')

print(f"\nFull dataset: {df_full.shape[0]} players, {df_full.shape[1]} columns")
print(f"Light dataset: {df_light.shape[0]} players, {df_light.shape[1]} columns")

# Inspect the light dataset (easier to work with initially)
print("\n" + "=" * 80)
print("LIGHT DATASET COLUMNS")
print("=" * 80)
print(df_light.columns.tolist())

print("\n" + "=" * 80)
print("SAMPLE DATA (first 5 rows)")
print("=" * 80)
print(df_light.head())

print("\n" + "=" * 80)
print("DATA TYPES")
print("=" * 80)
print(df_light.dtypes)

print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)
print(df_light.describe())

print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)
print(df_light.isnull().sum().sort_values(ascending=False).head(20))

# Check leagues/competitions
print("\n" + "=" * 80)
print("LEAGUES/COMPETITIONS")
print("=" * 80)
if 'Comp' in df_light.columns:
    print(df_light['Comp'].value_counts())
elif 'competition' in df_light.columns:
    print(df_light['competition'].value_counts())
else:
    print("Looking for competition column...")
    comp_cols = [c for c in df_light.columns if 'comp' in c.lower() or 'league' in c.lower()]
    print(f"Potential columns: {comp_cols}")

# Check positions
print("\n" + "=" * 80)
print("POSITIONS")
print("=" * 80)
if 'Pos' in df_light.columns:
    print(df_light['Pos'].value_counts())
elif 'position' in df_light.columns:
    print(df_light['position'].value_counts())
else:
    pos_cols = [c for c in df_light.columns if 'pos' in c.lower()]
    print(f"Potential columns: {pos_cols}")

# Check key numeric columns for analysis
print("\n" + "=" * 80)
print("KEY METRICS AVAILABLE")
print("=" * 80)
numeric_cols = df_light.select_dtypes(include=['float64', 'int64']).columns.tolist()
print(f"Numeric columns ({len(numeric_cols)}):")
print(numeric_cols)
