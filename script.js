document.addEventListener('DOMContentLoaded', function() {
    // API per le allerte di oggi
    const apiUrl = "https://allertameteo.regione.marche.it/o/api/allerta/get-stato-allerta";
    
    // Proxy per superare problemi di sicurezza (CORS e SSL)
    const proxyUrl = 'https://api.allorigins.win/raw?url=';

    // Configurazioni del widget
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

    // Funzione principale che carica e visualizza i dati
    async function aggiornaAllerte() {
        try {
            // 1. Contatta l'API
            const response = await fetch(proxyUrl + encodeURIComponent(apiUrl));
            if (!response.ok) throw new Error(`Errore HTTP: ${response.status}`);
            const datiApi = await response.json();
            
            // 2. Elabora i dati ricevuti
            const allerteFiltrate = datiApi.filter(item => areeDiInteresse.includes(item.area));
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

            // 3. Visualizza i risultati (METODO CORRETTO E STABILE)
            const container = document.getElementById('container');
            container.innerHTML = ''; // Pulisce la visualizzazione

            const ordineVisualizzazione = ['idrogeologica', 'idraulica', 'temporali', 'vento', 'neve', 'mareggiate'];
            
            ordineVisualizzazione.forEach(evento => {
                const colore = allerteFinali[evento];
                const info = eventiInfo[evento];
                const testo = (colore === 'green' || colore === 'white') ? 'NESSUN ALLARME' : 'ALLARME';
                
                // Crea un nuovo elemento div per ogni allerta
                const divEvento = document.createElement('div');
                divEvento.className = `evento ${colore}`;
                divEvento.innerHTML = `
                    <img src="${info.icona}" class="icona" alt="Icona ${info.testo}">
                    <p class="testo">${testo}<br>${info.testo}</p>
                `;
                // Aggiunge l'elemento creato al contenitore
                container.appendChild(divEvento);
            });

        } catch (error) {
            console.error("Errore nel caricamento dei dati di allerta:", error);
            document.getElementById('container').innerHTML = '<div class="loading red">Errore nel caricamento dati.</div>';
        }
    }

    // Esegui la funzione all'avvio e poi ogni 15 minuti
    aggiornaAllerte();
    setInterval(aggiornaAllerte, 900000); 
});
