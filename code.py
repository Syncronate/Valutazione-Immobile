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

# --- Struttura Dati Checklist (con OPTIONS e nuova key per multiselect/extra notes) ---
checklist_data = [
    {
        "section": "1. STATO GENERALE E MANUTENZIONE",
        "items": [
            {"label": "Qualità Ristrutturazione 2023", "key_score": "s1_q1_score", "key_ms": "s1_q1_ms", "key_notes_extra": "s1_q1_notes_extra", "hint": "Dettagli? Cosa rifatto? Documenti?", "help_text": "Chiedere dettaglio: cosa rinnovato? (Bagni, cucina, pavimenti, impianti?). Interventi strutturali? Documentazione disponibile?",
             "options": ["Aspetto recente/moderno", "Finiture economiche/standard", "Lavoro ben eseguito (visibile)", "Lavoro approssimativo (visibile)", "Ristrutturazione solo estetica?", "Ristrutturazione completa (da conf.)", "Verificare Documenti", "Altro (vedi note extra)"]},
            {"label": "Stato Tetto (Visivo/Info)", "key_score": "s1_q2_score", "key_ms": "s1_q2_ms", "key_notes_extra": "s1_q2_notes_extra", "hint": "Tegole? Grondaie? Manutenzione?", "help_text": "Ispezionare o chiedere: Tegole rotte/mancanti? Grondaie OK/Danneggiate? Ultima manutenzione?",
             "options": ["Aspetto recente/Buono stato", "Aspetto datato/Usurato", "Tegole danneggiate/mancanti", "Grondaie OK", "Grondaie danneggiate/intasate", "Muschio/Segni infiltrazioni?", "Non visibile", "Necessita controllo esperto", "Altro (vedi note extra)"]},
            {"label": "Stato Facciata (Visivo/Info)", "key_score": "s1_q3_score", "key_ms": "s1_q3_ms", "key_notes_extra": "s1_q3_notes_extra", "hint": "Crepe? Intonaco? Umidità risalita?", "help_text": "Osservare: Crepe evidenti? Intonaco scrostato? Segni umidità risalita? Ultima manutenzione?",
              "options": ["Buono stato/Recente", "Datata/Da rinfrescare", "Crepe evidenti", "Intonaco scrostato/danneggiato", "Segni umidità risalita", "Balconi/Elementi OK", "Balconi/Elementi ammalorati", "Altro (vedi note extra)"]},
            {"label": "Presenza Umidità/Muffa/Crepe", "key_score": "s1_q4_score", "key_ms": "s1_q4_ms", "key_notes_extra": "s1_q4_notes_extra", "hint": "Muri interni/esterni? Angoli? Bagni? Cantina? Odori?", "help_text": "Controllare angoli, muri perimetrali, bagni, cantina. Cercare macchie, aloni, odore muffa. Verificare crepe.",
              "options": ["Nessun segno evidente", "Muffa (localizzata)", "Muffa (diffusa)", "Macchie/Aloni umidità", "Odore muffa/umido", "Crepe intonaco", "Crepe sospette (strutturali?)", "Condensa presente", "Altro (vedi note extra)"]},
            {"label": "Stato Infissi (Materiale, Età, Tenuta)", "key_score": "s1_q5_score", "key_ms": "s1_q5_ms", "key_notes_extra": "s1_q5_notes_extra", "hint": "Chiusura? Spifferi? Condensa? Materiale? Vetrocamera? Età?", "help_text": "Aprire/chiudere: Si muovono bene? Spifferi? Condensa tra vetri? Materiale? Età?",
              "options": ["Nuovi/Recenti", "Datati ma funzionali", "Da sostituire", "Legno", "PVC", "Alluminio", "Vetro singolo", "Vetrocamera (doppio/triplo)", "Buona tenuta", "Spifferi evidenti", "Cassonetti tapparelle vecchi/non isolati", "Altro (vedi note extra)"]},
            {"label": "Stato Pavimenti", "key_score": "s1_q6_score", "key_ms": "s1_q6_ms", "key_notes_extra": "s1_q6_notes_extra", "hint": "Usura? Livellamento? Materiali? Età?", "help_text": "Camminare: Scricchiolii? Avvallamenti? Usura? Materiale? Età?",
             "options": ["Nuovi/Ottimo stato", "Buono stato/Poco usurati", "Usurati/Da lucidare", "Danneggiati/Da sostituire", "Non livellati", "Materiale pregio", "Materiale standard", "Materiale economico", "Altro (vedi note extra)"]},
            {"label": "Stato Pittura/Intonaco Interno", "key_score": "s1_q7_score", "key_ms": "s1_q7_ms", "key_notes_extra": "s1_q7_notes_extra", "hint": "Recente? Da rifare? Crepe superficiali?", "help_text": "Valutare stato tinteggiatura: Recente? Da rifare? Crepe superficiali?",
             "options": ["Rifatta di recente", "Buone condizioni", "Da rinfrescare", "Da rifare (pareti rovinate)", "Crepe superficiali intonaco", "Altro (vedi note extra)"]},
        ]
    },
    # --- SEZIONE 2: IMPIANTI ---
    {
        "section": "2. IMPIANTI",
        "items": [
             {"label": "Impianto Riscaldamento (Caldaia)", "key_score": "s2_q1_score", "key_ms": "s2_q1_ms", "key_notes_extra": "s2_q1_notes_extra", "hint": "Tipo? Età? Revisione? Libretto? Funziona?", "help_text": "Chiedere: Tipo caldaia? Età? Ultima revisione (libretto)? Funziona?",
              "options": ["Caldaia recente (condensazione?)", "Caldaia datata", "Caldaia vecchia (da sostituire?)", "Manutenzione regolare (documentata)", "Manutenzione incerta", "Libretto impianto presente", "Libretto mancante/incompleto", "Radiatori/Termosifoni OK", "Radiatori vecchi/danneggiati", "Altro (vedi note extra)"]},
             {"label": "Impianto Climatizzazione", "key_score": "s2_q2_score", "key_ms": "s2_q2_ms", "key_notes_extra": "s2_q2_notes_extra", "hint": "Split? Posizione? Età? Revisione?", "help_text": "Split: numero, posizione? Età impianto? Ultima manutenzione?",
              "options": ["Presente e recente", "Presente ma datato", "Assente", "Split ben posizionati", "Split in posizioni scomode", "Manutenzione recente (riferita)", "Altro (vedi note extra)"]},
             {"label": "Impianto Elettrico (Età, Conformità?)", "key_score": "s2_q3_score", "key_ms": "s2_q3_ms", "key_notes_extra": "s2_q3_notes_extra", "hint": "Recente? Prese? Punti luce? Dich. Conformità?", "help_text": "Aspetto recente (quadro, prese)? Prese/punti luce sufficienti? Dichiarazione Conformità disponibile?",
              "options": ["Rifatto/Recente (visibile)", "Datato (visibile)", "Vecchio/Da rifare", "Prese/Punti luce sufficienti", "Prese/Punti luce scarsi", "Quadro elettrico moderno", "Quadro elettrico vecchio", "Conformità presente/dichiarata", "Conformità assente/incerta", "Altro (vedi note extra)"]},
             {"label": "Impianto Idraulico (Età, Perdite?)", "key_score": "s2_q4_score", "key_ms": "s2_q4_ms", "key_notes_extra": "s2_q4_notes_extra", "hint": "Pressione acqua? Scarichi? Età? Perdite passate?", "help_text": "Pressione acqua OK? Scarichi OK? Età impianto? Problemi perdite passate?",
              "options": ["Rifatto/Recente (visibile/dich.)", "Datato", "Vecchio/Rischio problemi", "Pressione acqua buona", "Pressione acqua scarsa", "Scarichi efficienti", "Scarichi lenti/rumorosi", "Nessuna perdita passata riferita", "Perdite passate riferite", "Altro (vedi note extra)"]},
             {"label": "Pozzo (Uso, Funzionamento, Manut.)", "key_score": "s2_q5_score", "key_ms": "s2_q5_ms", "key_notes_extra": "s2_q5_notes_extra", "hint": "Irrigazione? Pompa ok? Manutenzione? Potabile?", "help_text": "Uso pozzo? Pompa funzionante? Manutenzione? Acqua potabile?",
              "options": ["Presente e funzionante", "Presente ma non funzionante/usato", "Assente", "Uso irrigazione", "Uso domestico (verificare potabilità!)", "Pompa OK", "Pompa da verificare/riparare", "Manutenzione necessaria", "Acqua potabile (certificata?)", "Acqua non potabile", "Altro (vedi note extra)"]},
             {"label": "Allaccio Fognatura Comunale?", "key_score": "s2_q6_score", "key_ms": "s2_q6_ms", "key_notes_extra": "s2_q6_notes_extra", "hint": "Confermare allaccio rete pubblica.", "help_text": "Confermare allaccio fognatura comunale o presenza fossa biologica/Imhoff.",
              "options": ["Allacciato a rete comunale", "Fossa biologica/Imhoff", "Fossa da svuotare/manutenere", "Sistema incerto/Da verificare", "Altro (vedi note extra)"]},
        ]
    },
    # --- SEZIONE 3: ASPETTI STRUTTURALI ---
    {
        "section": "3. ASPETTI STRUTTURALI",
         "items": [
            {"label": "Segni Assestamento / Livello Pavimenti", "key_score": "s3_q1_score", "key_ms": "s3_q1_ms", "key_notes_extra": "s3_q1_notes_extra", "hint": "Pavimenti inclinati? Crepe strutturali? Porte/finestre?", "help_text": "Osservare pavimenti inclinati. Cercare crepe significative muri (oblique?). Porte/finestre chiudono bene?",
              "options": ["Nessun segno evidente", "Pavimenti leggermente inclinati", "Pavimenti molto inclinati", "Crepe solo intonaco", "Crepe sospette (strutturali?)", "Porte/Finestre OK", "Porte/Finestre 'toccano'/non chiudono bene", "Necessita verifica esperto", "Altro (vedi note extra)"]},
            {"label": "Problemi Strutturali Passati? (Info)", "key_score": "s3_q2_score", "key_ms": "s3_q2_ms", "key_notes_extra": "s3_q2_notes_extra", "hint": "Interventi documentati? Chiedere.", "help_text": "Chiedere esplicitamente problemi strutturali passati (cedimenti?) e interventi documentati.",
              "options": ["Nessuno riferito", "Problemi riferiti e risolti (documentati?)", "Problemi riferiti (dettagli?)", "Informazione non disponibile/vaga", "Altro (vedi note extra)"]},
            {"label": "Modifiche Strutturali Autorizzate? (Info)", "key_score": "s3_q3_score", "key_ms": "s3_q3_ms", "key_notes_extra": "s3_q3_notes_extra", "hint": "Aggiunte/modifiche? Regolarizzate?", "help_text": "Modifiche strutturali (muri portanti?) rispetto a pianta originale? Regolarmente autorizzate?",
              "options": ["Nessuna modifica riferita", "Modifiche riferite e autorizzate", "Modifiche riferite (verificare autorizzazioni!)", "Abusi edilizi sanati?", "Abusi edilizi presenti?", "Informazione non disponibile/vaga", "Altro (vedi note extra)"]},
        ]
    },
    # --- SEZIONE 4: ESTERNI E ACCESSORI ---
    {
        "section": "4. ESTERNI E ACCESSORI",
        "items": [
            {"label": "Stato Giardino (ca. 1000mq)", "key_score": "s4_q1_score", "key_ms": "s4_q1_ms", "key_notes_extra": "s4_q1_notes_extra", "hint": "Manutenzione? Piante? Recinzione? Livellamento?", "help_text": "Valutare manutenzione giardino. Piantumazione? Recinzione OK? Terreno pianeggiante/scosceso?",
             "options": ["Ben tenuto", "Trascurato", "Da sistemare", "Piantumazione curata", "Piantumazione scarsa/assente", "Recinzione OK", "Recinzione danneggiata/assente", "Pianeggiante", "Scosceso/In pendenza", "Spazio sfruttabile", "Altro (vedi note extra)"]},
            {"label": "Parcheggio Comune (4 posti auto)", "key_score": "s4_q2_score", "key_ms": "s4_q2_ms", "key_notes_extra": "s4_q2_notes_extra", "hint": "Dove? Quanti garantiti? Regole? Costi? Accessibilità? Condiviso con chi?", "help_text": "Chiedere: Dove sono? Quanti assegnati? Regole? Costi? Accesso? Condiviso con chi?",
             "options": ["Posti auto assegnati/chiari", "Posti auto liberi/non garantiti", "Spazio ampio", "Spazio stretto/difficile manovra", "Accesso comodo", "Accesso scomodo", "Nessun costo extra", "Costi gestione/manutenzione?", "Area ben tenuta", "Area trascurata", "Altro (vedi note extra)"]},
            {"label": "Potenziale Annesso (Ricostruzione - Info)", "key_score": "s4_q3_score", "key_ms": "s4_q3_ms", "key_notes_extra": "s4_q3_notes_extra", "hint": "Dov'era? Dimensioni? Vincoli? Info proprietario.", "help_text": "Chiedere: Dov'era annesso? Dimensioni ricostruibili? Vincoli? Info preliminari Comune?",
             "options": ["Potenziale interessante", "Potenziale limitato", "Vincoli presenti (paesaggistici?)", "Costi ricostruzione elevati (presunti)", "Informazioni chiare fornite", "Informazioni vaghe/assenti", "Verifica fattibilità in Comune necessaria", "Altro (vedi note extra)"]},
            {"label": "Condizioni Generali Esterne", "key_score": "s4_q4_score", "key_ms": "s4_q4_ms", "key_notes_extra": "s4_q4_notes_extra", "hint": "Muri cinta? Cancello? Illuminazione? Vialetti?", "help_text": "Valutare stato muri cinta, cancello, illuminazione esterna, vialetti, pavimentazioni.",
              "options": ["Buono stato generale", "Necessitano manutenzione", "Muri cinta OK", "Muri cinta danneggiati", "Cancello OK (manuale/elettrico?)", "Cancello da riparare", "Illuminazione presente/funzionante", "Illuminazione scarsa/assente", "Vialetti/Pavimentazioni OK", "Vialetti/Pavimentazioni sconnessi/rotti", "Altro (vedi note extra)"]},
        ]
    },
    # --- SEZIONE 5: EFFICIENZA ENERGETICA E COSTI ---
     {
        "section": "5. EFFICIENZA ENERGETICA E COSTI",
        "items": [
            {"label": "Classe Energetica E (Verifica APE?)", "key_score": "s5_q1_score", "key_ms": "s5_q1_ms", "key_notes_extra": "s5_q1_notes_extra", "hint": "APE disponibile? Conferma kWh/m² anno?", "help_text": "Chiedere APE valido. Confermare valore consumo (EPgl,nren).",
             "options": ["APE disponibile e visionato", "APE non disponibile/scaduto", "Classe E confermata", "Classe energetica bassa (costi elevati?)", "Indice consumo elevato", "Possibili miglioramenti", "Altro (vedi note extra)"]},
            {"label": "Interventi Efficienza Energetica? (in ristr.)", "key_score": "s5_q2_score", "key_ms": "s5_q2_ms", "key_notes_extra": "s5_q2_notes_extra", "hint": "Cappotto? Infissi performanti? Tetto isolato?", "help_text": "Fatti interventi specifici durante ristrutturazione? (Cappotto, infissi, tetto isolato?)",
             "options": ["Interventi specifici effettuati (dich.)", "Nessun intervento specifico (dich.)", "Isolamento a cappotto presente", "Infissi performanti installati", "Tetto isolato (verificare)", "Interventi non documentati/verificabili", "Altro (vedi note extra)"]},
            {"label": "Costi Utenze Medie Annuali? (Info)", "key_score": "s5_q3_score", "key_ms": "s5_q3_ms", "key_notes_extra": "s5_q3_notes_extra", "hint": "Chiedere stima Gas, Luce, Acqua.", "help_text": "Chiedere stima costi annuali/mensili Gas, Luce, Acqua. Visionare bollette?",
             "options": ["Costi stimati forniti (bassi)", "Costi stimati forniti (medi)", "Costi stimati forniti (alti)", "Bollette visionate", "Informazioni vaghe/non fornite", "Costi probabilmente alti (classe E)", "Altro (vedi note extra)"]},
            {"label": "Costi Imposte Annuali? (IMU, TARI - Info)", "key_score": "s5_q4_score", "key_ms": "s5_q4_ms", "key_notes_extra": "s5_q4_notes_extra", "hint": "Chiedere importi indicativi.", "help_text": "Chiedere importo approx IMU (se dovuta) e TARI annuali.",
             "options": ["Importi forniti (bassi)", "Importi forniti (medi)", "Importi forniti (alti)", "Informazioni vaghe/non fornite", "Verificare aliquote comunali", "Altro (vedi note extra)"]},
            {"label": "Spese Condivise / Straordinarie? (Info)", "key_score": "s5_q5_score", "key_ms": "s5_q5_ms", "key_notes_extra": "s5_q5_notes_extra", "hint": "Oltre parcheggio? Strada privata? Spese future zona?", "help_text": "Altre spese condivise (strada accesso)? Spese straordinarie previste zona?",
             "options": ["Nessuna spesa extra riferita", "Spese manutenzione strada privata", "Altre spese condivise (specificare?)", "Spese straordinarie previste (informarsi?)", "Informazioni non disponibili", "Altro (vedi note extra)"]},
        ]
    },
    # --- SEZIONE 6: ZONA, CONTESTO E ASPETTI GENERALI ---
    {
        "section": "6. ZONA, CONTESTO E ASPETTI GENERALI",
        "items": [
            {"label": "Luminosità Naturale / Esposizione", "key_score": "s6_q1_score", "key_ms": "s6_q1_ms", "key_notes_extra": "s6_q1_notes_extra", "hint": "Stanze luminose? Orientamento?", "help_text": "Valutare luminosità stanze. Esposizione principale casa?",
             "options": ["Molto luminoso", "Abbastanza luminoso", "Poco luminoso", "Esposizione buona (Sud/Est/Ovest)", "Esposizione sfavorevole (Nord)", "Altro (vedi note extra)"]},
            {"label": "Rumorosità Zona (Percepita/Info)", "key_score": "s6_q2_score", "key_ms": "s6_q2_ms", "key_notes_extra": "s6_q2_notes_extra", "hint": "Traffico? Vicini? Attività? Valutare/Chiedere.", "help_text": "Prestare attenzione rumori esterni. Chiedere com'è in diversi momenti.",
             "options": ["Molto silenzioso", "Abbastanza silenzioso", "Rumori di fondo presenti (traffico?)", "Rumoroso", "Vicini tranquilli (riferito)", "Vicini rumorosi (riferito)", "Rumori specifici (attività? animali?)", "Altro (vedi note extra)"]},
            {"label": "Qualità Vista Panoramica", "key_score": "s6_q3_score", "key_ms": "s6_q3_ms", "key_notes_extra": "s6_q3_notes_extra", "hint": "Corrisponde a descrizione? Ostacoli?", "help_text": "Vista corrisponde ad annuncio? Ostacoli visivi?",
             "options": ["Vista notevole/Come da descrizione", "Vista parziale/limitata", "Vista ostruita", "Vista aperta", "Vista su colline", "Vista mare (in lontananza?)", "Altro (vedi note extra)"]},
            {"label": "Vicinanza Servizi Essenziali (Info)", "key_score": "s6_q4_score", "key_ms": "s6_q4_ms", "key_notes_extra": "s6_q4_notes_extra", "hint": "Distanza reale negozi, farmacia, scuole? Auto indispensabile?", "help_text": "Verificare distanza effettiva servizi. Auto indispensabile?",
             "options": ["Servizi vicini/raggiungibili a piedi", "Servizi a breve distanza (auto)", "Servizi lontani", "Auto indispensabile", "Zona isolata", "Trasporti pubblici vicini", "Trasporti pubblici scarsi/assenti", "Altro (vedi note extra)"]},
            {"label": "Qualità Connessione Internet? (Info)", "key_score": "s6_q5_score", "key_ms": "s6_q5_ms", "key_notes_extra": "s6_q5_notes_extra", "hint": "Tipo connessione? Velocità? Chiedere.", "help_text": "Tipo connessione disponibile (Fibra? ADSL? FWA?)? Velocità? Stabilità?",
              "options": ["Fibra ottica disponibile (FTTH/FTTC)", "ADSL disponibile", "FWA (Fixed Wireless) disponibile", "Solo connessione mobile", "Connessione veloce/stabile (riferito)", "Connessione lenta/instabile (riferito)", "Verificare copertura operatori", "Altro (vedi note extra)"]},
            {"label": "Funzionalità Disposizione Interna", "key_score": "s6_q6_score", "key_ms": "s6_q6_ms", "key_notes_extra": "s6_q6_notes_extra", "hint": "Spazi ben distribuiti? Corridoi? Stanze sfruttabili?", "help_text": "Disposizione spazi funzionale? Corridoi sprecati? Stanze regolari/arredabili?",
             "options": ["Layout ottimo/funzionale", "Layout buono", "Layout migliorabile", "Spazi ben distribuiti", "Spazi mal distribuiti/corridoi lunghi", "Stanze ampie", "Stanze piccole", "Facilmente arredabile", "Difficile da arredare", "Altro (vedi note extra)"]},
            {"label": "Presenza Odori Particolari", "key_score": "s6_q7_score", "key_ms": "s6_q7_ms", "key_notes_extra": "s6_q7_notes_extra", "hint": "Muffa, chiuso, scarichi, fumo?", "help_text": "Attenzione odori sgradevoli (muffa, umido, chiuso, scarichi, fumo).",
             "options": ["Nessun odore particolare", "Odore di chiuso/poco areato", "Odore di muffa/umido", "Odore dagli scarichi", "Odore di fumo", "Altro (vedi note extra)"]},
            {"label": "Arredamento Incluso? (Parziale - Info)", "key_score": "s6_q8_score", "key_ms": "s6_q8_ms", "key_notes_extra": "s6_q8_notes_extra", "hint": "Chiedere *esattamente* cosa rimane.", "help_text": "Chiedere lista precisa mobili/elettrodomestici inclusi.",
             "options": ["Nessun arredo incluso", "Solo cucina inclusa", "Cucina e bagni inclusi", "Arredo parziale (lista fornita?)", "Arredo completo incluso", "Mobili vecchi/da sostituire", "Mobili di buona qualità", "Altro (vedi note extra)"]},
            {"label": "Chiarimento Superficie (130 vs 174mq - Info)", "key_score": "s6_q9_score", "key_ms": "s6_q9_ms", "key_notes_extra": "s6_q9_notes_extra", "hint": "Dettaglio mq calpestabili/commerciali? Cosa sono i 174mq?", "help_text": "Chiedere chiarimenti discrepanza mq. Sup. calpestabile? Cosa include 174mq?",
             "options": ["Discrepanza chiarita (OK)", "Discrepanza chiarita (Superficie minore del previsto?)", "Discrepanza non chiarita/confusa", "Superficie commerciale vs lorda", "Inclusione aree esterne?", "Verificare visura catastale", "Altro (vedi note extra)"]},
            {"label": "Motivazioni Vendita / Tempistiche? (Info)", "key_score": "s6_q10_score", "key_ms": "s6_q10_ms", "key_notes_extra": "s6_q10_notes_extra", "hint": "Da quanto in vendita? Perché? Disponibilità rogito? Trattabilità?", "help_text": "Chiedere (con tatto): Da quanto in vendita? Motivo? Tempistica rogito? Margine trattativa?",
             "options": ["Motivazione chiara/comprensibile", "Motivazione vaga/sconosciuta", "Vendita urgente?", "Nessuna fretta di vendere", "Disponibilità immediata al rogito", "Tempistiche lunghe per rogito", "Prezzo trattabile (indicato)", "Prezzo non trattabile (indicato)", "In vendita da poco", "In vendita da molto tempo", "Altro (vedi note extra)"]},
        ]
    }
]


