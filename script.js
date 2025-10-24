document.addEventListener('DOMContentLoaded', function() {
    // --- CONFIGURAZIONE ---
    const googleSheetCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQRYZz5cm8M6XWpz9aFh62Pw-2q-7pIpViKFV_Zv4qlJMWYTQwg2zMW9L1U_s3QfPdrQtNPvmD8cBUx/pub?gid=62264278&single=true&output=csv";

    // *** MODIFICA CHIAVE ***
    // Inserisci in questa lista solo i nomi degli eventi per cui hai caricato l'icona.
    // Lo script mostrerà solo questi.
    const eventiDaMostrare = ['mareggiate', 'vento'];

    // Mappa per tradurre i valori del foglio (Italiano) nei nomi delle classi CSS (Inglese)
    const mappaColori = {
        "Rossa": "red",
        "Arancione": "orange",
        "Gialla": "yellow",
        "Verde": "green",
        "Nessuna": "green",
        "Bianca": "white"
    };

    // Le informazioni per tutti gli eventi rimangono qui, lo script sceglierà solo quelle necessarie
    const eventiInfo = {
        'idrogeologica': { testo: 'IDROGEOLOGICO', icona: 'idrogeologico.png' },
        'idraulica': { testo: 'IDRAULICO', icona: 'idraulico.png' },
        'temporali': { testo: 'TEMPORALI', icona: 'temporali.png' },
        'vento': { testo: 'VENTO', icona: 'vento.png' },
        'neve': { testo: 'NEVE', icona: 'neve.png' },
        'mareggiate': { testo: 'MAREGGIATE', icona: 'mareggiate.png' }
    };
    // --- FINE CONFIGURAZIONE ---


    async function caricaEVisualizzaAllerte() {
        try {
            const response = await fetch(googleSheetCsvUrl + '&_cacheBuster=' + new Date().getTime());
            
            if (!response.ok) {
                throw new Error(`Errore HTTP: ${response.status}`);
            }
            
            const datiCsv = await response.text();
            
            const righe = datiCsv.trim().split('\n');
            const header = righe[0].split(','); 
            const valori = righe[1].split(',');

            const allerte = {};
            header.forEach((titolo, index) => {
                const titoloPulito = titolo.trim().toLowerCase();
                allerte[titoloPulito] = valori[index].trim();
            });

            const container = document.getElementById('container');
            container.innerHTML = ''; 

            // *** MODIFICA CHIAVE ***
            // Il ciclo ora usa la nuova lista "eventiDaMostrare" invece di un elenco fisso.
            eventiDaMostrare.forEach(evento => {
                const coloreItaliano = allerte[evento] || "Nessuna";
                const colore = mappaColori[coloreItaliano] || "green";
                const info = eventiInfo[evento];
                const testoAllarme = (colore === 'green' || colore === 'white') ? 'NESSUN ALLARME' : 'ALLARME';

                const divEvento = document.createElement('div');
                divEvento.className = `evento ${colore}`;
                divEvento.innerHTML = `
                    <img src="${info.icona}" class="icona" alt="Icona ${info.testo}">
                    <p class="testo">${testoAllarme}<br>${info.testo}</p>
                `;
                container.appendChild(divEvento);
            });

        } catch (error) {
            console.error("Errore nel caricamento dei dati dal Google Sheet:", error);
            document.getElementById('container').innerHTML = '<div class="loading red">Errore nel caricamento dati.</div>';
        }
    }

    caricaEVisualizzaAllerte();
    setInterval(caricaEVisualizzaAllerte, 900000);
});
