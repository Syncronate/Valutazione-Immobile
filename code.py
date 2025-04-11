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
# (Identica alla versione precedente, con tutti gli items e help_text)
checklist_data = [
    {
        "section": "1. STATO GENERALE E MANUTENZIONE",
        "items": [
            {"label": "Qualità Ristrutturazione 2023", "key_score": "s1_q1_score", "key_notes": "s1_q1_notes", "hint": "Dettagli? Cosa rifatto? Documenti?",
             "help_text": "Chiedere nel dettaglio cosa è stato rinnovato (Bagni, cucina, pavimenti, tetto, finestre, impianti?). La ristrutturazione ha coinvolto interventi strutturali? È disponibile la documentazione relativa (fatture, permessi, certificazioni)?"},
            {"label": "Stato Tetto (Visivo/Info)", "key_score": "s1_q2_score", "key_notes": "s1_q2_notes", "hint": "Tegole? Grondaie? Manutenzione?",
             "help_text": "Ispezionare visivamente (se possibile) o chiedere: Ci sono tegole rotte/mancanti? Le grondaie sono pulite e integre? Quando è stato ispezionato o manutenuto l'ultima volta?"},
            {"label": "Stato Facciata (Visivo/Info)", "key_score": "s1_q3_score", "key_notes": "s1_q3_notes", "hint": "Crepe? Intonaco? Umidità risalita?",
              "help_text": "Osservare: Ci sono crepe evidenti? L'intonaco è scrostato o danneggiato? Ci sono segni di umidità di risalita alla base dei muri? Quando è stata fatta l'ultima manutenzione/tinteggiatura?"},
            {"label": "Presenza Umidità/Muffa/Crepe", "key_score": "s1_q4_score", "key_notes": "s1_q4_notes", "hint": "Muri interni/esterni? Angoli? Bagni? Cantina? Odori?",
              "help_text": "Controllare attentamente angoli bassi e alti, muri perimetrali (specie a nord), bagni, eventuale cantina/seminterrato. Cercare macchie, aloni, scrostamenti, odore di muffa o chiuso. Verificare crepe interne/esterne."},
            {"label": "Stato Infissi (Materiale, Età, Tenuta)", "key_score": "s1_q5_score", "key_notes": "s1_q5_notes", "hint": "Chiusura? Spifferi? Condensa? Materiale? Vetrocamera? Età?",
              "help_text": "Aprire e chiudere finestre/porte: Si muovono agevolmente? Ci sono spifferi evidenti? C'è condensa tra i vetri (se vetrocamera)? Di che materiale sono (Legno, PVC, Alluminio)? Chiedere età approssimativa."},
            {"label": "Stato Pavimenti", "key_score": "s1_q6_score", "key_notes": "s1_q6_notes", "hint": "Usura? Livellamento? Materiali? Età?",
             "help_text": "Camminare su tutta la superficie: Ci sono punti in cui il pavimento scricchiola, è avvallato o non è livellato? Valutare grado di usura. Che tipo di materiale è? Chiedere età."},
            {"label": "Stato Pittura/Intonaco Interno", "key_score": "s1_q7_score", "key_notes": "s1_q7_notes", "hint": "Recente? Da rifare? Crepe superficiali?",
             "help_text": "Valutare lo stato generale della tinteggiatura: È recente o necessita di essere rifatta? Ci sono crepe superficiali sull'intonaco?"},
        ]
    },
    {
        "section": "2. IMPIANTI",
        "items": [
            {"label": "Impianto Riscaldamento (Caldaia)", "key_score": "s2_q1_score", "key_notes": "s2_q1_notes", "hint": "Tipo? Età? Revisione? Libretto? Funziona?",
             "help_text": "Chiedere: Che tipo di caldaia è (condensazione, tradizionale)? Quanti anni ha? Quando è stata fatta l'ultima revisione e pulizia fumi (verificare libretto impianto)? L'impianto funziona correttamente?"},
            {"label": "Impianto Climatizzazione", "key_score": "s2_q2_score", "key_notes": "s2_q2_notes", "hint": "Split? Posizione? Età? Revisione?",
             "help_text": "Quanti split ci sono e dove sono posizionati? Quanti anni ha l'impianto? Quando è stata effettuata l'ultima manutenzione/pulizia filtri?"},
            {"label": "Impianto Elettrico (Età, Conformità?)", "key_score": "s2_q3_score", "key_notes": "s2_q3_notes", "hint": "Recente? Prese? Punti luce? Dich. Conformità?",
             "help_text": "L'impianto sembra recente (quadro elettrico, prese, interruttori)? Ci sono abbastanza prese e punti luce? Chiedere se è disponibile la Dichiarazione di Conformità (obbligatoria se rifatto dopo il 2008 o modificato)."},
            {"label": "Impianto Idraulico (Età, Perdite?)", "key_score": "s2_q4_score", "key_notes": "s2_q4_notes", "hint": "Pressione acqua? Scarichi? Età? Perdite passate?",
             "help_text": "Aprire i rubinetti: la pressione dell'acqua è buona? Gli scarichi defluiscono correttamente? Chiedere l'età dell'impianto (se rifatto durante la ristrutturazione). Ci sono stati problemi di perdite in passato?"},
            {"label": "Pozzo (Uso, Funzionamento, Manut.)", "key_score": "s2_q5_score", "key_notes": "s2_q5_notes", "hint": "Irrigazione? Pompa ok? Manutenzione? Potabile?",
             "help_text": "A cosa serve il pozzo (irrigazione, uso domestico)? La pompa è funzionante? Richiede manutenzione specifica? L'acqua è stata analizzata? È potabile?"},
            {"label": "Allaccio Fognatura Comunale?", "key_score": "s2_q6_score", "key_notes": "s2_q6_notes", "hint": "Confermare allaccio rete pubblica.",
             "help_text": "Chiedere conferma se l'immobile è allacciato alla rete fognaria comunale o se dispone di fossa biologica/Imhoff (che richiede manutenzione periodica)."},
        ]
    },
    {
        "section": "3. ASPETTI STRUTTURALI",
        "items": [
            {"label": "Segni Assestamento / Livello Pavimenti", "key_score": "s3_q1_score", "key_notes": "s3_q1_notes", "hint": "Pavimenti inclinati? Crepe strutturali? Porte/finestre?",
              "help_text": "Osservare attentamente se i pavimenti sono inclinati. Cercare crepe significative (non superficiali) sui muri, specialmente oblique o a 'scaletta'. Verificare se porte e finestre chiudono bene o 'toccano' il telaio."},
            {"label": "Problemi Strutturali Passati? (Info)", "key_score": "s3_q2_score", "key_notes": "s3_q2_notes", "hint": "Interventi documentati? Chiedere.",
             "help_text": "Chiedere esplicitamente se ci sono stati problemi strutturali in passato (cedimenti, lesioni importanti) e se sono stati fatti interventi documentati."},
            {"label": "Modifiche Strutturali Autorizzate? (Info)", "key_score": "s3_q3_score", "key_notes": "s3_q3_notes", "hint": "Aggiunte/modifiche? Regolarizzate?",
             "help_text": "Sono state apportate modifiche strutturali (es. apertura muri portanti, ampliamenti) rispetto alla pianta originale? Sono state regolarmente autorizzate con pratiche edilizie?"},
        ]
    },
    {
        "section": "4. ESTERNI E ACCESSORI",
        "items": [
            {"label": "Stato Giardino (ca. 1000mq)", "key_score": "s4_q1_score", "key_notes": "s4_q1_notes", "hint": "Manutenzione? Piante? Recinzione? Livellamento?",
             "help_text": "Valutare lo stato di manutenzione generale del giardino. Com'è la piantumazione? La recinzione è in buono stato? Il terreno è pianeggiante o scosceso?"},
            {"label": "Parcheggio Comune (4 posti auto)", "key_score": "s4_q2_score", "key_notes": "s4_q2_notes", "hint": "Dove? Quanti garantiti? Regole? Costi? Accessibilità? Condiviso con chi?",
             "help_text": "Chiedere con precisione: Dove si trovano i posti auto? Quanti sono assegnati/garantiti a questa proprietà? Ci sono regole di utilizzo? Ci sono costi associati? L'accesso è agevole? Con chi è condiviso (se specificato 'comune')?"},
            {"label": "Potenziale Annesso (Ricostruzione - Info)", "key_score": "s4_q3_score", "key_notes": "s4_q3_notes", "hint": "Dov'era? Dimensioni? Vincoli? Info proprietario.",
             "help_text": "Chiedere dove si trovava l'annesso originale. Quali sono le dimensioni massime ricostruibili? Ci sono vincoli particolari (paesaggistici, urbanistici)? Il proprietario ha già informazioni preliminari dal Comune?"},
            {"label": "Condizioni Generali Esterne", "key_score": "s4_q4_score", "key_notes": "s4_q4_notes", "hint": "Muri cinta? Cancello? Illuminazione? Vialetti?",
              "help_text": "Valutare lo stato di eventuali muri di cinta, del cancello (manuale/elettrico?), dell'illuminazione esterna, dei vialetti e delle pavimentazioni esterne."},
        ]
    },
     {
        "section": "5. EFFICIENZA ENERGETICA E COSTI",
        "items": [
            {"label": "Classe Energetica E (Verifica APE?)", "key_score": "s5_q1_score", "key_notes": "s5_q1_notes", "hint": "APE disponibile? Conferma kWh/m² anno?",
             "help_text": "Chiedere se è disponibile l'Attestato di Prestazione Energetica (APE) in corso di validità. Confermare il valore di consumo indicato (EPgl,nren)."},
            {"label": "Interventi Efficienza Energetica? (in ristr.)", "key_score": "s5_q2_score", "key_notes": "s5_q2_notes", "hint": "Cappotto? Infissi performanti? Tetto isolato?",
             "help_text": "Durante la ristrutturazione del 2023 sono stati fatti interventi specifici per migliorare l'efficienza? (Es. isolamento a cappotto, sostituzione infissi con modelli performanti, isolamento del tetto/solaio)."},
            {"label": "Costi Utenze Medie Annuali? (Info)", "key_score": "s5_q3_score", "key_notes": "s5_q3_notes", "hint": "Chiedere stima Gas, Luce, Acqua.",
             "help_text": "Chiedere al proprietario una stima dei costi annuali o mensili per le principali utenze (gas metano per riscaldamento/acqua calda, energia elettrica, acqua da acquedotto). Se possibile, visionare bollette."},
            {"label": "Costi Imposte Annuali? (IMU, TARI - Info)", "key_score": "s5_q4_score", "key_notes": "s5_q4_notes", "hint": "Chiedere importi indicativi.",
             "help_text": "Chiedere l'importo approssimativo dell'IMU (se seconda casa o di lusso) e della TARI (tassa rifiuti) pagate annualmente."},
            {"label": "Spese Condivise / Straordinarie? (Info)", "key_score": "s5_q5_score", "key_notes": "s5_q5_notes", "hint": "Oltre parcheggio? Strada privata? Spese future zona?",
             "help_text": "Ci sono altre spese condivise con vicini (es. manutenzione strada privata di accesso)? Sono state deliberate o sono previste spese straordinarie significative nella zona (es. rifacimento fognature, strade)?"},
        ]
    },
    {
        "section": "6. ZONA, CONTESTO E ASPETTI GENERALI",
        "items": [
            {"label": "Luminosità Naturale / Esposizione", "key_score": "s6_q1_score", "key_notes": "s6_q1_notes", "hint": "Stanze luminose? Orientamento?",
             "help_text": "Valutare la luminosità naturale nelle diverse stanze durante l'orario della visita. Qual è l'esposizione principale della casa (Sud, Nord, Est, Ovest)?"},
            {"label": "Rumorosità Zona (Percepita/Info)", "key_score": "s6_q2_score", "key_notes": "s6_q2_notes", "hint": "Traffico? Vicini? Attività? Valutare/Chiedere.",
             "help_text": "Durante la visita, prestare attenzione ai rumori esterni (traffico, attività vicine, animali). Chiedere al proprietario com'è la rumorosità in diversi momenti della giornata/settimana."},
            {"label": "Qualità Vista Panoramica", "key_score": "s6_q3_score", "key_notes": "s6_q3_notes", "hint": "Corrisponde a descrizione? Ostacoli?",
             "help_text": "La vista panoramica descritta nell'annuncio corrisponde alla realtà? Ci sono ostacoli visivi importanti (es. edifici, pali)?"},
            {"label": "Vicinanza Servizi Essenziali (Info)", "key_score": "s6_q4_score", "key_notes": "s6_q4_notes", "hint": "Distanza reale negozi, farmacia, scuole? Auto indispensabile?",
             "help_text": "Chiedere o verificare la distanza effettiva (a piedi/in auto) dai principali servizi: negozi alimentari, farmacia, scuole, fermate mezzi pubblici. L'auto è indispensabile per ogni spostamento?"},
            {"label": "Qualità Connessione Internet? (Info)", "key_score": "s6_q5_score", "key_notes": "s6_q5_notes", "hint": "Tipo connessione? Velocità? Chiedere.",
              "help_text": "Chiedere che tipo di connessione internet è disponibile (Fibra FTTH/FTTC, ADSL, FWA, solo mobile?). Qual è la velocità tipica? È stabile?"},
            {"label": "Funzionalità Disposizione Interna", "key_score": "s6_q6_score", "key_notes": "s6_q6_notes", "hint": "Spazi ben distribuiti? Corridoi? Stanze sfruttabili?",
             "help_text": "Valutare se la disposizione degli spazi è funzionale per le proprie esigenze. Ci sono corridoi lunghi/sprecati? Le stanze hanno forme regolari e sono facilmente arredabili?"},
            {"label": "Presenza Odori Particolari", "key_score": "s6_q7_score", "key_notes": "s6_q7_notes", "hint": "Muffa, chiuso, scarichi, fumo?",
             "help_text": "Prestare attenzione a eventuali odori sgradevoli o persistenti (muffa, umido, chiuso, scarichi, fumo di sigaretta impregnato nei muri)."},
            {"label": "Arredamento Incluso? (Parziale - Info)", "key_score": "s6_q8_score", "key_notes": "s6_q8_notes", "hint": "Chiedere *esattamente* cosa rimane.",
             "help_text": "L'annuncio indica 'parzialmente arredato'. Chiedere una lista precisa di quali mobili/elettrodomestici sono inclusi nel prezzo di vendita."},
            {"label": "Chiarimento Superficie (130 vs 174mq - Info)", "key_score": "s6_q9_score", "key_notes": "s6_q9_notes", "hint": "Dettaglio mq calpestabili/commerciali? Cosa sono i 174mq?",
             "help_text": "Chiedere chiarimenti sulla discrepanza tra superficie commerciale (130mq) e totale indicata (174mq). Qual è la superficie calpestabile interna? Cosa comprendono esattamente i 174mq (giardino, aree scoperte, annesso da ricostruire?)?"},
            {"label": "Motivazioni Vendita / Tempistiche? (Info)", "key_score": "s6_q10_score", "key_notes": "s6_q10_notes", "hint": "Da quanto in vendita? Perché? Disponibilità rogito? Trattabilità?",
             "help_text": "Chiedere (con tatto) da quanto tempo l'immobile è in vendita e qual è il motivo. Qual è la loro tempistica ideale per il rogito notarile? C'è margine di trattativa sul prezzo?"},
        ]
    }
]