# --- Struttura Dati per Valutazione Stanze (con OPTIONS) ---
room_evaluation_data = [
    {"name": "Soggiorno/Cucina (PT)", "key_score": "room_sogg_score", "key_ms": "room_sogg_ms", "key_notes_extra": "room_sogg_notes_extra", "help": "Valuta condizioni generali, finiture, luminosità, prese, segni di usura specifici di questa stanza.",
     "options": ["Luminoso", "Poco luminoso", "Spazioso", "Piccolo/Angusto", "Layout funzionale", "Layout poco pratico", "Finiture buone/recenti", "Finiture usurate/datate", "Pavimento OK", "Pavimento rovinato", "Pareti OK", "Pareti da sistemare", "Prese OK", "Prese scarse", "Cucina OK", "Cucina datata/da rifare", "Altro (vedi note extra)"]},
    {"name": "Bagno/Lavanderia (PT)", "key_score": "room_bagno_pt_score", "key_ms": "room_bagno_pt_ms", "key_notes_extra": "room_bagno_pt_notes_extra", "help": "Valuta sanitari, rubinetteria, scarichi, piastrelle, finestra, muffa, spazio lavatrice.",
     "options": ["Recente/Ristrutturato", "Funzionale ma datato", "Da rifare", "Sanitari OK", "Sanitari vecchi/rovinati", "Rubinetteria OK", "Rubinetteria da sostituire", "Doccia/Vasca OK", "Doccia/Vasca rovinata", "Piastrelle OK", "Piastrelle rotte/vecchie", "Finestra presente", "Cieco (con aerazione forzata?)", "Spazio lavatrice OK", "Spazio lavatrice assente/scomodo", "Muffa presente", "Altro (vedi note extra)"]},
    {"name": "Camera Matrimoniale (PT)", "key_score": "room_cam_pt_score", "key_ms": "room_cam_pt_ms", "key_notes_extra": "room_cam_pt_notes_extra", "help": "Valuta dimensioni, luminosità, prese, condizioni pavimento/pareti, infissi.",
      "options": ["Ampia", "Dimensioni standard", "Piccola", "Luminosa", "Poco luminosa", "Pavimento OK", "Pavimento rovinato", "Pareti OK", "Pareti da sistemare", "Infissi OK", "Infissi problematici", "Prese OK", "Prese scarse", "Altro (vedi note extra)"]},
    {"name": "Camera 1 (P1)", "key_score": "room_cam1_p1_score", "key_ms": "room_cam1_p1_ms", "key_notes_extra": "room_cam1_p1_notes_extra", "help": "Valuta dimensioni, luminosità, prese, condizioni pavimento/pareti, infissi.",
      "options": ["Ampia", "Dimensioni standard", "Piccola", "Luminosa", "Poco luminosa", "Pavimento OK", "Pavimento rovinato", "Pareti OK", "Pareti da sistemare", "Infissi OK", "Infissi problematici", "Prese OK", "Prese scarse", "Altro (vedi note extra)"]},
    {"name": "Camera 2 (P1)", "key_score": "room_cam2_p1_score", "key_ms": "room_cam2_p1_ms", "key_notes_extra": "room_cam2_p1_notes_extra", "help": "Valuta dimensioni, luminosità, prese, condizioni pavimento/pareti, infissi.",
      "options": ["Ampia", "Dimensioni standard", "Piccola", "Luminosa", "Poco luminosa", "Pavimento OK", "Pavimento rovinato", "Pareti OK", "Pareti da sistemare", "Infissi OK", "Infissi problematici", "Prese OK", "Prese scarse", "Altro (vedi note extra)"]},
    {"name": "Bagno (P1)", "key_score": "room_bagno_p1_score", "key_ms": "room_bagno_p1_ms", "key_notes_extra": "room_bagno_p1_notes_extra", "help": "Valuta sanitari, rubinetteria, scarichi, doccia/vasca, piastrelle, finestra, muffa.",
     "options": ["Recente/Ristrutturato", "Funzionale ma datato", "Da rifare", "Sanitari OK", "Sanitari vecchi/rovinati", "Rubinetteria OK", "Rubinetteria da sostituire", "Doccia/Vasca OK", "Doccia/Vasca rovinata", "Piastrelle OK", "Piastrelle rotte/vecchie", "Finestra presente", "Cieco (con aerazione forzata?)", "Muffa presente", "Altro (vedi note extra)"]},
    {"name": "Cantina (Ex Ingresso PT)", "key_score": "room_cantina_pt_score", "key_ms": "room_cantina_pt_ms", "key_notes_extra": "room_cantina_pt_notes_extra", "help": "Valuta dimensioni, umidità, illuminazione, accessibilità, potenziale utilizzo.",
     "options": ["Spaziosa", "Piccola", "Asciutto", "Umida", "Finestra presente", "Senza finestra", "Illuminazione OK", "Illuminazione scarsa/assente", "Accesso comodo", "Accesso scomodo", "Utilizzabile come ripostiglio", "Utilizzabile per altro?", "Da sistemare", "Altro (vedi note extra)"]},
]


