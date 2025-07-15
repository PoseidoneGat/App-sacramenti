import webview
import logging
from typing import Dict, Optional

# ------------------------------------------------------------------------------

# 1. HTML/CSS/JS
# ------------------------------------------------------------------------------

html = '''
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <title>Sacramenti Poseidone</title>
  <style>
    :root {
      --bg: #f8f9fa;
      --text: #212529;
      --primary: #0d6efd;
      --secondary: #6c757d;
      --success: #198754;
      --danger: #dc3545;
      --warning: #ffc107;
      --info: #0dcaf0;
      --card-radius: 1rem;
      --modal-bg: rgba(0,0,0,0.75);
      --shadow: 0 .125rem .25rem rgba(0,0,0,.075);
      --transition: all 0.3s ease;
    }

    .dark {
      --bg: #212529;
      --text: #f8f9fa;
      --shadow: 0 .125rem .25rem rgba(255,255,255,.075);
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      transition: var(--transition);
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      line-height: 1.5;
    }

    header {
      padding: 1rem 1.5rem;
      display: flex;
      align-items: center;
      background: var(--bg);
      box-shadow: var(--shadow);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    header h1 {
      flex: 1;
      font-size: 1.5rem;
      font-weight: 600;
    }

    .price-btn {
      background: var(--danger);
      color: #fff;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      font-weight: 500;
      transform: translateY(0);
      box-shadow: var(--shadow);
    }

    .price-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 .5rem 1rem rgba(220,53,69,.15);
    }

    main {
      flex: 1;
      padding: 2rem;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
      align-items: start;
    }

    .card {
      border-radius: var(--card-radius);
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      background: linear-gradient(135deg, var(--start), var(--end));
      color: #fff;
      box-shadow: var(--shadow);
      transform: translateY(0);
      height: 100%;
    }

    .card:hover {
      transform: translateY(-5px);
      box-shadow: 0 1rem 3rem rgba(0,0,0,.175);
    }

    .card .icon {
      font-size: 3rem;
      margin-bottom: 1rem;
    }

    .card h2 {
      font-size: 1.25rem;
      margin-bottom: 0.5rem;
      font-weight: 600;
    }

    .card p {
      margin-bottom: 1.5rem;
      opacity: 0.9;
    }

    .card button {
      margin-top: auto;
      padding: 0.5rem 1.5rem;
      border: none;
      background: var(--warning);
      color: #000;
      border-radius: 0.5rem;
      font-weight: 500;
      transform: translateY(0);
    }

    .card button:hover {
      transform: translateY(-2px);
      box-shadow: 0 .5rem 1rem rgba(255,193,7,.15);
    }

    .info-btn {
      position: fixed;
      bottom: 2rem;
      left: 2rem;
      width: 3rem;
      height: 3rem;
      border-radius: 50%;
      background: var(--info);
      color: #fff;
      border: none;
      font-size: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow);
      transform: translateY(0);
    }

    .info-btn:hover {
      transform: translateY(-3px);
      box-shadow: 0 .5rem 1rem rgba(13,202,240,.15);
    }

    /* Modals */
    .modal {
      position: fixed;
      inset: 0;
      background: var(--modal-bg);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      backdrop-filter: blur(5px);
      user-select: text;  /* Permette la selezione del testo */
    }

    .modal-content {
      background: var(--bg);
      color: var(--text);
      padding: 1.5rem;
      border-radius: var(--card-radius);
      max-width: 600px;
      width: 100%;
      max-height: 90vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1rem 3rem rgba(0,0,0,.175);
      user-select: text;  /* Permette la selezione del testo */
    }

    .modal-body {
      flex: 1;
      white-space: pre-wrap;
      background: var(--bg);
      padding: 1rem;
      border-radius: 0.5rem;
      margin-bottom: 1rem;
      overflow: auto;
      border: 1px solid rgba(0,0,0,.1);
      user-select: text !important;  /* Forza la selezione del testo */
      -webkit-user-select: text !important;  /* Per Safari */
      -moz-user-select: text !important;     /* Per Firefox */
      -ms-user-select: text !important;      /* Per IE/Edge */
    }

    .dark .modal-body {
      border-color: rgba(255,255,255,.1);
    }

    .modal-content button {
      align-self: flex-end;
      padding: 0.5rem 1rem;
      border: none;
      background: var(--primary);
      color: #fff;
      border-radius: 0.5rem;
      font-weight: 500;
    }

    .modal-content button:hover {
      box-shadow: 0 .5rem 1rem rgba(13,110,253,.15);
    }

    /* Input styles */
    input[type="text"] {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid rgba(0,0,0,.1);
      border-radius: 0.5rem;
      margin-top: 0.25rem;
      background: var(--bg);
      color: var(--text);
    }

    .dark input[type="text"] {
      border-color: rgba(255,255,255,.1);
    }

    label {
      display: block;
      margin-top: 1rem;
      font-weight: 500;
    }

    /* Buttons container */
    .buttons-container {
      display: flex;
      justify-content: flex-end;
      gap: 0.5rem;
      margin-top: 1.5rem;
    }

    button {
      cursor: pointer;
      transition: var(--transition);
    }

    button:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }

    .switch {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-left: 1rem;
    }

    .switch input[type="checkbox"] {
      height: 0;
      width: 0;
      visibility: hidden;
    }

    .switch label {
      cursor: pointer;
      width: 48px;
      height: 24px;
      background: var(--secondary);
      display: block;
      border-radius: 100px;
      position: relative;
      margin: 0;
    }

    .switch label:after {
      content: '';
      position: absolute;
      top: 2px;
      left: 2px;
      width: 20px;
      height: 20px;
      background: #fff;
      border-radius: 90px;
      transition: var(--transition);
    }

    .switch input:checked + label {
      background: var(--primary);
    }

    .switch input:checked + label:after {
      left: calc(100% - 2px);
      transform: translateX(-100%);
    }
  </style>
</head>
<body>
  <header>
    <h1>⛪ Sacramenti Poseidone</h1>
    <button class="price-btn" onclick="showPriceList()">Listino Prezzi</button>
    <div class="switch">
      <input type="checkbox" id="darkMode" onchange="toggleDark(this)">
      <label for="darkMode"></label>
      Dark Mode
    </div>
  </header>

  <main id="cards"></main>

  <!-- Pulsante Info App -->
  <button class="info-btn" onclick="showAppInfo()">ℹ️</button>

  <!-- Modal di sola lettura -->
  <div id="modal" class="modal">
    <div id="modalContent" class="modal-content">
      <h3 id="modalTitle"></h3>
      <pre id="modalBody" class="modal-body"></pre>
      <button onclick="closeModal()">Chiudi</button>
    </div>
  </div>

  <!-- Modal di input per Battesimo e Matrimonio -->
  <div id="inputModal" class="modal">
    <div id="inputContent" class="modal-content">
      <h3 id="inputTitle"></h3>
      <div id="inputBody"></div>
      <div class="buttons-container">
        <button id="inputCancel" onclick="closeInputModal()">Annulla</button>
        <button id="inputConfirm" onclick="confirmInput()">Conferma</button>
      </div>
    </div>
  </div>

  <script>
    const services = [
      { key: 'battesimo',   icon: '🕊️', title: 'Battesimo',           desc: 'Accoglienza nella fede' },
      { key: 'matrimonio',  icon: '💒', title: 'Matrimonio',          desc: 'Unione davanti a Poseidone' },
      { key: 'cammino',     icon: '✨', title: "Cammino dell'Abisso", desc: 'Guida per il percorso' },
      { key: 'divinazione', icon: '🔮', title: 'Rivelazione Divina',  desc: 'Ricerca spirituale' },
      { key: 'confessione', icon: '🙏', title: 'Confessione',         desc: 'Confessa i peccati' },
      { key: 'unzione',     icon: '⚕️', title: 'Unzione',             desc: 'Sacramento degli infermi' }
    ];
    const colors = {
      battesimo:   ['#4FC3F7','#2196F3'],
      matrimonio:  ['#F06292','#F06292'],
      cammino:     ['#BA68C8','#AB47BC'],
      divinazione: ['#FF8A65','#FF7043'],
      confessione: ['#78909C','#37474F'],
      unzione:     ['#81C784','#66BB6A']
    };

    const container = document.getElementById('cards');
    services.forEach(s => {
      const card = document.createElement('div');
      card.classList.add('card');
      card.style.setProperty('--start', colors[s.key][0]);
      card.style.setProperty('--end',   colors[s.key][1]);
      card.innerHTML = `
        <div class="icon">${s.icon}</div>
        <h2>${s.title}</h2>
        <p>${s.desc}</p>
        <button onclick="openService('${s.key}')">Apri</button>
      `;
      container.appendChild(card);
    });

    function toggleDark(cb) {
      document.documentElement.classList.toggle('dark', cb.checked);
    }

    function showModal(title, body) {
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalBody').textContent = body;
      document.getElementById('modal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('modal').style.display = 'none';
    }

    let currentKey = '';

    function openService(key) {
      currentKey = key;
      if (key === 'battesimo' || key === 'matrimonio') {
        showInputModal(key);
      } else {
        window.pywebview.api.openCeremony(key)
          .then(res => showModal(res.title, res.content));
      }
    }

    function showInputModal(key) {
      const titleMap = {
        'battesimo': 'Battesimo – Dati',
        'matrimonio': 'Matrimonio – Dati'
      };
      document.getElementById('inputTitle').innerText = titleMap[key];
      const body = document.getElementById('inputBody');
      body.innerHTML = '';
      if (key === 'battesimo') {
        body.innerHTML = '<label>Nome del battezzando:</label><input id="inputNome" type="text">';
      } else {
        body.innerHTML = `
          <label>Nome sposo:</label><input id="inputSposo" type="text">
          <label>Nome sposa:</label><input id="inputSposa" type="text">
        `;
      }
      document.getElementById('inputModal').style.display = 'flex';
    }

    function closeInputModal() {
      document.getElementById('inputModal').style.display = 'none';
    }

    async function confirmInput() {
      let data = {};
      if (currentKey === 'battesimo') {
        data.nome = document.getElementById('inputNome').value.trim();
        if (!data.nome) { alert('Inserisci il nome'); return; }
      } else {
        data.sposo = document.getElementById('inputSposo').value.trim();
        data.sposa = document.getElementById('inputSposa').value.trim();
        if (!data.sposo || !data.sposa) { alert('Completa tutti i campi'); return; }
      }
      closeInputModal();
      const res = await window.pywebview.api.openCeremony(currentKey, data);
      showModal(res.title, res.content);
    }

    function showPriceList() {
      window.pywebview.api.openPriceList()
        .then(res => showModal(res.title, res.content));
    }

    function showAppInfo() {
      window.pywebview.api.openAppInfo()
        .then(res => showModal(res.title, res.content));
    }
  </script>
</body>
</html>
'''

