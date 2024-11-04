import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
sns.set(style='dark')


def categorize_ispu(x):
    if 0 <= x <= 50:
        return "Baik"
    elif 51 <= x <= 100:
        return "Sedang"
    elif 101 <= x <= 200:
        return "Tidak Sehat"
    elif 201 <= x <= 300:
        return "Sangat Tidak Sehat"
    else:
        return "Berbahaya"


def create_annual_avg(df):
    annual_avg = df.groupby(['station', df['date'].dt.year]).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    }).round(2).reset_index()

    annual_avg['date'] = annual_avg['date'].astype(str)

    annual_avg['min_ispu'] = annual_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].min(axis=1)
    annual_avg['polutan_min_ispu'] = annual_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].idxmin(axis=1)

    annual_avg['max_ispu'] = annual_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].max(axis=1)
    annual_avg['polutan_max_ispu'] = annual_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].idxmax(axis=1)
    annual_avg['category'] = annual_avg['max_ispu'].apply(
        lambda x: categorize_ispu(x))

    return annual_avg


def create_five_yr_avg(df):
    five_yr_avg = df.groupby(by='station').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean'
    }).round(2).reset_index()

    five_yr_avg['min_ispu'] = five_yr_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].min(axis=1)
    five_yr_avg['polutan_min_ispu'] = five_yr_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].idxmin(axis=1)

    five_yr_avg['max_ispu'] = five_yr_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].max(axis=1)
    five_yr_avg['polutan_max_ispu'] = five_yr_avg[[
        'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].idxmax(axis=1)
    five_yr_avg['category'] = five_yr_avg['max_ispu'].apply(
        lambda x: categorize_ispu(x))

    return five_yr_avg


daily_avg_df = pd.read_csv("ISPU.csv")

daily_avg_df['date'] = pd.to_datetime(daily_avg_df['date'])
daily_avg_df.sort_values(by="date", inplace=True)
daily_avg_df.reset_index(inplace=True)

# Membuat header dashboard
st.header(':cloud: Dashboard Indeks Standar Pencemar Udara (ISPU) :cloud:')

# Menambahkan markdown definisi ISPU
st.markdown("**Indeks Standar Pencemar Udara (ISPU)** adalah angka yang tidak punya satuan, tapi penting banget buat mengetahui seberapa bersih atau kotor udara di suatu tempat. Angka ini dipakai buat mengecek dampak udara terhadap kesehatan kita, tampilan lingkungan, dan juga buat makhluk hidup lainnya. Jadi, ISPU ini semacam pengukur kualitas udara yang kita hirup setiap hari! :smile:")

# Menambahkan tabel kategori ISPU
kategori_df = pd.DataFrame({
    "Kategori": ["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"],
    "Angka rentang": ["1 - 50", "51 - 100", "101 - 200", "201 - 300", ">= 301"],
    "Keterangan": [
        "Kualitas udara sangat baik! ⭐⭐⭐, udara ini tidak akan kasih dampak negatif buat manusia, hewan, maupun tumbuhan.",
        "Kualitas udara sedang ⭐⭐, artinya masih bisa diterima bagi kesehatan manusia, hewan, dan tumbuhan. Tapi, buat beberapa kelompok sensitif, perlu ngurangin aktivitas fisik yang terlalu lama dan berat.",
        "Kualitas udara yang tidak sehat ⭐, udara ini ngerugiin manusia, hewan, dan tumbuhan lho. Kelompok sensitif harus terus memantau kondisi tubuh dan perhatiin gejala seperti batuk atau sesak napas.",
        "Kualitas udara yang bener-bener tidak sehat!, udara ini bisa ningkatin risiko kesehatan makhluk hidup yang terpapar. Waspada selalu dan hindari aktivitas di luar ruangan terlalu lama (apalagi buat kelompok sensitif).",
        "Kualitas udara berbahaya! ⚠️, udara ini benar-benar merugikan kesehatan lho. Makhluk hidup bisa kena masalah kesehatan serius dan perlu penanganan serius. Hindari aktivitas di luar ruangan."
    ]
})
st.table(kategori_df)

five_yr_avg = create_five_yr_avg(daily_avg_df)

# Menambahkan tampilan informasi dan grafik daerah paling berpolusi dan paling bersih
st.subheader(
    'Daerah Paling Berpolusi dan Paling Bersih berdasarkan Nilai ISPU Dalam 5 Tahun (2013-2017)')

col1, col2 = st.columns(2)

# Informasi nilai ISPU Tertinggi
with col1:
    ispu_max = five_yr_avg.max_ispu.max()
    st.metric("ISPU Tertinggi", value=ispu_max)

# Informasi nilai ISPU Terendah
with col2:
    ispu_min = five_yr_avg.max_ispu.min()
    st.metric("ISPU Terendah", value=ispu_min)

# Grafik daerah paling berpolusi
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

colors_min = ["#A1C349", "#D8D1BD", "#D8D1BD", "#D8D1BD", "#D8D1BD"]
colors_max = ["#F9A03F", "#D8D1BD", "#D8D1BD", "#D8D1BD", "#D8D1BD"]

sns.barplot(x="max_ispu", y="station", data=five_yr_avg.sort_values(
    by='max_ispu', ascending=False).head(5), palette=colors_max, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Indeks Standar Pencemar Udara (ISPU)",
                 labelpad=10, fontsize=12)
ax[0].set_title("Daerah Paling Berpolusi berdasarkan \nPerhitungan Indeks Standar Pencemar Udara (ISPU) \ndalam 5 Tahun (2013-2017)", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(x="max_ispu", y="station", data=five_yr_avg.sort_values(
    by="max_ispu", ascending=True).head(5), palette=colors_min, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Indeks Standar Pencemar Udara (ISPU)",
                 labelpad=10, fontsize=12)
ax[1].set_title("Daerah Paling Bersih berdasarkan \nPerhitungan Indeks Standar Pencemar Udara (ISPU) \ndalam 5 Tahun (2013-2017)", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=12)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

# Menambahkan tampilan informasi dan grafik tren ISPU 6 polutan per daerah
st.subheader(
    'Tren ISPU 6 Polutan di Setiap Daerah')

# Membuat filter station
station = daily_avg_df['station'].unique()
selected_station = st.selectbox("Pilih Station", station)
filtered_df = daily_avg_df[daily_avg_df['station'] == selected_station]

# Menerapkan filter untuk menampilkan semua data sesuai station
annual_avg = create_annual_avg(filtered_df)
five_yr_avg_filtered = create_five_yr_avg(filtered_df)

# Menampilkan nama station
st.subheader(f':orange[{selected_station}]')

# Menampilkan informasi nilai ISPU
col1, col2, col3 = st.columns(3)

# Informasi nilai ISPU dalam 5 tahun sesuai dengan daerah yang difilter
with col1:
    nilai_ispu = five_yr_avg_filtered.max_ispu.max()
    st.metric("ISPU (2013-2017)", value=nilai_ispu)

# Informasi kategori ISPU
with col2:
    kategori_ispu = five_yr_avg_filtered.category.mode()[0]
    st.metric("Kategori", value=kategori_ispu)

# Informasi jenis polutan paling dominan dalam 5 tahun sesuai dengan daerah yang difilter
with col3:
    dominan_polutan = five_yr_avg_filtered.polutan_max_ispu.mode()[0]
    st.metric("Polutan Dominan", value=dominan_polutan)

# Grafik tren 6 polutan di setiap daerah
fig = plt.figure(figsize=(15, 8))

colors_polutant = ["#F9A03F", "#FF6363",
                   "#6B4226", "#3A86FF", "#FFBE0B", "#8338EC"]
polutant = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]

for i in range(len(polutant)):
    plt.plot(annual_avg['date'], annual_avg[polutant[i]], marker='o',
             label=polutant[i], color=colors_polutant[i], linewidth=2)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.ylabel("ISPU", fontsize=18, labelpad=20)

plt.legend(title="Polutan", fontsize=12, loc='upper center',
           bbox_to_anchor=(0.5, -0.15), ncol=6)

st.pyplot(fig)
