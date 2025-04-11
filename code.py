import streamlit as st

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Scheda Visita Immobile",
    page_icon=" Vistita Guidata Caslino Solfanuccio",
    layout="wide" # Utilizza l'intera larghezza dello schermo
)

# --- Struttura Dati Checklist ---
# Usiamo una lista di dizionari per definire sezioni e item.
# Ogni item ha un'etichetta (label) e chiavi uniche per punteggio e note in st.session_state
checklist_data = [
    {
        "section": "1. STATO GENERALE E MANUTENZIONE",
        "items": [
            {"label": "Qualità Ristrutturazione 2023", "key_score": "s1_q1_score", "key_notes": "s1_q1_notes", "hint": "Dettagli? Cosa rifatto? Documenti?"},
            {"label": "Stato Tetto (Visivo/Info)", "key_score": "s1_q2_score", "key_notes": "s1_q2_notes", "hint": "Tegole? Grondaie? Manutenzione?"},
            {"label": "Stato Facciata (Visivo/Info)", "key_score": "s1_q3_score", "key_notes": "s1_q3_notes", "hint": "Crepe? Intonaco? Umidità risalita?"},
            {"label": "Presenza Umidità/Muffa/Crepe", "key_score": "s1_q4_score", "key_notes": "s1_q4_notes", "hint": "Muri interni/esterni? Angoli? Bagni? Cantina? Odori?"},
            {"label": "Stato Infissi (Materiale, Età, Tenuta)", "key_score": "s1_q5_score", "key_notes": "s1_q5_notes", "hint": "Chiusura? Spifferi? Condensa? Materiale? Vetrocamera? Età?"},
            {"label": "Stato Pavimenti", "key_score": "s1_q6_score", "key_notes": "s1_q6_notes", "hint": "Usura? Livellamento? Materiali? Età?"},
            {"label": "Stato Pittura/Intonaco Interno", "key_score": "s1_q7_score", "key_notes": "s1_q7_notes", "hint": "Recente? Da rifare? Crepe superficiali?"},
        ]
    },
    {
        "section": "2. IMPIANTI",
        "items": [
            {"label": "Impianto Riscaldamento (Caldaia)", "key_score": "s2_q1_score", "key_notes": "s2_q1_notes", "hint": "Tipo? Età? Revisione? Libretto? Funziona?"},
            {"label": "Impianto Climatizzazione", "key_score": "s2_q2_score", "key_notes": "s2_q2_notes", "hint": "Split? Posizione? Età? Revisione?"},
            {"label": "Impianto Elettrico (Età, Conformità?)", "key_score": "s2_q3_score", "key_notes": "s2_q3_notes", "hint": "Recente? Prese? Punti luce? Dich. Conformità?"},
            {"label": "Impianto Idraulico (Età, Perdite?)", "key_score": "s2_q4_score", "key_notes": "s2_q4_notes", "hint": "Pressione acqua? Scarichi? Età? Perdite passate?"},
            {"label": "Pozzo (Uso, Funzionamento, Manut.)", "key_score": "s2_q5_score", "key_notes": "s2_q5_notes", "hint": "Irrigazione? Pompa ok? Manutenzione? Potabile?"},
            {"label": "Allaccio Fognatura Comunale?", "key_score": "s2_q6_score", "key_notes": "s2_q6_notes", "hint": "Confermare allaccio rete pubblica."},
        ]
    },
    {
        "section": "3. ASPETTI STRUTTURALI",
        "items": [
            {"label": "Segni Assestamento / Livello Pavimenti", "key_score": "s3_q1_score", "key_notes": "s3_q1_notes", "hint": "Pavimenti inclinati? Crepe strutturali? Porte/finestre?"},
            {"label": "Problemi Strutturali Passati? (Info)", "key_score": "s3_q2_score", "key_notes": "s3_q2_notes", "hint": "Interventi documentati? Chiedere."},
            {"label": "Modifiche Strutturali Autorizzate? (Info)", "key_score": "s3_q3_score", "key_notes": "s3_q3_notes", "hint": "Aggiunte/modifiche? Regolarizzate?"},
        ]
    },
    {
        "section": "4. ESTERNI E ACCESSORI",
        "items": [
            {"label": "Stato Giardino (ca. 1000mq)", "key_score": "s4_q1_score", "key_notes": "s4_q1_notes", "hint": "Manutenzione? Piante? Recinzione? Livellamento?"},
            {"label": "Parcheggio Comune (4 posti auto)", "key_score": "s4_q2_score", "key_notes": "s4_q2_notes", "hint": "Dove? Quanti garantiti? Regole? Costi? Accessibilità? Condiviso con chi?"},
            {"label": "Potenziale Annesso (Ricostruzione - Info)", "key_score": "s4_q3_score", "key_notes": "s4_q3_notes", "hint": "Dov'era? Dimensioni? Vincoli? Info proprietario."},
            {"label": "Condizioni Generali Esterne", "key_score": "s4_q4_score", "key_notes": "s4_q4_notes", "hint": "Muri cinta? Cancello? Illuminazione? Vialetti?"},
        ]
    },
     {
        "section": "5. EFFICIENZA ENERGETICA E COSTI",
        "items": [
            {"label": "Classe Energetica E (Verifica APE?)", "key_score": "s5_q1_score", "key_notes": "s5_q1_notes", "hint": "APE disponibile? Conferma kWh/m² anno?"},
            {"label": "Interventi Efficienza Energetica? (in ristr.)", "key_score": "s5_q2_score", "key_notes": "s5_q2_notes", "hint": "Cappotto? Infissi performanti? Tetto isolato?"},
            {"label": "Costi Utenze Medie Annuali? (Info)", "key_score": "s5_q3_score", "key_notes": "s5_q3_notes", "hint": "Chiedere stima Gas, Luce, Acqua."},
            {"label": "Costi Imposte Annuali? (IMU, TARI - Info)", "key_score": "s5_q4_score", "key_notes": "s5_q4_notes", "hint": "Chiedere importi indicativi."},
            {"label": "Spese Condivise / Straordinarie? (Info)", "key_score": "s5_q5_score", "key_notes": "s5_q5_notes", "hint": "Oltre parcheggio? Strada privata? Spese future zona?"},
        ]
    },
    {
        "section": "6. ZONA, CONTESTO E ASPETTI GENERALI",
        "items": [
            {"label": "Luminosità Naturale / Esposizione", "key_score": "s6_q1_score", "key_notes": "s6_q1_notes", "hint": "Stanze luminose? Orientamento?"},
            {"label": "Rumorosità Zona (Percepita/Info)", "key_score": "s6_q2_score", "key_notes": "s6_q2_notes", "hint": "Traffico? Vicini? Attività? Valutare/Chiedere."},
            {"label": "Qualità Vista Panoramica", "key_score": "s6_q3_score", "key_notes": "s6_q3_notes", "hint": "Corrisponde a descrizione? Ostacoli?"},
            {"label": "Vicinanza Servizi Essenziali (Info)", "key_score": "s6_q4_score", "key_notes": "s6_q4_notes", "hint": "Distanza reale negozi, farmacia, scuole? Auto indispensabile?"},
            {"label": "Qualità Connessione Internet? (Info)", "key_score": "s6_q5_score", "key_notes": "s6_q5_notes", "hint": "Tipo connessione? Velocità? Chiedere."},
            {"label": "Funzionalità Disposizione Interna", "key_score": "s6_q6_score", "key_notes": "s6_q6_notes", "hint": "Spazi ben distribuiti? Corridoi? Stanze sfruttabili?"},
            {"label": "Presenza Odori Particolari", "key_score": "s6_q7_score", "key_notes": "s6_q7_notes", "hint": "Muffa, chiuso, scarichi, fumo?"},
            {"label": "Arredamento Incluso? (Parziale - Info)", "key_score": "s6_q8_score", "key_notes": "s6_q8_notes", "hint": "Chiedere *esattamente* cosa rimane."},
            {"label": "Chiarimento Superficie (130 vs 174mq - Info)", "key_score": "s6_q9_score", "key_notes": "s6_q9_notes", "hint": "Dettaglio mq calpestabili/commerciali? Cosa sono i 174mq?"},
            {"label": "Motivazioni Vendita / Tempistiche? (Info)", "key_score": "s6_q10_score", "key_notes": "s6_q10_notes", "hint": "Da quanto in vendita? Perché? Disponibilità rogito? Trattabilità?"},
        ]
    }
    # Aggiungi qui altre sezioni se necessario
]

