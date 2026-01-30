import streamlit as st

st.title("👋 Willkommen zur Kasse der Frauenkleiderbörse in der AndreasGemeinde")
st.write("Wähle links im Menü eine Funktion.")

st.info("Kasse: Eingabe von verkauften Artikeln.")
st.info("Belege: Einsicht in einzelne Belege.")
st.info("Statistik: Übersicht über Gesamtsummen und Spenden.")
st.info("Verkauferbericht: Ausdruck der Berichte für Verkäufer.")


st.warning("Bitte eine Übersicht zu den Verkäufer in der beigefügten Exceltabelle hinterlegen: (A) Name, (B) Nummer, (C) Spendenanteil. " \
"Belege der Kasse werden einzeln im csv-Format im Ordner Belege gespeichert. Dadurch kommt es bei einem Neustart der Kasse zu keinem Datenverlust. " \
"Die Berichte können für alle Verkäufer über einen Klick als PDF gedruckt werden und sind dann im Ordner pdfs gespeichert.") 