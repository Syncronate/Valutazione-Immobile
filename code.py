import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Scheda Visita Immobile",
    page_icon=" Vistita Guidata Caslino Solfanuccio",
    layout="wide"
)

# --- Struttura Dati Checklist (COMPLETA) ---
checklist_data = [
    {
        "section": "1. STATO GENERALE E MANUTENZIONE", # Chiave univoca
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
        "section": "2. IMPIANTI", # Chiave univoca
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
        "section": "3. ASPETTI STRUTTURALI", # Chiave univoca
        "items": [
            {"label": "Segni Assestamento / Livello Pavimenti", "key_score": "s3_q1_score", "key_notes": "s3_q1_notes", "hint": "Pavimenti inclinati? Crepe strutturali? Porte/finestre?"},
            {"label": "Problemi Strutturali Passati? (Info)", "key_score": "s3_q2_score", "key_notes": "s3_q2_notes", "hint": "Interventi documentati? Chiedere."},
            {"label": "Modifiche Strutturali Autorizzate? (Info)", "key_score": "s3_q3_score", "key_notes": "s3_q3_notes", "hint": "Aggiunte/modifiche? Regolarizzate?"},
        ]
    },
    {
        "section": "4. ESTERNI E ACCESSORI", # Chiave univoca
        "items": [
            {"label": "Stato Giardino (ca. 1000mq)", "key_score": "s4_q1_score", "key_notes": "s4_q1_notes", "hint": "Manutenzione? Piante? Recinzione? Livellamento?"},
            {"label": "Parcheggio Comune (4 posti auto)", "key_score": "s4_q2_score", "key_notes": "s4_q2_notes", "hint": "Dove? Quanti garantiti? Regole? Costi? Accessibilità? Condiviso con chi?"},
            {"label": "Potenziale Annesso (Ricostruzione - Info)", "key_score": "s4_q3_score", "key_notes": "s4_q3_notes", "hint": "Dov'era? Dimensioni? Vincoli? Info proprietario."},
            {"label": "Condizioni Generali Esterne", "key_score": "s4_q4_score", "key_notes": "s4_q4_notes", "hint": "Muri cinta? Cancello? Illuminazione? Vialetti?"},
        ]
    },
     {
        "section": "5. EFFICIENZA ENERGETICA E COSTI", # Chiave univoca
        "items": [
            {"label": "Classe Energetica E (Verifica APE?)", "key_score": "s5_q1_score", "key_notes": "s5_q1_notes", "hint": "APE disponibile? Conferma kWh/m² anno?"},
            {"label": "Interventi Efficienza Energetica? (in ristr.)", "key_score": "s5_q2_score", "key_notes": "s5_q2_notes", "hint": "Cappotto? Infissi performanti? Tetto isolato?"},
            {"label": "Costi Utenze Medie Annuali? (Info)", "key_score": "s5_q3_score", "key_notes": "s5_q3_notes", "hint": "Chiedere stima Gas, Luce, Acqua."},
            {"label": "Costi Imposte Annuali? (IMU, TARI - Info)", "key_score": "s5_q4_score", "key_notes": "s5_q4_notes", "hint": "Chiedere importi indicativi."},
            {"label": "Spese Condivise / Straordinarie? (Info)", "key_score": "s5_q5_score", "key_notes": "s5_q5_notes", "hint": "Oltre parcheggio? Strada privata? Spese future zona?"},
        ]
    },
    {
        "section": "6. ZONA, CONTESTO E ASPETTI GENERALI", # Chiave univoca
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
]


# --- Inizializzazione Session State ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.active_section = None # Traccia la sezione attiva
    for section in checklist_data:
        for item in section["items"]:
            st.session_state[item["key_score"]] = 3
            st.session_state[item["key_notes"]] = ""
    st.session_state.punti_forza = ""
    st.session_state.criticita = ""
    st.session_state.impressione_generale = 3
    st.session_state.prossimi_passi = ""
    st.session_state.data_visita = ""


# --- Funzione Callback per Mantenere Aperto Expander ---
def set_active_section(section_key):
    """Imposta la sezione attiva nello stato della sessione."""
    st.session_state.active_section = section_key

# --- Funzione per Calcolare Medie Sezioni ---
def calculate_section_averages(data):
    averages = {}
    labels = []
    scores = []
    for section_data in data:
        section_name = section_data["section"]
        section_scores = []
        for item in section_data["items"]:
            score = st.session_state.get(item["key_score"], None)
            if isinstance(score, (int, float)):
                 section_scores.append(score)

        if section_scores:
             avg = np.mean(section_scores)
        else:
            avg = 0
        averages[section_name] = avg
        label_name = section_name.split('. ')[1] if '. ' in section_name else section_name
        labels.append(label_name)
        scores.append(avg)
    return labels, scores, averages


# --- Titolo e Info Generali ---
st.title(" Scheda Valutazione Visita Immobile")
st.header("Casalino Solfanuccio")
st.markdown("**Indirizzo:** Via Umbria, San Costanzo (PU)")
st.markdown("**Prezzo Richiesto:** € 250.000")
st.text_input("Data Visita:", key="data_visita", value=st.session_state.data_visita)

st.markdown("---")
st.markdown("**Legenda Punteggio:** `1`=Pessimo, `2`=Scarso, `3`=Sufficiente, `4`=Buono, `5`=Ottimo")
st.markdown("---")

# --- Generazione Dinamica Checklist ---
for section_data in checklist_data:
    section_key = section_data["section"]

    section_scores_list = [st.session_state.get(item["key_score"]) for item in section_data["items"] if isinstance(st.session_state.get(item["key_score"]), (int, float))]
    current_avg_str = f" (Media: {np.mean(section_scores_list):.1f})" if section_scores_list else ""

    is_expanded = (st.session_state.get("active_section") == section_key)

    with st.expander(f"**{section_key}**{current_avg_str}", expanded=is_expanded):
        for item in section_data["items"]:
            st.markdown(f"**{item['label']}**")
            if "hint" in item:
                 st.caption(f"*{item['hint']}*")

            col1, col2 = st.columns([1, 2])

            with col1:
                st.radio(
                    "Punteggio:",
                    options=[1, 2, 3, 4, 5],
                    key=item["key_score"],
                    horizontal=True,
                    label_visibility="collapsed",
                    on_change=set_active_section,
                    args=(section_key,)
                )

            with col2:
                st.text_area(
                    "Note:",
                    key=item["key_notes"],
                    value=st.session_state[item["key_notes"]],
                    height=70,
                    label_visibility="collapsed",
                    on_change=set_active_section,
                    args=(section_key,)
                )
            st.markdown("---")

# --- Sezione Riepilogo Generale ---
st.markdown("---")
st.header("Riepilogo e Impressione Generale")
st.text_area("Punti di Forza Rilevati:", key="punti_forza", value=st.session_state.punti_forza, height=100)
st.text_area("Criticità / Dubbi Principali Rilevati:", key="criticita", value=st.session_state.criticita, height=100)
st.radio(
    "Punteggio Complessivo Impressione:",
    options=[1, 2, 3, 4, 5],
    key="impressione_generale",
    horizontal=True
)
st.text_area("Ulteriori Note / Prossimi Passi:", key="prossimi_passi", value=st.session_state.prossimi_passi, height=100)


# --- Sezione Grafica Riassuntiva ---
st.markdown("---")
st.header(" Riepilogo Grafico")
section_labels, section_scores, section_averages_dict = calculate_section_averages(checklist_data)
if not section_labels or not any(s > 0 for s in section_scores):
    st.warning("Inserisci almeno un punteggio per generare i grafici.")
else:
    # Grafico Radar
    fig_radar = go.Figure()
    valid_scores_radar = [s if s > 0 else 0.1 for s in section_scores]
    fig_radar.add_trace(go.Scatterpolar(
          r=valid_scores_radar + [valid_scores_radar[0]],
          theta=section_labels + [section_labels[0]],
          fill='toself',
          name='Punteggio Medio'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 5])), showlegend=False, title="Punteggio Medio per Sezione (Radar)")
    st.plotly_chart(fig_radar, use_container_width=True)
    # Grafico a Barre
    fig_bar = px.bar(x=section_labels, y=section_scores, title="Punteggio Medio per Sezione (Barre)", labels={'x': 'Sezione', 'y': 'Punteggio Medio'}, text_auto='.1f')
    fig_bar.update_layout(yaxis_range=[0, 5])
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)