# --- Inizializzazione Session State ---
# Necessario per conservare i valori tra le interazioni
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    # Inizializza tutte le chiavi per punteggi e note
    for section in checklist_data:
        for item in section["items"]:
            st.session_state[item["key_score"]] = 3 # Default a 3 (Sufficiente)
            st.session_state[item["key_notes"]] = ""
    # Inizializza campi riepilogo
    st.session_state.punti_forza = ""
    st.session_state.criticita = ""
    st.session_state.impressione_generale = 3 # Default a 3
    st.session_state.prossimi_passi = ""
    st.session_state.data_visita = "" # Inizializza anche la data visita


# --- Titolo e Info Generali ---
st.title(" Scheda Valutazione Visita Immobile")
st.header("Casalino Solfanuccio")
st.markdown("**Indirizzo:** Via Umbria, San Costanzo (PU)")
st.markdown("**Prezzo Richiesto:** € 250.000")
st.text_input("Data Visita:", key="data_visita") # Usa text_input per la data

st.markdown("---")
st.markdown("**Legenda Punteggio:** `1`=Pessimo, `2`=Scarso, `3`=Sufficiente, `4`=Buono, `5`=Ottimo")
st.markdown("---")

# --- Generazione Dinamica Checklist ---
for section_data in checklist_data:
    with st.expander(f"**{section_data['section']}**", expanded=False): # Usa expander per compattare
        for item in section_data["items"]:
            st.markdown(f"**{item['label']}**")
            if "hint" in item:
                 st.caption(f"*{item['hint']}*") # Mostra il suggerimento

            # Layout a colonne per punteggio e note
            col1, col2 = st.columns([1, 2]) # Colonna note più larga

            with col1:
                # Usiamo st.radio orizzontale per il punteggio
                st.radio(
                    "Punteggio:",
                    options=[1, 2, 3, 4, 5],
                    key=item["key_score"],
                    horizontal=True,
                    label_visibility="collapsed" # Nasconde etichetta "Punteggio:"
                )

            with col2:
                # Usiamo st.text_area per le note
                st.text_area(
                    "Note:",
                    key=item["key_notes"],
                    height=50, # Altezza ridotta per compattezza
                     label_visibility="collapsed" # Nasconde etichetta "Note:"
                )
            st.markdown("---") # Divisore tra items

