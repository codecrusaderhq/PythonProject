import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

# 🔧 Streamlit konfigürasyonu
st.set_page_config(page_title="Süpermarket Satış Dashboard'u", layout="wide")

# Veri yükleme
@st.cache_data
def veriyi_yukle():
    df = pd.read_csv("data/sales_data.csv", parse_dates=["Tarih"])
    return df

df = veriyi_yukle()

# Başlık
st.title("🛒 Süpermarket Satış Dashboard'u")

# Sidebar filtreler
st.sidebar.header("🔍 Filtreler")
sehirler = st.sidebar.multiselect("Şehir seçin", df["Şehir"].unique(), default=df["Şehir"].unique())
kategoriler = st.sidebar.multiselect("Kategori seçin", df["Kategori"].unique(), default=df["Kategori"].unique())
tarih_araligi = st.sidebar.date_input("Tarih aralığı seçin", [df["Tarih"].min(), df["Tarih"].max()])

# Filtreleme
filtrelenmis_df = df[
    (df["Şehir"].isin(sehirler)) &
    (df["Kategori"].isin(kategoriler)) &
    (df["Tarih"] >= pd.to_datetime(tarih_araligi[0])) &
    (df["Tarih"] <= pd.to_datetime(tarih_araligi[1]))
]

# Genel istatistikler
st.subheader("Genel İstatistikler")
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Satış Tutarı", f"{filtrelenmis_df['Toplam Satış'].sum():,.2f}₺")
col2.metric("Toplam Ürün Adedi", int(filtrelenmis_df["Adet"].sum()))
col3.metric("Satış Sayısı", len(filtrelenmis_df))

# Zaman serisi grafiği
st.subheader("Zaman Serisi Grafiği")
zaman_serisi = filtrelenmis_df.groupby("Tarih")["Toplam Satış"].sum().reset_index()
fig1 = px.line(zaman_serisi, x="Tarih", y="Toplam Satış", title="Günlük Toplam Satış")
st.plotly_chart(fig1, use_container_width=True)

# Şehir ve kategori bazlı grafikler
col4, col5 = st.columns(2)

with col4:
    st.subheader("Şehirlere Göre Satış")
    sehir_satis = filtrelenmis_df.groupby("Şehir")["Toplam Satış"].sum().reset_index()
    fig2 = px.bar(sehir_satis, x="Şehir", y="Toplam Satış", color="Şehir", title="Şehir Bazlı Satış")
    st.plotly_chart(fig2, use_container_width=True)

with col5:
    st.subheader("Kategorilere Göre Satış")
    kategori_satis = filtrelenmis_df.groupby("Kategori")["Toplam Satış"].sum().reset_index()
    fig3 = px.pie(kategori_satis, values="Toplam Satış", names="Kategori", title="Kategori Dağılımı")
    st.plotly_chart(fig3, use_container_width=True)

# Veri çıktısı fonksiyonları
def df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def df_to_html(df):
    return df.to_html(index=False).encode("utf-8")

# İndirme butonları
st.sidebar.markdown("## Veri İndir")

st.sidebar.download_button(
    label="📄 CSV olarak indir",
    data=df_to_csv(filtrelenmis_df),
    file_name="filtrelenmis_satislar.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    label="🌐 HTML olarak indir",
    data=df_to_html(filtrelenmis_df),
    file_name="filtrelenmis_satislar.html",
    mime="text/html"
)