# --- Pulsante Riepilogo Testuale ---
st.markdown("---")
if st.button(" Mostra Riepilogo Testuale Completo"):
    summary = []
    summary.append(f"# Riepilogo Visita: Casalino Solfanuccio")
    summary.append(f"**Data Visita:** {st.session_state.data_visita}")
    summary.append(f"**Prezzo Richiesto:** € 250.000")
    summary.append("\n---\n")
    summary.append("## Punteggi Medi per Sezione:")
    labels_from_avg, scores_from_avg, _ = calculate_section_averages(checklist_data)
    for label, score in zip(labels_from_avg, scores_from_avg):
         summary.append(f"- **{label}:** {score:.1f}")
    summary.append("\n---\n")
    for section_data in checklist_data:
        summary.append(f"## {section_data['section']}")
        for item in section_data["items"]:
            score = st.session_state.get(item["key_score"], 'N/D')
            notes = st.session_state.get(item["key_notes"], '')
            score_str = f"`{score}`" if isinstance(score, (int, float)) else f"`{score}`"
            summary.append(f"- **{item['label']}:** Punteggio {score_str}")
            if notes:
                notes_indented = "\n  ".join(notes.strip().split('\n'))
                summary.append(f"  *Note:* {notes_indented}")
        summary.append("\n")
    summary.append("## Riepilogo Generale")
    summary.append(f"**Punti di Forza:**\n{st.session_state.punti_forza}")
    summary.append(f"\n**Criticità / Dubbi:**\n{st.session_state.criticita}")
    summary.append(f"\n**Punteggio Complessivo:** `{st.session_state.impressione_generale}`")
    summary.append(f"\n**Prossimi Passi:**\n{st.session_state.prossimi_passi}")
    st.markdown("---")
    st.subheader("Riepilogo Completo (Markdown)")
    st.text_area("Copia questo riepilogo:", value="\n".join(summary), height=400)


# --- Nota sull'uso ---
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila i punteggi e le note. La sezione attiva rimarrà aperta.
    2. Visualizza i grafici riassuntivi.
    3. Usa "Mostra Riepilogo Testuale Completo" per il report dettagliato.
    """
)