# ------------------------------------------------------------------------------

# 2. API PYTHON
# ------------------------------------------------------------------------------

class Api:
    def __init__(self):
        self._texts_cache: Dict[str, str] = {}
        self._setup_logging()
        self.texts = {
            'cammino': '''[Si controlla se il fedele ha compiuto il sacramento del Battesimo sul /sacramenti info [NomePlayer]]

[Si fa pagare al fedele 250,00€]

[Si porta il fedele nella biblioteca e si comincia la lezione]

---------------------------------------------------------------------
                      COPIARE IL TESTO QUI SOTTO                           
---------------------------------------------------------------------

LEZIONE: La Natura e i Misteri di Poseidone e il Suo Legame con l'Unione

Benvenuti a questa lezione dedicata al cammino di devozione a Poseidone. 

Dopo aver ricevuto il battesimo, è naturale approfondire la conoscenza di questo potente dio del mare e comprendere il suo ruolo nella nostra vita, nelle unioni e nelle tradizioni. 

Poseidone, dio del mare, dei terremoti e dei cavalli, è una delle figure principali dell'Olimpo, simbolo delle forze selvagge e incontrollabili della natura, ma anche della calma profonda degli abissi marini. 

Questa dualità di potenza e tranquillità si riflette nel modo in cui Poseidone influenza le relazioni umane e, in particolare, i legami duraturi.

Come il mare, l'unione tra due persone è una danza continua tra momenti di tempesta e di pace, una comunione che richiede equilibrio e rispetto. 

Nella mitologia, il legame di Poseidone con la nereide Anfitrite, che divenne la sua regina, è un esempio dell’armonia tra nature diverse ma complementari. 

Il loro rapporto simboleggia l'accettazione reciproca, insegnandoci che una relazione prospera solo con impegno e con la volontà di comprendersi profondamente.

Attraverso i secoli, il culto di Poseidone ha lasciato un’impronta indelebile nella tradizione, e oggi scopriamo come il suo spirito aleggi ancora tra di noi, specialmente nelle acque che lo rappresentano. 

Chi abbraccia il culto di Poseidone si immerge nelle sue acque sacre per ascoltare i segreti e accettare l’ignoto, simboleggiando il rispetto per ciò che è insondabile e misterioso. 

La leggenda del "Libro dell'Abisso", un antico testo sommerso che si dice custodisca i misteri e le avventure di Poseidone, è il cuore di questa tradizione.

Questo libro, custodito negli abissi e protetto da creature marine, è accessibile solo ai più devoti in sogni o visioni.

Le storie contenute nel "Libro dell'Abisso" insegnano principi fondamentali della guida spirituale di Poseidone:
 il rispetto per il mare, la venerazione per il compagno o la compagna, e l'importanza dell'unione come legame eterno.

Onorando Poseidone come guardiano delle acque e delle anime, apprendiamo che l’amore e il matrimonio sono viaggi tanto vasti e profondi quanto l'oceano stesso, in cui esploriamo sia il mondo esterno sia i nostri più reconditi misteri.

In questa lezione, riflettiamo sull’essenza di Poseidone come guida e protettore dell’unità, ricordandoci che ogni legame umano, come il mare, è un equilibrio tra calma e forza, tra ciò che è manifesto e ciò che resta avvolto nei segreti degli abissi.
''',

            'divinazione': '''[Si controlla se il fedele ha compiuto i sacramenti del Battesimo e del Cammino dell’Abisso sul /sacramenti info [NomePlayer]]

[Si fa pagare il fedele 400,00€ alla cassa] 

[Si fa mettere il fedele davanti all’altare con il capo chinato]

---------------------------------------------------------------------
                      COPIARE IL TESTO QUI SOTTO                           
---------------------------------------------------------------------

In nome di Poseidone, Signore degli Oceani e Custode delle Correnti, oggi celebriamo il momento in cui ti avvicini al banchetto eterno del mare.
 
Questo dono sacro ti lega alle acque eterne, simbolo della forza e della misericordia del nostro Dio.
 
Sei pronto a ricevere il nutrimento divino e a unirti al flusso della sua grazia infinita?
(Rispondere: Sì, sono pronto a immergermi nelle sue acque eterne.)

Oggi Poseidone ti chiama a condividere il frutto delle sue maree. Questo dono è simbolo del suo potere che sostiene la vita e rinnova lo spirito. 
Accogli ora il nutrimento sacro, segno della sua comunione con te.
(Rispondere: Accolgo il dono di Poseidone con fede e gratitudine.)

Che le acque del Signore degli Oceani ti proteggano e ti guidino attraverso le tempeste della vita. Possa la sua benedizione scorrere dentro di te, portando forza, saggezza e pace. 

Vai ora in comunione con Poseidone, e che le sue onde ti accompagnino sempre.
(Rispondere: Che le onde di Poseidone mi guidino e il suo spirito viva in me.)''',

            'confessione': '''[Si controlla se il fedele ha compiuto il sacramento del Battesimo sul /sacramenti info [NomePlayer]]

[Si fa pagare il fedele 100,00€ alla cassa] 

[Si porta il fedele all’interno di una stanza privata dove nessuno puo’ sentire]

---------------------------------------------------------------------
                      COPIARE IL TESTO QUI SOTTO                           
---------------------------------------------------------------------

Celebrante: In nome delle acque infinite che tutto avvolgono, del moto eterno delle onde, e del profondo silenzio degli abissi, io, servo del Signore degli Oceani, ti accolgo. 

Celebrante: Figliulo, in questo sacro momento, poni la tua anima al cospetto di Poseidone, affinché le tue colpe possano essere lavate come sabbia dalla risacca. 

Celebrante: Lascia che i tuoi peccati scorrano come un fiume verso il mare, per essere purificati nell’immensità delle sue acque.

Celebrante: Ora, forza figliuolo, confessa i tuoi peccati.

Fedele: [Confessa i suoi peccati]

Celebrante: Le onde di Poseidone, misericordiose e potenti, ti avvolgano e ti purifichino. Possa il suo tridente guidarti verso porti sicuri e la sua forza proteggerti dalle tempeste. 

Celebrante: [/sacramenti aggiungi confession  *NomePlayer*]

Celebrante: Vai, redento, e che il mare della tua anima sia calmo e sereno. Amen.''',

            'unzione':     '''[Si controlla se il fedele ha compiuto il sacramento del Battesimo sul /sacramenti info [NomePlayer]] 

[Si fa pagare il fedele 150,00€ alla cassa] 

[Si fa mettere il fedele davanti all’altare con il capo chinato]

---------------------------------------------------------------------
                      COPIARE IL TESTO QUI SOTTO                           
---------------------------------------------------------------------

In nome del Signore degli Oceani, che regna sugli abissi e sulle tempeste, siamo qui riuniti per invocare la forza delle onde e il conforto delle acque eterne su di te.
 
Che il potere rigenerante del mare possa donarti pace e guarigione. Sei pronto ad accogliere l’abbraccio di Poseidone?
(Rispondere: Sì, sono pronto a immergermi nella sua misericordia.)

Azione: *azione* Versa olio benedetto sul capo del fedele 
Con quest’olio, simbolo delle maree che guariscono, e con quest’acqua, dono di Poseidone, io ti ungo. 

Che il suo potere rinnovi il tuo spirito e il tuo corpo, portandoti la calma dei fondali e la forza delle onde. Possa Poseidone, sovrano del mare eterno, sostenerti nel tuo viaggio.
(Rispondere: Che le acque mi rinforzino e le onde mi proteggano.)

Confida nel mare infinito e nella benevolenza del nostro Signore Poseidone. Ti affido alla corrente della sua grazia. Sei pronto a lasciare andare ogni timore, abbracciando il suo volere?
(Rispondere:  Lascio che la corrente mi guidi, confidando nella sua potenza.)

Poseidone, il signore delle maree, ti benedica e ti custodisca. Che la sua forza ti sostenga, che le sue acque ti purifichino e che la sua pace ti avvolga. 

Nel nome del Tridente eterno, vai in serenità e fiducia. Amen.
(Rispondere: Amen. Che le onde mi accompagnino.)
'''
        }

    def _setup_logging(self):
        """Configura il logging per l'API"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='sacramenti.log'
        )

    def _get_text(self, key: str) -> str:
        """Recupera il testo dalla cache o dal dizionario principale con gestione errori"""
        try:
            if key not in self._texts_cache:
                self._texts_cache[key] = self.texts.get(key, '')
            return self._texts_cache[key]
        except Exception as e:
            logging.error(f"Errore nel recupero del testo per {key}: {str(e)}")
            return ''

    def _validate_ceremony_data(self, key: str, data: Optional[dict]) -> tuple:
        """Valida i dati della cerimonia"""
        if key == 'battesimo':
            nome = data.get('nome', '').strip() if data else ''
            if not nome:
                return False, 'Nome non valido'
            return True, nome
        elif key == 'matrimonio':
            if not data or not all(k in data for k in ['sposo', 'sposa']):
                return False, 'Dati matrimonio incompleti'
            return True, (data.get('sposo', '').strip(), data.get('sposa', '').strip())
        return True, None

    def openCeremony(self, key: str, data: Optional[dict] = None) -> dict:
        """Gestisce l'apertura delle cerimonie con gestione errori migliorata"""
        try:
            key = str(key).lower().strip()
            valid, result = self._validate_ceremony_data(key, data)
            
            if not valid:
                return {'title': 'Errore', 'content': result}

            if key == 'battesimo':
                nome = result
                testo = f"""Oh Poseidone, dio delle acque inesplorate, accogli {nome} nei tuoi regni. Possa il suono delle onde sussurrare la sua connessione con l'oceano infinito, e possano le correnti misteriose guidarlo/la nel flusso della vita con saggezza e forza sovrannaturale.
 
Con queste acque sacre, benedette dalla tua presenza, immergiamo {nome} in un abbraccio simbolico del tuo regno marino. Che ogni goccia rappresenti un legame eterno tra la sua anima e il vasto mistero degli abissi che abiti.

Che il suo spirito sia temprato dall'immensità dell'oceano, e che possa affrontare le tempeste della vita con la stessa maestosità delle onde che danzano sotto la tua guida.

Nel nome di Poseidone, accogliamo {nome} come un/a figlio/a del mare, destinato/a a navigare le acque della vita con coraggio e determinazione. Che le tue acque lo/la guidino attraverso mari sereni e tempestosi, illuminando il suo cammino con la luce del tuo potere divino.

Come la luna governa il ritmo delle maree, così {nome} sarà guidato/a dalla forza dei cicli naturali e dalla tua protezione. Che la tua grazia lo/la avvolga come le correnti che dondolano delicatamente le creature marine, e che possa sempre percepire la tua presenza nel susseguirsi delle onde e nel richiamo del vento marino.

O Poseidone, signore delle profondità, accogli {nome} tra i tuoi protetti. Che questo battesimo nelle tue acque sacre sia un segno eterno della sua connessione con il regno marino. Possa navigare la vita con la forza delle tue correnti e l'ardore del tuo spirito. Che sia così!"""
                return {'title': 'Battesimo', 'content': testo}
            
            elif key == 'matrimonio':
                spos, sposa = result
                testo = f"""{spos} e {sposa} prendetevi la mano.
Ora legherò queste corde, mentre tutti noi auguriamo felicità alla coppia e alla loro unione in questo giorno.

Con la legatura di queste corde la coppia non è più composta da due entità separate, ma diviene una cosa sola, legata insieme dall’amore e dal rispetto reciproco.

Queste sono le mani del tuo migliore amico, giovani e forti e piene di amore per te, che stringono le tue nel giorno del tuo matrimonio, mentre promettete di amarvi oggi, domani e per sempre. 

Queste sono le mani che lavoreranno al anco delle tue, mentre costruite il vostro futuro insieme.

Queste sono le mani che ti ameranno appassionatamente e ti adoreranno nel corso degli anni e, con il minimo tocco, sapranno consolarti come nessun altro ha mai saputo fare.

Queste sono le mani che ti stringeranno quando la paura o il dolore pervaderanno i tuoi pensieri.                                                                                                                                                 

Queste sono le mani che asciugheranno le lacrime dai tuoi occhi; lacrime di dolore e, come oggi, lacrime di gioia.                                                                                                         

Queste sono le mani che ti daranno forza quando ne avrai bisogno. Queste sono le mani che ti ameranno e ti adoreranno nel corso degli anni, per una vita di felicità.

Queste sono le mani che ti daranno supporto sapendo che insieme, come una vera squadra, tutto ciò che desiderate può essere realizzato. Possano le vostre mani essere sempre strette l'una all'altra.

Nel luogo sacro della natura, sotto il cielo azzurro e la volta stellata, ci riuniamo per celebrare un rito sacro, un incontro di anime destinate a intrecciarsi nell'eternità.

Oh, potente Poseidone, dio dell'acqua, noi vi chiamiamo oggi per benedire questa unione sacra tra {spos} e {sposa}.

Che la terra sostenga i loro passi, che l'acqua purifichi le loro anime e porti il messaggio dell'amore eterno.

In questo cerchio magico, segnato dalla luce delle candele che simboleggiano la amma dell'amore divino, gli sposi si uniscono come due amme che si fondono in una sola.

La loro unione è un riflesso del ciclo eterno della vita, un'armonia di dualità che si completa e si rinnova.

Che il sole, simbolo di vita e rinascita, illumini il cammino di {spos} e {sposa}. Che la luna, regina della notte e della magia, vegli su di loro durante i momenti di oscurità. 

Possano gli astri, con il loro splendore invito, ispirare e guidare questa unione verso la grandezza e la saggezza.

Ora Poseidone vi rende partecipi dello stesso amore con cui egli ha amato la sua Chiesa, no a dare se stesso per lei. Vi chiedo pertanto di esprimere le vostre intenzioni.

Siete venuti a celebrare il Matrimonio senza alcuna costrizione, in piena libertà e consapevoli del signicato della vostra decisione? [Rispondere: Si, lo siamo.]

Siete disposti, seguendo la via del Matrimonio, ad amarvi e onorarvi l'un l'altro per tutta la vita, ad accogliere con amore i gli che Poseidone vorrà donarvi? [Rispondere: Si, lo siamo.]

{spos} vuoi accogliere {sposa} come tua sposa, promettendo di esserle fedele sempre, nella gioia e nel dolore, nella salute e nella malattia, e di amarla e onorarla tutti i giorni della tua vita? Sposo: [Rispondere: Sì. la voglio!]

{sposa} vuoi accogliere {spos} come tuo sposo, promettendo di esserle fedele sempre, nella gioia e nel dolore, nella salute e nella malattia, e di amarla e onorarla tutti i giorni della tua vita? Sposa: [Rispondere: Sì. lo voglio!]

Ora, con il potere di questo rito sacro, dichiaro {spos} e {sposa} legati in unione eterna.

Che il vostro cammino sia illuminato dalla luce dell'amore divino e che possano affrontare insieme ogni sfida con coraggio, compassione e comprensione. Benedizioni a questa unione sacra e a coloro che la celebrano. Che sia così!"""
                return {'title': 'Matrimonio', 'content': testo}
            
            elif key in self.texts:
                return {
                    'title': {
                        'cammino': "Cammino dell'Abisso",
                        'divinazione': "Rivelazione Divina", 
                        'confessione': "Confessione",
                        'unzione': "Unzione"
                    }.get(key, key.title()),
                    'content': self._get_text(key)
                }

            return {'title': 'Errore', 'content': 'Servizio non trovato'}
            
        except Exception as e:
            logging.error(f"Errore nella cerimonia {key}: {str(e)}")
            return {'title': 'Errore', 'content': f'Si è verificato un errore: {str(e)}'}

    def openPriceList(self):
        prezzi = (
            "Battesimo: 200€\n"
            "Cammino Spirituale: 250€\n"
            "Divinazione: 400€\n"
            "Confessione: 100€\n"
            "Unzione: 150€\n"
            "Matrimonio Default: 1200€\n"
            "Matrimonio Premium: 2250€\n"
            "Divorzio: 500€"
        )
        return {'title': 'Listino Prezzi', 'content': prezzi}

    def openAppInfo(self):
        contact = (
            "Contatti: @RicordiFelici\n"
            "kekkolona fa schifo\n"
            "HiroHito voglio 300k di stipendio\n"
        )
        version = "Versione: 1.0.1\n"
        # Solo info dell'app, niente testi sacramenti
        content = contact + "\n" + version
        return {'title': 'Info App & Versione', 'content': content}

def start_app():
    try:
        api = Api()
        window = webview.create_window(
            'Sacramenti Poseidone',
            html=html,
            js_api=api,
            width=800,
            height=700,
            min_size=(600, 400),
            resizable=True,
        )
        webview.start(debug=False)
    except Exception as e:
        logging.error(f"Errore durante l'avvio dell'app: {str(e)}")
        raise

if __name__ == '__main__':
    start_app()
