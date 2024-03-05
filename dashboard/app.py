import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Judul dashboard
st.title("Analisis Data Sewa Sepeda")

# Mengimpor data
data = pd.read_csv('day.csv')

# Tampilkan dataset
st.subheader('Tampilan Dataset')
st.write(data)

# Konversi kolom 'dteday' ke format datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Line chart untuk persewaan sepeda dari waktu ke waktu
st.subheader("Persewaan Sepeda dari Waktu ke Waktu (Harian)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['dteday'], data['cnt'], marker='o', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Persewaan Sepeda")
ax.set_title("Persewaan Sepeda dari Waktu ke Waktu (Harian)")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Keterangan tambahan
st.write("""
Dari grafik di atas, terlihat bahwa terdapat pola berulang pada interval tertentu.
""")

# Statistik persewaan per bulan
st.subheader('Statistik Persewaan Per Bulan')

# Mengelompokkan data berdasarkan bulan dan menghitung statistik
rentals_by_month = data.groupby('mnth').agg({
    'cnt': ['sum', 'mean', 'median']
})

# Mengurutkan data berdasarkan jumlah total persewaan
rentals_by_month_sorted = rentals_by_month.sort_values(('cnt', 'sum'), ascending=False)

# Menampilkan tabel
st.write(rentals_by_month_sorted)

# Diagram batang persewaan total per bulan
st.subheader('Diagram Batang Jumlah Total Persewaan Per Bulan (Menurun)')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=rentals_by_month_sorted.index, y=rentals_by_month_sorted[('cnt', 'sum')], ax=ax, order=rentals_by_month_sorted.index)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Jumlah Persewaan")
ax.set_title("Jumlah Total Persewaan Per Bulan (Menurun)")
ax.tick_params(axis='x', rotation=45)

# Menambahkan label pada batang
for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')

st.pyplot(fig)

# Statistik persewaan per musim
st.subheader('Analisis Persewaan Berdasarkan Musim')
rentals_by_season = data.groupby('season').agg({
    'cnt': ['sum', 'mean', 'median']
})
st.write(rentals_by_season)

# Visualisasi bar chart jumlah total persewaan per musim
st.subheader('Bar Chart: Jumlah Total Persewaan per Musim')
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=rentals_by_season.index, y=rentals_by_season['cnt']['sum'], ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Total Persewaan')
ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
plt.tight_layout()

# Menambahkan label pada batang
for index, value in enumerate(rentals_by_season['cnt']['sum']):
    ax.text(index, value + 10, str(value), ha='center', va='bottom')

st.pyplot(fig)


# Visualisasi scatter plot jumlah total persewaan per musim
st.subheader('Scatter Plot: Hubungan antara Total Persewaan dan Musim')
plt.figure(figsize=(8, 6))
sns.scatterplot(x='season', y='cnt', data=data)
plt.xlabel('Musim')
plt.ylabel('Total Persewaan')
plt.xticks(range(1, 5), labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
plt.tight_layout()

# Menghitung garis regresi
slope, intercept, r_value, p_value, std_err = linregress(data['season'], data['cnt'])
x_values = np.array([1, 2, 3, 4])
y_values = slope * x_values + intercept

# Menambahkan garis regresi ke plot
plt.plot(x_values, y_values, color='red', linestyle='--', label='Garis Regresi')

plt.legend()  # Menampilkan legenda
st.pyplot()