# --- Sezione Riepilogo Generale ---
st.markdown("---")
st.header("Riepilogo e Impressione Generale")

st.text_area("Punti di Forza Rilevati:", key="punti_forza", height=100)
st.text_area("Criticità / Dubbi Principali Rilevati:", key="criticita", height=100)

st.radio(
    "Punteggio Complessivo Impressione:",
    options=[1, 2, 3, 4, 5],
    key="impressione_generale",
    horizontal=True
)

st.text_area("Ulteriori Note / Prossimi Passi:", key="prossimi_passi", height=100)

# --- (Opzionale) Pulsante per Generare Riepilogo Testuale ---
st.markdown("---")
if st.button(" Mostra Riepilogo Testuale"):
    summary = []
    summary.append(f"# Riepilogo Visita: Casalino Solfanuccio")
    summary.append(f"**Data Visita:** {st.session_state.data_visita}")
    summary.append(f"**Prezzo Richiesto:** € 250.000")
    summary.append("\n---\n")

    for section_data in checklist_data:
        summary.append(f"## {section_data['section']}")
        for item in section_data["items"]:
            score = st.session_state[item["key_score"]]
            notes = st.session_state[item["key_notes"]]
            summary.append(f"- **{item['label']}:** Punteggio `{score}`")
            if notes:
                # Indenta le note per migliore leggibilità
                notes_indented = "\n  ".join(notes.strip().split('\n'))
                summary.append(f"  *Note:* {notes_indented}")
        summary.append("\n") # Spazio tra sezioni

    summary.append("## Riepilogo Generale")
    summary.append(f"**Punti di Forza:**\n{st.session_state.punti_forza}")
    summary.append(f"\n**Criticità / Dubbi:**\n{st.session_state.criticita}")
    summary.append(f"\n**Punteggio Complessivo:** `{st.session_state.impressione_generale}`")
    summary.append(f"\n**Prossimi Passi:**\n{st.session_state.prossimi_passi}")

    st.markdown("---")
    st.subheader("Riepilogo Completo (Markdown)")
    # Mostra il riepilogo in un'area di testo per copiarlo facilmente
    st.text_area("Copia questo riepilogo:", value="\n".join(summary), height=400)


# --- Nota sull'uso ---
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila i punteggi e le note durante o dopo la visita.
    2. I dati inseriti rimangono salvati nella sessione del browser finché non chiudi la scheda.
    3. Usa il pulsante "Mostra Riepilogo Testuale" per generare un report da copiare.

    **Deployment:**
    - Carica `app.py` e `requirements.txt` su un repository GitHub.
    - Collega il repository a Streamlit Community Cloud.
    """
)