# --- Inizializzazione Session State ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.active_section = None # Traccia la sezione checklist attiva

    # Inizializza checklist (con multiselect e note extra)
    for section in checklist_data:
        for item in section["items"]:
            st.session_state[item["key_score"]] = 3
            st.session_state[item["key_ms"]] = [] # Multiselect inizia vuoto
            st.session_state[item["key_notes_extra"]] = ""

    # Inizializza valutazione stanze (con multiselect e note extra)
    for room in room_evaluation_data:
        st.session_state[room["key_score"]] = 3
        st.session_state[room["key_ms"]] = [] # Multiselect inizia vuoto
        st.session_state[room["key_notes_extra"]] = ""

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
# (Invariata)
def calculate_section_averages(data):
    # ... (codice identico a prima)
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


# --- Funzione per ottenere dati stanze per grafici ---
# (Invariata)
def get_room_scores(room_data):
    # ... (codice identico a prima)
    labels = []
    scores = []
    for room in room_data:
        score = st.session_state.get(room["key_score"], None)
        if isinstance(score, (int, float)):
            labels.append(room["name"])
            scores.append(score)
    return labels, scores


# --- Titolo e Info Generali ---
# (Invariato)
st.title(" Scheda Valutazione Visita Immobile")
st.header("Casalino Solfanuccio")
# ... (resto invariato)
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

            # Colonna per Punteggio
            col1, col_ms, col_notes = st.columns([1, 2, 1]) # Punteggio, Multiselect, Note Extra

            with col1:
                st.radio(
                    "Punteggio:",
                    options=[1, 2, 3, 4, 5],
                    key=item["key_score"],
                    horizontal=True,
                    on_change=set_active_section,
                    args=(section_key,),
                    help=item.get("help_text")
                )

            # Colonna per Multiselect
            with col_ms:
                 st.multiselect(
                     "Osservazioni Rapide:",
                     options=item.get("options", []), # Prende le opzioni dalla struttura dati
                     key=item["key_ms"], # Usa la nuova chiave per multiselect
                     label_visibility="collapsed",
                     default=st.session_state[item["key_ms"]], # Assicura che mantenga lo stato
                     on_change=set_active_section, # Mantiene l'expander aperto
                     args=(section_key,)
                 )

            # Colonna per Note Extra (opzionale)
            with col_notes:
                st.text_input(
                    "Note Extra:",
                    key=item["key_notes_extra"], # Usa la nuova chiave per note extra
                    placeholder="Dettagli...",
                    label_visibility="collapsed",
                    on_change=set_active_section, # Mantiene l'expander aperto
                    args=(section_key,)
                )

            st.markdown("---") # Divisore tra gli item

