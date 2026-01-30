import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
from datetime import datetime
import uuid
import os

# Initialisierung
if 'verkaufsdaten' not in st.session_state:
    st.session_state.verkaufsdaten = []
if 'belegenummer' not in st.session_state:
    st.session_state.belegenummer = str(uuid.uuid4())[:8]
if 'verkaeufer_input' not in st.session_state:
    st.session_state['verkaeufer_input'] = ""
if 'preis_input' not in st.session_state:
    st.session_state['preis_input'] = 0.01  # min_value beachten!

st.title("🧾 Kassensystem")

# Eingabeformular
with st.form(key='eingabe_form', clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        verkaeufer = st.text_input("Verkäufernummer", key="verkaeufer_input")
    with col2:
        preis = st.number_input("Preis (€)", min_value=0.01, step=0.01, format="%.2f", key="preis_input")

    submitted = st.form_submit_button("Hinzufügen")

    if submitted and verkaeufer and preis:
        verkaeufer_4stellig = verkaeufer.zfill(4)
        st.session_state.verkaufsdaten.append({
            "Uhrzeit": datetime.now().strftime("%H:%M:%S"),
            "Belegenummer": st.session_state.belegenummer,
            "Verkäufer": verkaeufer_4stellig,
            "Preis": preis
        })
        st.rerun()


# Aktuellen Beleg anzeigen
df = pd.DataFrame(st.session_state.verkaufsdaten)


selected = []
if not df.empty:
    st.write(f"**Gesamtsumme:** {df['Preis'].sum():.2f} €")


    if st.button("💾 Verkauf abschließen und speichern"):
        df['Datum'] = datetime.now().strftime("%Y-%m-%d")
        dateipfad = os.path.join("belege", f"beleg_{st.session_state.belegenummer}.csv")
        df.to_csv(dateipfad, index=False)
        st.success(f"Beleg {st.session_state.belegenummer} gespeichert.")
        # Zurücksetzen
        st.session_state.verkaufsdaten = []
        st.session_state.belegenummer = str(uuid.uuid4())[:8]
        st.rerun()

    st.write("Aktueller Beleg")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=250,
        key='grid'
    )

    selected = grid_response['selected_rows']
 
    if str(type(selected)) =="<class 'NoneType'>":
        st.warning("Keine Zeile ausgewählt!")
    else:
        if st.button("❌ Entferne ausgewählte Zeile"):
            selected_row = selected.iloc[0]  # funktioniert auch bei String-Index
            # Zeile aus df löschen
            df = df[~(
                (df['Uhrzeit'] == selected_row['Uhrzeit']) &
                (df['Verkäufer'] == selected_row['Verkäufer']) &
                (df['Preis'] == selected_row['Preis'])
            )]
            # session_state aktualisieren
            st.session_state.verkaufsdaten = df.to_dict('records')
            st.success("Zeile erfolgreich gelöscht.")
            st.rerun()