# --- Inizializzazione Session State ---
# (Invariato)
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.active_section = None
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
# (Invariato)
def set_active_section(section_key):
    st.session_state.active_section = section_key

# --- Funzione per Calcolare Medie Sezioni ---
# (Invariato)
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
# (Invariato)
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
            # Usiamo il label dell'item come titolo principale
            st.markdown(f"**{item['label']}**")
            # Il caption rimane visibile sotto il titolo
            if "hint" in item:
                 st.caption(f"*{item['hint']}*")

            col1, col2 = st.columns([1, 2])

            with col1:
                # MODIFICA: Rimosso label_visibility per far apparire l'help
                st.radio(
                    "Punteggio:", # L'etichetta ora è visibile
                    options=[1, 2, 3, 4, 5],
                    key=item["key_score"],
                    horizontal=True,
                    # label_visibility="collapsed", # RIMOSSO/COMMENTATO
                    on_change=set_active_section,
                    args=(section_key,),
                    help=item.get("help_text") # Parametro Help
                )

            with col2:
                st.text_area(
                    "Note:",
                    key=item["key_notes"],
                    value=st.session_state[item["key_notes"]],
                    height=70,
                    label_visibility="collapsed", # Le note possono rimanere collapsed
                    on_change=set_active_section,
                    args=(section_key,)
                )
            st.markdown("---") # Divisore tra gli item

