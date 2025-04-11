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

# --- Struttura Dati Checklist (COMPLETA con help_text) ---
# (Identica alla versione precedente)
checklist_data = [
    {
        "section": "1. STATO GENERALE E MANUTENZIONE",
        "items": [
            {"label": "Qualità Ristrutturazione 2023", "key_score": "s1_q1_score", "key_notes": "s1_q1_notes", "hint": "Dettagli? Cosa rifatto? Documenti?", "help_text": "Chiedere nel dettaglio cosa è stato rinnovato..."},
            {"label": "Stato Tetto (Visivo/Info)", "key_score": "s1_q2_score", "key_notes": "s1_q2_notes", "hint": "Tegole? Grondaie? Manutenzione?", "help_text": "Ispezionare visivamente o chiedere: Tegole rotte/mancanti?..."},
            {"label": "Stato Facciata (Visivo/Info)", "key_score": "s1_q3_score", "key_notes": "s1_q3_notes", "hint": "Crepe? Intonaco? Umidità risalita?", "help_text": "Osservare: Crepe evidenti? Intonaco scrostato?..."},
            {"label": "Presenza Umidità/Muffa/Crepe", "key_score": "s1_q4_score", "key_notes": "s1_q4_notes", "hint": "Muri interni/esterni? Angoli? Bagni? Cantina? Odori?", "help_text": "Controllare attentamente angoli, muri perimetrali..."},
            {"label": "Stato Infissi (Materiale, Età, Tenuta)", "key_score": "s1_q5_score", "key_notes": "s1_q5_notes", "hint": "Chiusura? Spifferi? Condensa? Materiale? Vetrocamera? Età?", "help_text": "Aprire e chiudere finestre/porte: Si muovono agevolmente?..."},
            {"label": "Stato Pavimenti", "key_score": "s1_q6_score", "key_notes": "s1_q6_notes", "hint": "Usura? Livellamento? Materiali? Età?", "help_text": "Camminare su tutta la superficie: Ci sono punti in cui scricchiola?..."},
            {"label": "Stato Pittura/Intonaco Interno", "key_score": "s1_q7_score", "key_notes": "s1_q7_notes", "hint": "Recente? Da rifare? Crepe superficiali?", "help_text": "Valutare lo stato generale della tinteggiatura..."},
        ]
    },
    {
        "section": "2. IMPIANTI",
        "items": [
             {"label": "Impianto Riscaldamento (Caldaia)", "key_score": "s2_q1_score", "key_notes": "s2_q1_notes", "hint": "Tipo? Età? Revisione? Libretto? Funziona?", "help_text": "Chiedere: Che tipo di caldaia è?..."},
             {"label": "Impianto Climatizzazione", "key_score": "s2_q2_score", "key_notes": "s2_q2_notes", "hint": "Split? Posizione? Età? Revisione?", "help_text": "Quanti split ci sono?..."},
             {"label": "Impianto Elettrico (Età, Conformità?)", "key_score": "s2_q3_score", "key_notes": "s2_q3_notes", "hint": "Recente? Prese? Punti luce? Dich. Conformità?", "help_text": "L'impianto sembra recente?..."},
             {"label": "Impianto Idraulico (Età, Perdite?)", "key_score": "s2_q4_score", "key_notes": "s2_q4_notes", "hint": "Pressione acqua? Scarichi? Età? Perdite passate?", "help_text": "Aprire i rubinetti: la pressione è buona?..."},
             {"label": "Pozzo (Uso, Funzionamento, Manut.)", "key_score": "s2_q5_score", "key_notes": "s2_q5_notes", "hint": "Irrigazione? Pompa ok? Manutenzione? Potabile?", "help_text": "A cosa serve il pozzo?..."},
             {"label": "Allaccio Fognatura Comunale?", "key_score": "s2_q6_score", "key_notes": "s2_q6_notes", "hint": "Confermare allaccio rete pubblica.", "help_text": "Chiedere conferma allaccio rete fognaria comunale..."},
        ]
    },
    {
        "section": "3. ASPETTI STRUTTURALI",
         "items": [
            {"label": "Segni Assestamento / Livello Pavimenti", "key_score": "s3_q1_score", "key_notes": "s3_q1_notes", "hint": "Pavimenti inclinati? Crepe strutturali? Porte/finestre?", "help_text": "Osservare attentamente se i pavimenti sono inclinati..."},
            {"label": "Problemi Strutturali Passati? (Info)", "key_score": "s3_q2_score", "key_notes": "s3_q2_notes", "hint": "Interventi documentati? Chiedere.", "help_text": "Chiedere esplicitamente se ci sono stati problemi strutturali..."},
            {"label": "Modifiche Strutturali Autorizzate? (Info)", "key_score": "s3_q3_score", "key_notes": "s3_q3_notes", "hint": "Aggiunte/modifiche? Regolarizzate?", "help_text": "Sono state apportate modifiche strutturali?..."},
        ]
    },
    {
        "section": "4. ESTERNI E ACCESSORI",
        "items": [
            {"label": "Stato Giardino (ca. 1000mq)", "key_score": "s4_q1_score", "key_notes": "s4_q1_notes", "hint": "Manutenzione? Piante? Recinzione? Livellamento?", "help_text": "Valutare lo stato di manutenzione generale del giardino..."},
            {"label": "Parcheggio Comune (4 posti auto)", "key_score": "s4_q2_score", "key_notes": "s4_q2_notes", "hint": "Dove? Quanti garantiti? Regole? Costi? Accessibilità? Condiviso con chi?", "help_text": "Chiedere con precisione: Dove si trovano i posti auto?..."},
            {"label": "Potenziale Annesso (Ricostruzione - Info)", "key_score": "s4_q3_score", "key_notes": "s4_q3_notes", "hint": "Dov'era? Dimensioni? Vincoli? Info proprietario.", "help_text": "Chiedere dove si trovava l'annesso originale..."},
            {"label": "Condizioni Generali Esterne", "key_score": "s4_q4_score", "key_notes": "s4_q4_notes", "hint": "Muri cinta? Cancello? Illuminazione? Vialetti?", "help_text": "Valutare lo stato di eventuali muri di cinta..."},
        ]
    },
    {
        "section": "5. EFFICIENZA ENERGETICA E COSTI",
        "items": [
            {"label": "Classe Energetica E (Verifica APE?)", "key_score": "s5_q1_score", "key_notes": "s5_q1_notes", "hint": "APE disponibile? Conferma kWh/m² anno?", "help_text": "Chiedere se è disponibile l'Attestato di Prestazione Energetica (APE)..."},
            {"label": "Interventi Efficienza Energetica? (in ristr.)", "key_score": "s5_q2_score", "key_notes": "s5_q2_notes", "hint": "Cappotto? Infissi performanti? Tetto isolato?", "help_text": "Durante la ristrutturazione del 2023 sono stati fatti interventi specifici?..."},
            {"label": "Costi Utenze Medie Annuali? (Info)", "key_score": "s5_q3_score", "key_notes": "s5_q3_notes", "hint": "Chiedere stima Gas, Luce, Acqua.", "help_text": "Chiedere al proprietario una stima dei costi annuali o mensili..."},
            {"label": "Costi Imposte Annuali? (IMU, TARI - Info)", "key_score": "s5_q4_score", "key_notes": "s5_q4_notes", "hint": "Chiedere importi indicativi.", "help_text": "Chiedere l'importo approssimativo dell'IMU..."},
            {"label": "Spese Condivise / Straordinarie? (Info)", "key_score": "s5_q5_score", "key_notes": "s5_q5_notes", "hint": "Oltre parcheggio? Strada privata? Spese future zona?", "help_text": "Ci sono altre spese condivise con vicini?..."},
        ]
    },
    {
        "section": "6. ZONA, CONTESTO E ASPETTI GENERALI",
        "items": [
            {"label": "Luminosità Naturale / Esposizione", "key_score": "s6_q1_score", "key_notes": "s6_q1_notes", "hint": "Stanze luminose? Orientamento?", "help_text": "Valutare la luminosità naturale nelle diverse stanze..."},
            {"label": "Rumorosità Zona (Percepita/Info)", "key_score": "s6_q2_score", "key_notes": "s6_q2_notes", "hint": "Traffico? Vicini? Attività? Valutare/Chiedere.", "help_text": "Durante la visita, prestare attenzione ai rumori esterni..."},
            {"label": "Qualità Vista Panoramica", "key_score": "s6_q3_score", "key_notes": "s6_q3_notes", "hint": "Corrisponde a descrizione? Ostacoli?", "help_text": "La vista panoramica descritta nell'annuncio corrisponde?..."},
            {"label": "Vicinanza Servizi Essenziali (Info)", "key_score": "s6_q4_score", "key_notes": "s6_q4_notes", "hint": "Distanza reale negozi, farmacia, scuole? Auto indispensabile?", "help_text": "Chiedere o verificare la distanza effettiva..."},
            {"label": "Qualità Connessione Internet? (Info)", "key_score": "s6_q5_score", "key_notes": "s6_q5_notes", "hint": "Tipo connessione? Velocità? Chiedere.", "help_text": "Chiedere che tipo di connessione internet è disponibile..."},
            {"label": "Funzionalità Disposizione Interna", "key_score": "s6_q6_score", "key_notes": "s6_q6_notes", "hint": "Spazi ben distribuiti? Corridoi? Stanze sfruttabili?", "help_text": "Valutare se la disposizione degli spazi è funzionale..."},
            {"label": "Presenza Odori Particolari", "key_score": "s6_q7_score", "key_notes": "s6_q7_notes", "hint": "Muffa, chiuso, scarichi, fumo?", "help_text": "Prestare attenzione a eventuali odori sgradevoli..."},
            {"label": "Arredamento Incluso? (Parziale - Info)", "key_score": "s6_q8_score", "key_notes": "s6_q8_notes", "hint": "Chiedere *esattamente* cosa rimane.", "help_text": "L'annuncio indica 'parzialmente arredato'. Chiedere lista precisa..."},
            {"label": "Chiarimento Superficie (130 vs 174mq - Info)", "key_score": "s6_q9_score", "key_notes": "s6_q9_notes", "hint": "Dettaglio mq calpestabili/commerciali? Cosa sono i 174mq?", "help_text": "Chiedere chiarimenti sulla discrepanza tra superficie commerciale..."},
            {"label": "Motivazioni Vendita / Tempistiche? (Info)", "key_score": "s6_q10_score", "key_notes": "s6_q10_notes", "hint": "Da quanto in vendita? Perché? Disponibilità rogito? Trattabilità?", "help_text": "Chiedere (con tatto) da quanto tempo l'immobile è in vendita..."},
        ]
    }
]