# --- Sezione Valutazione Stanze Specifiche (con Multiselect) ---
st.markdown("---")
st.subheader("Valutazione Stanze Specifiche")
for room in room_evaluation_data:
    st.markdown(f"**{room['name']}**")
    col1_room, col_ms_room, col_notes_room = st.columns([1, 2, 1])

    with col1_room:
        st.radio(
            "Punteggio Stanza:",
            options=[1, 2, 3, 4, 5],
            key=room["key_score"],
            horizontal=True,
            label_visibility="collapsed",
            help=room.get("help")
        )

    with col_ms_room:
        st.multiselect(
            "Osservazioni Stanza:",
            options=room.get("options", []),
            key=room["key_ms"],
            label_visibility="collapsed",
            default=st.session_state[room["key_ms"]]
        )

    with col_notes_room:
         st.text_input(
            "Note Extra Stanza:",
            key=room["key_notes_extra"],
            placeholder="Dettagli...",
            label_visibility="collapsed"
         )

    st.markdown("---") # Separatore tra stanze


# --- Sezione Riepilogo Generale ---
# (Invariato)
st.markdown("---")
st.header("Riepilogo e Impressione Generale")
# ... (resto invariato) ...


# --- Sezione Grafica Riassuntiva ---
# (Invariato)
st.markdown("---")
st.header(" Riepilogo Grafico")
# ... (resto invariato) ...


