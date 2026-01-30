import streamlit as st
import pandas as pd
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Belegeverzeichnis
Belegeordner = "belege"
os.makedirs(Belegeordner, exist_ok=True)

# Excel-Datei mit Verkäuferdaten laden
verkaeufer_df = pd.read_excel("verkaeufer.xlsx", dtype={"Nummer": str})
verkaeufer_df["Nummer"] = verkaeufer_df["Nummer"].str.zfill(4)  # macht aus der Zahl einen vierstelligen String und füllt mit Nullen auf, z.B. von 1 --> "0001"

# # Alle belegedateien automatisch einlesen
# verkaufsdaten_alle = []
# for f in os.listdir(Belegeordner):
#     if f.startswith("beleg_") and f.endswith(".csv"):
#         dateipfad = os.path.join(Belegeordner, f)
#         df = pd.read_csv(dateipfad)
#         df["Verkäufer"] = df["Verkäufer"].astype(str).str.zfill(4)  # macht aus der Zahl einen vierstelligen String und füllt mit Nullen auf, z.B. von 1 --> "0001"
#         verkaufsdaten_alle.append(df)
# # Gemeinsames DataFrame erzeugen
# verkaufsdaten_df = pd.concat(verkaufsdaten_alle, ignore_index=True) if verkaufsdaten_alle else pd.DataFrame()

# Alle belegedateien automatisch einlesen
verkaufsdaten_alle = []
for f in os.listdir(Belegeordner):
    if f.startswith("beleg_") and f.endswith(".csv"):
        dateipfad = os.path.join(Belegeordner, f)
        df = pd.read_csv(dateipfad)
        df["Verkäufer"] = df["Verkäufer"].astype(str).str.zfill(4)  # macht aus der Zahl einen vierstelligen String und füllt mit Nullen auf, z.B. von 1 --> "0001"
        
        # Umwandlung der Belegenummer zu String
        df["Belegenummer"] = df["Belegenummer"].astype(str)
        
        verkaufsdaten_alle.append(df)
# Gemeinsames DataFrame erzeugen
verkaufsdaten_df = pd.concat(verkaufsdaten_alle, ignore_index=True) if verkaufsdaten_alle else pd.DataFrame()
# Sicherstellen, dass alle Spalten in den richtigen Typen vorliegen
verkaufsdaten_df["Belegenummer"] = verkaufsdaten_df["Belegenummer"].astype(str)  # z.B. als String