# --- NUOVA Struttura Dati per Valutazione Stanze ---
room_evaluation_data = [
    {"name": "Soggiorno/Cucina (PT)", "key_score": "room_sogg_score", "key_notes": "room_sogg_notes", "help": "Valuta condizioni generali, finiture, luminosità, prese, segni di usura specifici di questa stanza."},
    {"name": "Bagno/Lavanderia (PT)", "key_score": "room_bagno_pt_score", "key_notes": "room_bagno_pt_notes", "help": "Valuta sanitari, rubinetteria, scarichi, piastrelle, finestra (se presente), presenza muffa, spazio lavatrice."},
    {"name": "Camera Matrimoniale (PT)", "key_score": "room_cam_pt_score", "key_notes": "room_cam_pt_notes", "help": "Valuta dimensioni, luminosità, disposizione prese, condizioni pavimento/pareti, infissi."},
    {"name": "Camera 1 (P1)", "key_score": "room_cam1_p1_score", "key_notes": "room_cam1_p1_notes", "help": "Valuta dimensioni, luminosità, disposizione prese, condizioni pavimento/pareti, infissi."},
    {"name": "Camera 2 (P1)", "key_score": "room_cam2_p1_score", "key_notes": "room_cam2_p1_notes", "help": "Valuta dimensioni, luminosità, disposizione prese, condizioni pavimento/pareti, infissi."},
    {"name": "Bagno (P1)", "key_score": "room_bagno_p1_score", "key_notes": "room_bagno_p1_notes", "help": "Valuta sanitari, rubinetteria, scarichi, doccia/vasca, piastrelle, finestra (se presente), presenza muffa."},
    {"name": "Cantina (Ex Ingresso PT)", "key_score": "room_cantina_pt_score", "key_notes": "room_cantina_pt_notes", "help": "Valuta dimensioni, umidità, illuminazione, accessibilità, potenziale utilizzo."},
    # Puoi aggiungere altre stanze se necessario, es:
    # {"name": "Corridoio/Disimpegno", "key_score": "room_corr_score", "key_notes": "room_corr_notes", "help": "Valuta larghezza, illuminazione, stato pareti."},
]

