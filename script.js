document.addEventListener('DOMContentLoaded', function() {
    // URL originale dell'API
    const apiUrl = "https://allertameteo.regione.marche.it/o/api/allerta/get-stato-allerta";
    
    // *** MODIFICA CHIAVE ***
    // Utilizziamo il proxy AllOrigins, che è più robusto e gestisce meglio i problemi di certificati SSL e CORS.
    const proxyUrl = 'https://api.allorigins.win/raw?url=';

    const areeDiInteresse = ["2", "4"];
    const gerarchiaColori = { "red": 4, "orange": 3, "yellow": 2, "green": 1, "white": 0 };

    const eventiInfo = {
        'idrogeologica': { testo: 'IDROGEOLOGICO', icona: 'idrogeologico.png' },
        'idraulica': { testo: 'IDRAULICO', icona: 'idraulico.png' },
        'temporali': { testo: 'TEMPORALI', icona: 'temporali.png' },
        'vento': { testo: 'VENTO', icona: 'vento.png' },
        'neve': { testo: 'NEVE', icona: 'neve.png' },
        'mareggiate': { testo: 'MAREGGIATE', icona: 'mareggiate.png' }
    };

    async function caricaEVisualizzaAllerte() {
        try {
            // La URL da chiamare ora è composta dal proxy + l'URL dell'API codificato
            const response = await fetch(proxyUrl + encodeURIComponent(apiUrl));
            
            if (!response.ok) {
                // Se la risposta non è OK, lancia un errore per attivare il blocco catch
                throw new Error(`Errore HTTP: ${response.status} ${response.statusText}`);
            }
            
            const dati = await response.json();
            
            const allerteFiltrate = dati.filter(item => areeDiInteresse.includes(item.area));
            const allerteFinali = {};
            for (const evento in eventiInfo) {
                allerteFinali[evento] = 'green';
            }

            allerteFiltrate.forEach(area => {
                area.eventi.split(',').forEach(e => {
                    const [tipo, colore] = e.split(':');
                    if (eventiInfo[tipo] && gerarchiaColori[colore] > gerarchiaColori[allerteFinali[tipo]]) {
                        allerteFinali[tipo] = colore;
                    }
                });
            });

            const container = document.getElementById('container');
            container.innerHTML = ''; 

            const ordineVisualizzazione = ['idrogeologica', 'idraulica', 'temporali', 'vento', 'neve', 'mareggiate'];

            ordineVisualizzazione.forEach(evento => {
                const colore = allerteFinali[evento];
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
            console.error("Errore nel caricamento dei dati di allerta:", error);
            document.getElementById('container').innerHTML = '<div class="loading red">Errore nel caricamento dati.</div>';
        }
    }

    caricaEVisualizzaAllerte();
    setInterval(caricaEVisualizzaAllerte, 900000); 
});