# --- Sezione Riepilogo Generale ---
# (Invariato)
st.markdown("---")
st.header("Riepilogo e Impressione Generale")
# ... (resto del codice identico alla versione precedente) ...
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
# (Invariato)
st.markdown("---")
st.header(" Riepilogo Grafico")
# ... (resto del codice identico alla versione precedente) ...
section_labels, section_scores, section_averages_dict = calculate_section_averages(checklist_data)
if not section_labels or not any(s > 0 for s in section_scores):
    st.warning("Inserisci almeno un punteggio per generare i grafici.")
else:
    fig_radar = go.Figure()
    valid_scores_radar = [s if s > 0 else 0.1 for s in section_scores]
    fig_radar.add_trace(go.Scatterpolar(r=valid_scores_radar + [valid_scores_radar[0]], theta=section_labels + [section_labels[0]], fill='toself', name='Punteggio Medio'))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 5])), showlegend=False, title="Punteggio Medio per Sezione (Radar)")
    st.plotly_chart(fig_radar, use_container_width=True)

    fig_bar = px.bar(x=section_labels, y=section_scores, title="Punteggio Medio per Sezione (Barre)", labels={'x': 'Sezione', 'y': 'Punteggio Medio'}, text_auto='.1f')
    fig_bar.update_layout(yaxis_range=[0, 5])
    fig_bar.update_traces(textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)


# --- Pulsante Riepilogo Testuale ---
# (Invariato)
st.markdown("---")
if st.button(" Mostra Riepilogo Testuale Completo"):
    # ... (resto del codice identico alla versione precedente) ...
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
# (Aggiornata)
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila i punteggi e le note. La sezione attiva rimarrà aperta.
    2. Passa sopra l'icona ❓ accanto all'etichetta "Punteggio:" per vedere dettagli/domande.
    3. Visualizza i grafici riassuntivi.
    4. Usa "Mostra Riepilogo Testuale Completo" per il report dettagliato.
    """
)
