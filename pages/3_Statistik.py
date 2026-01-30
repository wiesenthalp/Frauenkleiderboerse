import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime

st.set_page_config(layout="wide")
st.title("📊 Statistik")

# Rechnungsverzeichnis
Belegeordner = "belege"
os.makedirs(Belegeordner, exist_ok=True)

alle = []
for f in os.listdir(Belegeordner):
    if f.startswith("beleg_") and f.endswith(".csv"):
        dateipfad = os.path.join(Belegeordner, f)
        df = pd.read_csv(dateipfad)
        df['Verkäufer'] = df['Verkäufer'].astype(str).str.zfill(4)
        alle.append(df)

if alle:
    df_all = pd.concat(alle, ignore_index=True)
    df_all['Datum'] = pd.to_datetime(df_all.get('Datum', pd.Timestamp.today()))

    # Verkäuferdaten
    verkaeufer_df = pd.read_excel("verkaeufer.xlsx", dtype={"Nummer": str})
    verkaeufer_df["Nummer"] = verkaeufer_df["Nummer"].str.zfill(4)
    verkaeufer_df["Spendenanteil"] = verkaeufer_df["Spendenanteil"].fillna(0)

    # Zusammenführen für Spendenberechnung
    df_merged = df_all.merge(verkaeufer_df, left_on="Verkäufer", right_on="Nummer", how="left")
    df_merged["Spendenanteil"] = df_merged["Spendenanteil"].astype(float)
    df_merged["Spende"] = df_merged["Preis"] * df_merged["Spendenanteil"]
    
    # Gesamtsummen
    gesamt = df_merged["Preis"].sum()
    spenden = df_merged["Spende"].sum()
    auszahlung = gesamt - spenden

    st.subheader("💰 Gesamtsummen")
    col1, col2, col3 = st.columns(3)
    col1.metric("Gesamtbetrag", f"{gesamt:.2f} €")
    col2.metric("Spendenbetrag", f"{spenden:.2f} €")
    col3.metric("Auszahlungsbetrag", f"{auszahlung:.2f} €")

    st.markdown("---")

    # Umsatz pro Verkäufer
    st.subheader("📦 Gesamtumsatz pro Verkäufer")
    umsatz_pro_verkaeufer = df_merged.groupby("Verkäufer")["Preis"].sum().sort_values(ascending=False)

    fig1, ax1 = plt.subplots(figsize=(10, 7))
    ax1.barh(umsatz_pro_verkaeufer.index[::-1], umsatz_pro_verkaeufer.values[::-1], color="skyblue")
    ax1.set_xlabel("Gesamtumsatz (€)")
    ax1.set_ylabel("Verkäufer")
    ax1.set_title("Gesamtumsatz pro Verkäufer")
    st.pyplot(fig1)

    # Spenden pro Verkäufer
    st.subheader("🎁 Spenden pro Verkäufer")
    spenden_pro_verkaeufer = df_merged.groupby("Verkäufer")["Spende"].sum().sort_values(ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 7))
    ax2.barh(spenden_pro_verkaeufer.index[::-1], spenden_pro_verkaeufer.values[::-1], color="salmon")
    ax2.set_xlabel("Spendenbetrag (€)")
    ax2.set_ylabel("Verkäufer")
    ax2.set_title("Spenden pro Verkäufer")
    st.pyplot(fig2)



else:
    st.info("Keine Daten zum Auswerten.")