# --- Inizializzazione Session State ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.active_section = None # Traccia la sezione checklist attiva

    # Inizializza checklist
    for section in checklist_data:
        for item in section["items"]:
            st.session_state[item["key_score"]] = 3
            st.session_state[item["key_notes"]] = ""

    # NUOVO: Inizializza valutazione stanze
    for room in room_evaluation_data:
        st.session_state[room["key_score"]] = 3
        st.session_state[room["key_notes"]] = ""

    # Inizializza riepilogo
    st.session_state.punti_forza = ""
    st.session_state.criticita = ""
    st.session_state.impressione_generale = 3
    st.session_state.prossimi_passi = ""
    st.session_state.data_visita = ""


# --- Funzione Callback per Mantenere Aperto Expander ---
def set_active_section(section_key):
    st.session_state.active_section = section_key

# --- Funzione per Calcolare Medie Sezioni Checklist ---
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

# --- NUOVA Funzione per ottenere dati stanze per grafici ---
def get_room_scores(room_data):
    labels = []
    scores = []
    for room in room_data:
        score = st.session_state.get(room["key_score"], None)
        if isinstance(score, (int, float)):
            labels.append(room["name"])
            scores.append(score)
        # else: # Opzionale: includere anche se non valutato con score 0 o NaN
        #     labels.append(room["name"])
        #     scores.append(0) # o np.nan
    return labels, scores


