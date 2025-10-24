document.addEventListener('DOMContentLoaded', function() {
    // --- CONFIGURAZIONE (invariata) ---
    const googleSheetCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQRYZz5cm8M6XWpz9aFh62Pw-2q-7pIpViKFV_Zv4qlJMWYTQwg2zMW9L1U_s3QfPdrQtNPvmD8cBUx/pub?gid=62264278&single=true&output=csv";
    const eventiDaMostrare = ['mareggiate', 'vento'];

    const mappaColori = {
        "Rossa": "red",
        "Arancione": "orange",
        "Gialla": "yellow",
        "Verde": "green",
        "Nessuna": "green",
        "Bianca": "white"
    };

    const eventiInfo = {
        'idrogeologica': { testo: 'IDRO-GEOLOGICO', icona: 'idrogeologico.png' },
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

            eventiDaMostrare.forEach(evento => {
                const coloreItaliano = allerte[evento] || "Nessuna";
                const colore = mappaColori[coloreItaliano] || "green";
                const info = eventiInfo[evento];
                const testoPrimario = (colore === 'green' || colore === 'white') ? 'NO ALLARME' : 'ALLARME';
                const testoSecondario = info.testo;

                // *** INIZIO SEZIONE MODIFICATA ***
                // Qui creiamo la nuova struttura HTML che corrisponde al nuovo CSS.

                const divEvento = document.createElement('div');
                // L'evento ora non ha più il colore di sfondo, è solo un contenitore.
                divEvento.className = 'evento'; 
                
                // Creiamo l'innerHTML con la nuova struttura:
                // - Un .icona-container a cui diamo il colore di sfondo.
                // - Un .testo con due <span> interni per i colori separati.
                divEvento.innerHTML = `
                    <div class="icona-container ${colore}">
                        <img src="${info.icona}" class="icona" alt="Icona ${testoSecondario}">
                    </div>
                    <div class="testo">
                        <span class="testo-primario ${colore}-text">${testoPrimario}</span>
                        <span class="testo-secondario">${testoSecondario}</span>
                    </div>
                `;
                
                container.appendChild(divEvento);
                // *** FINE SEZIONE MODIFICATA ***
            });

        } catch (error) {
            console.error("Errore nel caricamento dei dati dal Google Sheet:", error);
            document.getElementById('container').innerHTML = '<div class="loading red">Errore nel caricamento dati.</div>';
        }
    }

    caricaEVisualizzaAllerte();
    setInterval(caricaEVisualizzaAllerte, 900000);
});
