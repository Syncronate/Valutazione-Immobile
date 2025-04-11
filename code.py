import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np # Necessario per calcolare la media ignorando None

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Scheda Visita Immobile",
    page_icon=" Vistita Guidata Caslino Solfanuccio", # Probabilmente volevi un'icona emoji qui, es. "🏠"
    layout="wide"
)

# --- Struttura Dati Checklist ---
# (Identica alla versione precedente)
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
]

# --- Inizializzazione Session State ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.expander_states = {} # <<< MODIFICA: Inizializza stato expander
    for i, section in enumerate(checklist_data):
        # <<< MODIFICA: Inizializza lo stato di ogni expander a chiuso (False)
        st.session_state.expander_states[section["section"]] = False
        for item in section["items"]:
            st.session_state[item["key_score"]] = 3 # Default a 3
            st.session_state[item["key_notes"]] = ""
    st.session_state.punti_forza = ""
    st.session_state.criticita = ""
    st.session_state.impressione_generale = 3
    st.session_state.prossimi_passi = ""
    st.session_state.data_visita = ""

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
             # Usare np.mean per gestire correttamente liste vuote o con None se necessario
             # Qui section_scores contiene solo numeri validi, quindi np.mean è sicuro
             avg = np.mean(section_scores)
        else:
            avg = 0 # O potresti usare None o np.nan se preferisci non mostrare 0
        averages[section_name] = avg
        labels.append(section_name.split('. ')[1]) # Prende il nome senza il numero
        scores.append(avg)
    return labels, scores, averages

# --- Titolo e Info Generali ---
st.title("Scheda Valutazione Visita Immobile")
st.header("Casalino Solfanuccio")
st.markdown("**Indirizzo:** Via Umbria, San Costanzo (PU)")
st.markdown("**Prezzo Richiesto:** € 250.000")
# Usa il valore da session_state per text_input
st.text_input("Data Visita:", key="data_visita") # Rimuovi value=..., key è sufficiente

st.markdown("---")
st.markdown("**Legenda Punteggio:** `1`=Pessimo, `2`=Scarso, `3`=Sufficiente, `4`=Buono, `5`=Ottimo")
st.markdown("---")

# --- Generazione Dinamica Checklist ---
for section_data in checklist_data:
    section_id = section_data["section"] # <<< MODIFICA: Identificatore unico per la sezione
    section_scores_list = [st.session_state.get(item["key_score"]) for item in section_data["items"] if isinstance(st.session_state.get(item["key_score"]), (int, float))]
    current_avg_str = f" (Media: {np.mean(section_scores_list):.1f})" if section_scores_list else ""

    # <<< MODIFICA: Usa lo stato salvato per 'expanded' e salva lo stato corrente
    # Leggi lo stato precedente dall' Msession_state
    initial_expanded_state = st.session_state.expander_states.get(section_id, False)

    # Crea l'expander e ottieni il suo stato *corrente* (se l'utente l'ha appena aperto/chiuso)
    is_expanded = st.expander(
        f"**{section_id}**{current_avg_str}",
        expanded=initial_expanded_state
    )

    # Aggiorna lo stato in session_state per il prossimo rerun
    st.session_state.expander_states[section_id] = is_expanded

    # Mostra il contenuto solo se l'expander è aperto
    if is_expanded:
        for item in section_data["items"]:
            st.markdown(f"**{item['label']}**")
            if "hint" in item:
                 st.caption(f"*{item['hint']}*")

            col1, col2 = st.columns([1, 2])

            with col1:
                # Non serve value=... se usi key in session_state
                st.radio(
                    "Punteggio:",
                    options=[1, 2, 3, 4, 5],
                    key=item["key_score"],
                    horizontal=True,
                    label_visibility="collapsed"
                )

            with col2:
                # Non serve value=... se usi key in session_state
                st.text_area(
                    "Note:",
                    key=item["key_notes"],
                    height=70,
                    label_visibility="collapsed"
                )
            st.markdown("---") # Separatore tra item all'interno dell'expander

# --- Sezione Riepilogo Generale ---
st.markdown("---") # Separatore prima del riepilogo
st.header("Riepilogo e Impressione Generale")

# Non serve value=... se usi key in session_state
st.text_area("Punti di Forza Rilevati:", key="punti_forza", height=100)
st.text_area("Criticità / Dubbi Principali Rilevati:", key="criticita", height=100)

st.radio(
    "Punteggio Complessivo Impressione:",
    options=[1, 2, 3, 4, 5],
    key="impressione_generale",
    horizontal=True
)

# Non serve value=... se usi key in session_state
st.text_area("Ulteriori Note / Prossimi Passi:", key="prossimi_passi", height=100)

# --- Sezione Grafica Riassuntiva ---
st.markdown("---") # Separatore prima dei grafici
st.header("Riepilogo Grafico")

