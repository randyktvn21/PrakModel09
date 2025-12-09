import pandas as pd
import numpy as np

def load_data():
    df = pd.read_csv("dataset_penduduk_bersih.csv")
    df['Perubahan'] = df['Jumlah_Penduduk'].diff()
    df_clean = df.dropna()
    return df, df_clean

def monte_carlo_predict(target_year):
    df, df_clean = load_data()

    # Hitung probabilitas perubahan
    frekuensi = df_clean['Perubahan'].value_counts()
    probabilitas = frekuensi / len(df_clean)

    nilai_perubahan = probabilitas.index.values
    nilai_peluang = probabilitas.values

    last_year = df['Tahun'].iloc[-1]
    last_pop = df['Jumlah_Penduduk'].iloc[-1]

    # Hitung selisih tahun menuju target
    years_to_predict = target_year - last_year
    if years_to_predict < 1:
        years_to_predict = 1

    pred_years = []
    pred_values = []
    current_pop = last_pop

    for i in range(1, years_to_predict + 1):
        perubahan = np.random.choice(nilai_perubahan, p=nilai_peluang)
        current_pop += perubahan

        pred_years.append(last_year + i)
        pred_values.append(int(current_pop))

    return pred_years, pred_values, df