# --- Titolo e Info Generali ---
# (Invariato)
st.title(" Scheda Valutazione Visita Immobile")
st.header("Casalino Solfanuccio")
st.markdown("**Indirizzo:** Via Umbria, San Costanzo (PU)")
st.markdown("**Prezzo Richiesto:** € 250.000")
st.text_input("Data Visita:", key="data_visita", value=st.session_state.data_visita)
st.markdown("---")
st.markdown("**Legenda Punteggio:** `1`=Pessimo, `2`=Scarso, `3`=Sufficiente, `4`=Buono, `5`=Ottimo")
st.markdown("---")


# --- Generazione Dinamica Checklist (Sezioni Tematiche) ---
st.subheader("Valutazione Aspetti Generali (Checklist)")
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
                    # label_visibility="collapsed", # Rimosso per far vedere l'help
                    on_change=set_active_section,
                    args=(section_key,),
                    help=item.get("help_text")
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

# --- NUOVA Sezione Valutazione Stanze Specifiche ---
st.markdown("---")
st.subheader("Valutazione Stanze Specifiche")
for room in room_evaluation_data:
    st.markdown(f"**{room['name']}**")
    col1_room, col2_room = st.columns([1, 2])

    with col1_room:
        st.radio(
            "Punteggio Stanza:",
            options=[1, 2, 3, 4, 5],
            key=room["key_score"],
            horizontal=True,
            label_visibility="collapsed", # Qui possiamo collassare, l'help è sul nome
            help=room.get("help") # Usiamo la chiave "help" definita in room_evaluation_data
        )

    with col2_room:
        st.text_area(
            f"Note per {room['name']}:",
            key=room["key_notes"],
            value=st.session_state[room["key_notes"]],
            height=70,
            label_visibility="collapsed"
        )
    st.markdown("---") # Separatore tra stanze


# --- Sezione Riepilogo Generale ---
# (Invariato)
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


# --- Sezione Grafica Riassuntiva (Aggiornata) ---
st.markdown("---")
st.header(" Riepilogo Grafico")

# Grafico Checklist
st.markdown("#### Punteggi Medi per Sezione (Checklist)")
section_labels, section_scores, section_averages_dict = calculate_section_averages(checklist_data)
if not section_labels or not any(s > 0 for s in section_scores):
    st.warning("Inserisci punteggi nella checklist per generare i grafici relativi.")
