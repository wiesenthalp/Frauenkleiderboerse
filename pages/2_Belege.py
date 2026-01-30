import streamlit as st
import pandas as pd
import os

st.title("📁 Belege einsehen")

# Rechnungsverzeichnis
Belegeordner = "belege"
os.makedirs(Belegeordner, exist_ok=True)

files = [f for f in os.listdir(Belegeordner) if f.startswith("beleg_") and f.endswith(".csv")]

if files:
    datei = st.selectbox("Wähle eineb Beleg:", files)
    dateipfad = os.path.join(Belegeordner, datei)
    df = pd.read_csv(dateipfad)
    st.dataframe(df)
    st.write(f"**Gesamtsumme:** {df['Preis'].sum():.2f} €")
else:
    st.info("Noch keine Belege gespeichert.")