# --- Pulsante Riepilogo Testuale (Aggiornato per Multiselect) ---
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
            selected_options = st.session_state.get(item["key_ms"], []) # Prendi le opzioni selezionate
            extra_notes = st.session_state.get(item["key_notes_extra"], '') # Prendi le note extra
            score_str = f"`{score}`" if isinstance(score, (int, float)) else f"`{score}`"

            summary.append(f"- **{item['label']}:** Punteggio {score_str}")
            # Aggiungi le opzioni selezionate se ce ne sono
            if selected_options:
                summary.append(f"  *Osservazioni:* {', '.join(selected_options)}")
            # Aggiungi le note extra se presenti
            if extra_notes:
                notes_indented = "\n    ".join(extra_notes.strip().split('\n')) # Indenta di più le note extra
                summary.append(f"    *Note Extra:* {notes_indented}")
        summary.append("\n")

    # Dettaglio Valutazione Stanze
    summary.append("---\n## Valutazione Stanze Specifiche:\n")
    for room in room_evaluation_data:
        score = st.session_state.get(room["key_score"], 'N/D')
        selected_options = st.session_state.get(room["key_ms"], [])
        extra_notes = st.session_state.get(room["key_notes_extra"], '')
        score_str = f"`{score}`" if isinstance(score, (int, float)) else f"`{score}`"

        summary.append(f"### {room['name']}")
        summary.append(f"- **Punteggio:** {score_str}")
        if selected_options:
            summary.append(f"  *Osservazioni:* {', '.join(selected_options)}")
        if extra_notes:
            notes_indented = "\n    ".join(extra_notes.strip().split('\n'))
            summary.append(f"    *Note Extra:* {notes_indented}")
        summary.append("\n")


    # Riepilogo Generale
    summary.append("---\n## Riepilogo Generale")
    # ... (resto invariato) ...
    summary.append(f"**Punti di Forza:**\n{st.session_state.punti_forza}")
    summary.append(f"\n**Criticità / Dubbi:**\n{st.session_state.criticita}")
    summary.append(f"\n**Punteggio Complessivo:** `{st.session_state.impressione_generale}`")
    summary.append(f"\n**Prossimi Passi:**\n{st.session_state.prossimi_passi}")

    st.markdown("---")
    st.subheader("Riepilogo Completo (Markdown)")
    st.text_area("Copia questo riepilogo:", value="\n".join(summary), height=600)


# --- Nota sull'uso ---
st.sidebar.info(
    """
    **Come Usare:**
    1. Compila punteggio e seleziona osservazioni rapide per checklist e stanze.
    2. Aggiungi eventuali note extra nel campo apposito.
    3. La sezione checklist attiva rimarrà aperta.
    4. Passa sopra ❓ per dettagli.
    5. Visualizza i grafici.
    6. Usa "Mostra Riepilogo" per il report dettagliato.
    """
)