else:
    fig_radar = go.Figure()
    valid_scores_radar = [s if s > 0 else 0.1 for s in section_scores]
    fig_radar.add_trace(go.Scatterpolar(r=valid_scores_radar + [valid_scores_radar[0]], theta=section_labels + [section_labels[0]], fill='toself', name='Punteggio Medio'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 5])), showlegend=False, title="Checklist: Punteggio Medio Sezioni (Radar)")
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_bar = px.bar(x=section_labels, y=section_scores, title="Checklist: Punteggio Medio Sezioni (Barre)", labels={'x': 'Sezione', 'y': 'Punteggio Medio'}, text_auto='.1f')
    fig_bar.update_layout(yaxis_range=[0, 5])
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

# NUOVO Grafico Stanze
st.markdown("---")
st.markdown("#### Punteggi Stanze Specifiche")
room_labels, room_scores = get_room_scores(room_evaluation_data)
if not room_labels or not any(s > 0 for s in room_scores):
     st.warning("Inserisci punteggi nelle stanze per generare il grafico relativo.")
else:
    fig_bar_rooms = px.bar(
        x=room_labels,
        y=room_scores,
        title="Punteggio per Stanza Specifica",
        labels={'x': 'Stanza', 'y': 'Punteggio'},
        text_auto='.0f' # Mostra il punteggio intero
    )
    fig_bar_rooms.update_layout(yaxis_range=[0, 5.5]) # Leggermente più di 5 per visibilità testo
    fig_bar_rooms.update_traces(textposition='outside')
    st.plotly_chart(fig_bar_rooms, use_container_width=True)


# --- Pulsante Riepilogo Testuale (Aggiornato) ---
st.markdown("---")
if st.button(" Mostra Riepilogo Testuale Completo"):
    summary = []
    summary.append(f"# Riepilogo Visita: Casalino Solfanuccio")
    summary.append(f"**Data Visita:** {st.session_state.data_visita}")
    summary.append(f"**Prezzo Richiesto:** € 250.000")
    summary.append("\n---\n")

    # Medie Checklist
    summary.append("## Punteggi Medi Checklist per Sezione:")
    labels_from_avg, scores_from_avg, _ = calculate_section_averages(checklist_data)
    for label, score in zip(labels_from_avg, scores_from_avg):
         summary.append(f"- **{label}:** {score:.1f}")
    summary.append("\n---\n")

    # Dettaglio Checklist
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

    # NUOVO: Dettaglio Valutazione Stanze
    summary.append("---\n## Valutazione Stanze Specifiche:\n")
    for room in room_evaluation_data:
        score = st.session_state.get(room["key_score"], 'N/D')
        notes = st.session_state.get(room["key_notes"], '')
        score_str = f"`{score}`" if isinstance(score, (int, float)) else f"`{score}`"
        summary.append(f"### {room['name']}")
        summary.append(f"- **Punteggio:** {score_str}")
        if notes:
            notes_indented = "\n  ".join(notes.strip().split('\n'))
            summary.append(f"- *Note:* {notes_indented}")
        summary.append("\n")


    # Riepilogo Generale
    summary.append("---\n## Riepilogo Generale")
    summary.append(f"**Punti di Forza:**\n{st.session_state.punti_forza}")
    summary.append(f"\n**Criticità / Dubbi:**\n{st.session_state.criticita}")
    summary.append(f"\n**Punteggio Complessivo:** `{st.session_state.impressione_generale}`")
    summary.append(f"\n**Prossimi Passi:**\n{st.session_state.prossimi_passi}")

    st.markdown("---")
    st.subheader("Riepilogo Completo (Markdown)")
    st.text_area("Copia questo riepilogo:", value="\n".join(summary), height=600) # Aumentata altezza


# --- Nota sull'uso ---
# (Aggiornata)
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila la checklist generale (le sezioni rimangono aperte).
    2. Compila la valutazione per ogni stanza specifica.
    3. Passa sopra l'icona ❓ per vedere dettagli/domande.
    4. Visualizza i grafici riassuntivi.
    5. Usa "Mostra Riepilogo Testuale Completo" per il report dettagliato.
    """
)
