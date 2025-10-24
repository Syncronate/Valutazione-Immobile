document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = "https://allertameteo.regione.marche.it/o/api/allerta/get-stato-allerta";
    
    // Usiamo Thingproxy perché è un proxy server che non è soggetto a restrizioni CORS
    const proxyUrl = 'https://thingproxy.freeboard.io/fetch/';

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
            const response = await fetch(proxyUrl + apiUrl);
            
            if (!response.ok) {
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