# Funktion zur PDF-Erstellung für einen einzelnen Verkäufer
def create_pdf(verkaeufer_nummer, verkaufsdaten, output_filename):
    try:
        verkaeufer_info = verkaeufer_df[verkaeufer_df["Nummer"] == verkaeufer_nummer].iloc[0]
    except IndexError:
        st.error(f"Keine Daten für Verkäufernummer {verkaeufer_nummer} gefunden.")
        return

    # Sicherstellen, dass das Verzeichnis existiert
    os.makedirs("pdfs", exist_ok=True)
    output_path = os.path.join("pdfs", output_filename)

    name = verkaeufer_info["Name"]
    spendenanteil_prozent = verkaeufer_info.get("Spendenanteil", 0)  # z. B. 10
    try:
        spendenanteil_float = float(str(spendenanteil_prozent).replace("%", "").replace(",", "."))
    except:
        spendenanteil_float = 0

    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    total_pages = 1  # Seitenzahl manuell starten

    def add_title(page_num, total_pages):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 800, "Kleiderbörse - 06. Februar 2026")
        c.drawString(100, 780, "AndreasGemeinde")
        c.drawString(100, 760, "Wilhelminenstraße 4-5")
        c.drawString(100, 740, "24536 Neumünster")
        c.drawString(100, 700, f"Verkäufer: {name}")
        c.drawString(100, 680, f"Verkäufernummer: {verkaeufer_nummer}")
        c.drawString(300, 50, f"{page_num}")

    def add_header(page_num, total_pages):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, 800, "Kleiderbörse - 06. Februar 2026")
        c.drawString(100, 780, f"{verkaeufer_nummer} - {name}")
        c.drawString(300, 50, f"{page_num}")
        y_position=750
        # Tabellenüberschrift
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, "Index")
        c.drawString(150, y_position, "Belegnummer")
        c.drawString(260, y_position, "Uhrzeit")
        c.drawString(400, y_position, "Preis")
        y_position -= 20
        c.setFont("Helvetica", 12)

    # Kopfzeile und Verkaufsdaten vorbereiten
    verkaufte_artikel = verkaufsdaten[verkaufsdaten["Verkäufer"] == verkaeufer_nummer]

    gesamtbetrag = verkaufte_artikel["Preis"].sum()
    spendenbetrag = gesamtbetrag * spendenanteil_float
    auszahlungsbetrag = gesamtbetrag - spendenbetrag

    y_position = 630

    add_title(total_pages, total_pages)
    
    c.setFont("Helvetica-Bold", 12)
    x_pos_betrag = 350
    c.drawString(100, y_position, f"Gesamtbetrag: ")
    c.drawRightString(x_pos_betrag, y_position, f"{gesamtbetrag:.2f} €") 
    y_position -= 20
    c.drawString(100, y_position, f"Spendenbetrag ({(spendenanteil_float*100):.1f}%):")
    c.drawRightString(x_pos_betrag, y_position, f"{spendenbetrag:.2f} €") 
    y_position -= 20
    c.drawString(100, y_position, f"Auszahlungsbetrag: ")
    c.drawRightString(x_pos_betrag, y_position, f"{auszahlungsbetrag:.2f} €") 
    y_position -= 40  # Leerzeile

    index_artikel = 0

    if verkaufte_artikel.empty:
        c.drawString(100, y_position, "Keine Verkäufe vorhanden.")
    else:
        # Tabellenüberschrift
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y_position, "Index")
        c.drawString(150, y_position, "Belegnummer")
        c.drawString(260, y_position, "Uhrzeit")
        c.drawString(400, y_position, "Preis")
        y_position -= 20
        c.setFont("Helvetica", 12)

        gesamtbetrag = 0

        for idx, row in verkaufte_artikel.iterrows():
            index_artikel += 1
            c.drawRightString(130, y_position, str(index_artikel))
            c.drawString(150, y_position, str(row.get("Belegenummer", "-")))
            c.drawString(260, y_position, str(row.get("Uhrzeit", "-")))
            c.drawString(400, y_position, f"{row.get('Preis', 0):.2f} €")
            gesamtbetrag += row.get("Preis", 0)
            y_position -= 20

            if y_position < 100:  # Neue Seite starten, wenn Platz zu Ende ist
                total_pages += 1
                c.showPage()
                add_header(total_pages, total_pages)  # Kopfzeile wiederholen
                y_position = 730  # Zurück zur oberen Position

    c.save()


# PDFs für alle Verkäufer erstellen
def create_pdfs_for_all(verkaufsdaten):
    os.makedirs("pdfs", exist_ok=True)
    for nummer in verkaeufer_df["Nummer"]:
        create_pdf(str(nummer), verkaufsdaten, f"verkauf_{nummer}.pdf")

# Streamlit-Benutzeroberfläche
st.title("Verkäuferübersicht und PDF-Export")

# Verkäufernummer auswählen
verkaeufer_nummer = st.selectbox("Wähle Verkäufer", verkaeufer_df["Nummer"].tolist())

# Gefilterte Daten für den ausgewählten Verkäufer
verkaeufer_daten = verkaufsdaten_df[verkaufsdaten_df["Verkäufer"] == verkaeufer_nummer]

# PDF für den ausgewählten Verkäufer erstellen
if st.button("PDF für ausgewählten Verkäufer erstellen"):
    create_pdf(str(verkaeufer_nummer), verkaufsdaten_df, f"verkauf_{verkaeufer_nummer}.pdf")
    st.success(f"PDF für Verkäufer {verkaeufer_nummer} erstellt.")
    #st.markdown(f"[Hier herunterladen](verkauf_{verkaeufer_nummer}.pdf)")

# Alle PDFs für alle Verkäufer erstellen
if st.button("PDFs für alle Verkäufer erstellen"):
    create_pdfs_for_all(verkaufsdaten_df)
    st.success("PDFs für alle Verkäufer erstellt.")
    #st.markdown("[Hier herunterladen](verkauf_alle.zip)")


# Tabelle mit Verkäufen des ausgewählten Verkäufers
st.subheader(f"Verkäufe von Verkäufer {verkaeufer_nummer}")
st.dataframe(verkaeufer_daten)

# Alle Verkaufsdaten anzeigen
st.subheader("Alle Verkaufsdaten")
st.dataframe(verkaufsdaten_df)