section_labels, section_scores, section_averages_dict = calculate_section_averages(checklist_data)

# Controllo più robusto per la visualizzazione dei grafici
if not section_labels or not any(s is not None and s > 0 for s in section_scores):
    st.warning("Inserisci almeno un punteggio (maggiore di 0) per generare i grafici.")
else:
    # Pulisci i dati per i grafici (sostituisci eventuali None con 0 o valori piccoli)
    # Nota: la funzione calculate_section_averages già restituisce 0 per sezioni senza punteggi
    valid_scores_radar = [max(s, 0.1) if s is not None else 0.1 for s in section_scores] # Usa 0.1 per visibilità radar minima
    valid_scores_bar = [s if s is not None else 0 for s in section_scores]

    # 1. Grafico Radar
    fig_radar = go.Figure()
    # Assicurati che ci sia almeno un punto per il radar
    if valid_scores_radar:
        fig_radar.add_trace(go.Scatterpolar(
            r=valid_scores_radar + [valid_scores_radar[0]], # Chiudi il radar
            theta=section_labels + [section_labels[0]],    # Chiudi il radar
            fill='toself',
            name='Punteggio Medio'
        ))
        fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, 5] # Mantiene il range fisso
            )),
        showlegend=False,
        title="Punteggio Medio per Sezione (Radar)"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
         st.info("Nessun dato valido per il grafico Radar.")

    # 2. Grafico a Barre
    # Assicurati che ci siano dati validi
    if any(s > 0 for s in valid_scores_bar):
        fig_bar = px.bar(
            x=section_labels,
            y=valid_scores_bar,
            title="Punteggio Medio per Sezione (Barre)",
            labels={'x': 'Sezione', 'y': 'Punteggio Medio'},
            text_auto='.1f' # Formatta il testo sulla barra
        )
        fig_bar.update_layout(yaxis_range=[0, 5]) # Mantiene il range fisso
        fig_bar.update_traces(textposition='outside') # Mostra il testo sopra la barra
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Nessun dato valido per il grafico a Barre.")


# --- Pulsante Riepilogo Testuale ---
st.markdown("---")
if st.button("Mostra Riepilogo Testuale Completo"):
    summary = []
    summary.append(f"# Riepilogo Visita: Casalino Solfanuccio")
    summary.append(f"**Data Visita:** {st.session_state.get('data_visita', 'N/D')}") # Usa .get per sicurezza
    summary.append(f"**Prezzo Richiesto:** € 250.000")
    summary.append("\n---\n")

    # Usa i dati calcolati (se disponibili)
    if section_labels and section_scores:
        summary.append("## Punteggi Medi per Sezione:")
        for label, score in zip(section_labels, section_scores):
             summary.append(f"- **{label}:** {score:.1f}" if score is not None else f"- **{label}:** N/D")
        summary.append("\n---\n")
    else:
        summary.append("## Punteggi Medi per Sezione:\nNessun punteggio inserito.")
        summary.append("\n---\n")


    for section_data in checklist_data:
        summary.append(f"## {section_data['section']}")
        for item in section_data["items"]:
            score = st.session_state.get(item["key_score"], 'N/D')
            notes = st.session_state.get(item["key_notes"], '').strip()
            # Gestione più pulita del punteggio
            score_str = f"`{score}`" if isinstance(score, (int, float)) else "`N/D`"
            summary.append(f"- **{item['label']}:** Punteggio {score_str}")
            if notes:
                # Indenta correttamente le note multiline
                notes_indented = "\n    ".join(notes.split('\n'))
                summary.append(f"  *Note:*\n    {notes_indented}") # Usa > per blockquote o indentazione
        summary.append("\n") # Spazio tra le sezioni

    summary.append("## Riepilogo Generale")
    summary.append(f"**Punti di Forza:**\n{st.session_state.get('punti_forza', '')}")
    summary.append(f"\n**Criticità / Dubbi:**\n{st.session_state.get('criticita', '')}")
    summary.append(f"\n**Punteggio Complessivo:** `{st.session_state.get('impressione_generale', 'N/D')}`")
    summary.append(f"\n**Prossimi Passi:**\n{st.session_state.get('prossimi_passi', '')}")

    st.markdown("---")
    st.subheader("Riepilogo Completo (Markdown)")
    st.text_area("Copia questo riepilogo:", value="\n".join(summary), height=500) # Aumentato altezza


# --- Nota sull'uso ---
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila i punteggi e le note nelle sezioni. L'expander rimarrà aperto.
    2. Visualizza i grafici riassuntivi aggiornati.
    3. Usa "Mostra Riepilogo Testuale Completo" per il report dettagliato da copiare.
    """
)

# Aggiungo un piccolo spazio alla fine per evitare che l'ultimo elemento sia attaccato al fondo
st.markdown("")
