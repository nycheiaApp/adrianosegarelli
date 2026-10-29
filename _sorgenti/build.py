# Genera tutte le pagine del sito. Uso: python3 build.py   (dalla cartella _sorgenti)
# I contenuti (testi, eventi, opere) stanno in questo file nella sezione DATI: si modificano qui e si rigenera.
import json, html, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
E = html.escape

# ───────────────────────────── DATI ─────────────────────────────
NOME = "Adriano Segarelli"
EMAIL = "adrianosegarelli.art@gmail.com"
INSTAGRAM = "https://www.instagram.com/adrianosegarelli/"
BEHANCE = "https://www.behance.net/adrianosegarel"
PORTFOLIO = "https://nycheiaapp.github.io/ASPortfolio/"
LINK_SCULTURE = "https://nycheiaapp.github.io/iltempodellaforma"
LINK_AFFRESCO = "https://nycheiaapp.github.io/strappodiaffresco/#top"

MENU = [("biografia","Biografia"),("pittura","La mia pittura"),("affresco","L'affresco"),
        ("sculture","Le mie sculture"),("libri","I miei libri"),("esperienze","Esperienze"),("contatti","Contatti")]

BIOGRAFIA = [
 "Sono nato a Roma nel 1978, ho frequentato l’Istituto Statale d’Arte Silvio D’Amico e da oltre vent’anni esprimo il mio linguaggio nell’arte attraverso la pittura, la scultura e la pubblicazione di libri.",
 "La mia pittura si sviluppa su un figurativo che porta alla memoria canoni novecenteschi e talvolta soggetti classici sporcati da un tocco contemporaneo. Riferimenti al mito evidenziano gli stati emotivi dell’uomo attraverso le fragilità delle varie divinità rappresentate.",
 "Questa ricerca si sviluppa attraverso un forte concetto metafisico, caratterizzato da figure squarciate da una luce quasi teatrale che mostrano la loro piena espressività in uno spazio surreale. Un luogo – non luogo dove le figure si muovono in maniera arbitraria cercando punti di luce che possa loro indicare la via d’uscita. Che possa dare loro le risposte ai più profondi quesiti della vita. Talvolta rivolte verso un buio che delinea un vuoto apparente, proprio lì dove verosimilmente c’è la necessità di cercare.",
 "Il percorso pittorico viene scandito negli anni da figure femminili dalla forte poetica ispiratrice che, per me, rappresentano in realtà l’altra parte dell’uomo, quella parte più fragile e sensibile e di conseguenza più comunicativa.",
 "Il soggetto femminile, attraverso pose quasi statiche, espressioni rigide e sguardi rivolti in uno spazio vuoto, perdono la loro forma estetica e si trasformano in uno strumento attraverso il quale tutti i sentimenti dell’essere umano vengono veicolati in modo rapido e diretto.",
 "Un istinto interiore che trova la sua creatività in opere che nascono dalle varie emozioni e da tutti quegli stati d’animo che mutano continuamente. Una ricerca ossessiva senza sosta che punta alla vera essenza dell’animo umano.",
 "L’esigenza comunicativa attraverso il linguaggio del corpo prende forma anche nella scultura, rappresentando e interpretando con la lavorazione della creta la parte emozionale, i disagi e i sentimenti racchiusi dell’uomo.",
 "Un “non finito” dove gli arti si decostruiscono plasmandosi nella materia composta da terre crude, paste grezze e stucchi. Le sculture volutamente non subiscono processi di cottura per un concetto basato su un naturale deterioramento nel tempo della creta, che rimane al suo interno un elemento vivo che proviene dal fiume."
]
# Ordine delle schede: dal tema con le opere piu' vecchie al piu' recente (anno mediano delle opere del tema nel foglio Pittura; a parita', anno medio).
TEMI = [("deserti","Deserti urbani"),("destrutturalismo","Destrutturalismo interiore"),("pensieri","Pensieri nell'ombra"),("ombre","Metafisica delle ombre"),("io-sospeso","Io sospeso"),("metafisica","Metafisica della luce"),("mito","Mito")]
# Descrizioni dei temi (foglio Tema). Status "N" = non pubblicare. Tema senza testo (o con lorem ipsum) = "Testo in arrivo".
TEMI_TESTI = {
 "destrutturalismo": [
  "L'identità umana viene frammentata e ricomposta attraverso il caos emotivo. Si esprime una sensibilità acuta verso la solitudine e la malinconia, utilizzando volti che emergono e si dissolvono in fondali astratti per simboleggiare la precarietà dell'io. La tecnica materica, con pennellate violente e colori che colano come ricordi sbiaditi, rivela un animo tormentato che cerca ordine nel disordine. C'è una tensione costante tra il realismo dei tratti somatici e l'astrazione dell'ambiente, a indicare il conflitto tra la realtà esterna e il turbolento mondo interiore. Le figure, spesso isolate o senza volto, parlano di un'alienazione moderna e di una ricerca di sé che passa attraverso la distruzione delle certezze. In definitiva, non sono dipinte persone, ma stati d'animo: l'eco di un pensiero, il peso di un'assenza e la bellezza cruda della vulnerabilità psicologica."
 ],
 "io-sospeso": [
  "La pittura figurativa e metafisica di Adriano Segarelli evoca un contatto concettuale, con il risultato di suscitare la curiosità di inseguire un pensiero, un’idea che va oltre l’aspetto pittorico dell’opera d’arte. Nelle sue opere, caratterizzante è l’approccio con il pensiero che si aggroviglia con la forma, con la struttura, con i colori e con il significato ultimo che l’artista vuole associare alle sue figure.",
  "Adriano Segarelli è un pittore che si esprime attraverso tre mezzi comunicativi, la pittura, la scultura e la scrittura. Può essere definito come quell’artista che lavora per associazioni di immagini con un suo universo semantico che supera l’opera d’arte. L’artista, attraverso le sue opere, segue lo sviluppo del pensiero nella sua formazione nella mente umana nel tentativo di catturare i fattori che lo determinano. Come afferma De Chirico:",
  "“La forma corrente del pensiero umano è l’immagine visibile e questa a sua volta è formata dalle impressioni sensoriali che la mente riceve, le immagini esistenti del nostro spirito raffigurano dei concetti, dei sentimenti o delle idee metafisiche”.",
  "A tal proposito le sue opere sono rappresentazioni connotate da una tavolozza di colori decisamente fauves. Esiti pittorici in armonia con il movimento futurista che si esprimeva con queste parole riguardo al cromatismo pittorico:",
  "“Tutti si accorgeranno che sotto la nostra epidermide non serpeggia il bruno, ma che vi splende il giallo, che il rosso vi fiammeggia, e che il verde, l’azzurro e il violetto vi danzano, voluttuosi e carezzevoli! Come si può ancora veder roseo un volto umano […]? Il volto umano è giallo, è rosso, è verde, è azzurro, è violetto». (Manifesto tecnico del movimento futurista).",
  "[Nota critica di Carmen D’ANTONINO]"
 ],
 "metafisica": [
  "Nella metafisica c'è la ricerca della realtà assoluta delle cose, al di là della loro apparenza, attraverso un processo estremamente interiore basato non sull'esperienza vissuta ma su un punto di vista profondo e intuitivo nei confronti di questo infinito contenitore di energia che è l'universo.",
  "Nella versione metafisica la luce non appare più come un fenomeno fisico, non più come una reazione elettromagnetica assorbita o riflessa dalle cose, bensì assume un ruolo rivelatore. Uno strumento empirico che svela quella parte più nascosta e profonda della coscienza umana.",
  "Una forza ancestrale e indomabile che non si limita ad accendere e a definire le forme, ma sopraggiunge per squarciare un buio apparentemente predominante, in spazi verosimilmente vuoti. La luce giunge quindi non ad evidenziare il vuoto, ma fa sì che il buio stesso riempia uno spazio che altrimenti sarebbe stato vuoto senza luce.",
  "Una riflessione filosofica che inequivocabilmente approda nella visione metafisica di Silvano Petrosino: \"il soggetto umano non è solo illuminato, come il semplice oggetto, ma è egli stesso luce, è egli stesso illuminante: lo sguardo è la luce con la quale egli illumina e va incontro alla realtà che gli viene incontro\"."
 ],
 "ombre": [
  "Nella metafisica delle ombre, le sagome sono ombre viventi. Sono la proiezione di tutti gli interrogativi dell’essere umano. Muovendosi su spazi surreali, all’infinita ricerca di una risposta interiore, si collocano in un luogo non definito, consce di essere parte integrante di tutto ciò che le circonda. Consapevoli della loro risolutezza, si fondono col tutto sapendo che il tutto nasce dalle viscere del proprio inconscio."
 ],
 "deserti": [
  "Deserti urbani descrive un'anima profondamente introspettiva e malinconica, una osservazione silenziosa che coglie l'essenza della solitudine nella folla. Le opere rivelano una sensibilità tattile per l'atmosfera, dove la pioggia e i riflessi non sono solo elementi meteorologici, ma stati d'animo: la nostalgia di un ricordo o la speranza di un incontro. La scelta di rappresentare figure umane come sagome anonime, quasi ombre, suggerisce una visione esistenzialista, dove l'individuo è piccolo di fronte all'immensità architettonica, eppure non è mai del tutto solo. C'è una musicalità di fondo, quasi jazzistica in alcune opere che traduce un temperamento romantico e sognatore, capace di trovare bellezza nel grigio e nel crepuscolo. In definitiva, emerge un creatore che cerca ordine nel caos urbano, trasformando la metropoli in un luogo di contemplazione interiore, dove il silenzio parla più forte del rumore."
 ],
 "mito": [
  "Il Mito percorre il linguaggio di un'anima profondamente introspettiva, sospesa in un eterno dialogo tra il sacro e il profano, attratta inevitabilmente dai grandi misteri della transizione e dell'aldilà. Le opere esprimono un temperamento malinconico e solenne, capace di evocare atmosfere oniriche dove il confine tra realtà e mito si dissolve in nebbie grigie e tempestose. C'è una ricerca ossessiva della luce in mezzo all'oscurità, simbolo di una speranza tenace o di una rivelazione divina che emerge faticosamente dal caos interiore. Le figure riflettono un senso di esilio spirituale e di profonda solitudine esistenziale. Mito non esprime semplicemente scene narrative, ma stati d'animo puri: il silenzio dell'attesa, il peso del destino e la bellezza tragica dell'effimero. È una visione dalla sensibilità romantica e quasi gotica, che cerca la verità non nella chiarezza assoluta, ma nelle ombre profonde e silenziose dell'esistenza umana."
 ],
 "pensieri": [
  "L'osservazione silenziosa ed empatica che scava oltre la superficie delle cose. Il contrasto tra luce e ombra, metafora visiva dell'interiorità, mostra la perenne lotta tra il razionale e l'emotivo. Dalle frasi poetiche che accompagnano i ritratti emerge una filosofia di vita introspettiva: il buio non è vuoto, ma un grembo fertile dove i sensi si annullano per lasciare spazio al \"sentire\" puro. Si valorizza l'invisibile, credendo fermamente che la vera connessione umana e la vera visione avvengano attraverso il cuore e non attraverso gli occhi. Diario intimo, un invito a non temere l'oscurità interiore, ma a usarla come sfondo per far risaltare la luce dei propri sentimenti più autentici."
 ]
}

# Eventi (skill as-rassegna-stampa): (anno, tipologia, titolo, luogo · sede, descrizione, link alla fonte). Status "N" = non pubblicato. Nell'elenco: dal più recente.
EVENTI = [
 [
  "2020",
  "Documentazione Artistica",
  "L'abbandono di un abbraccio",
  "Terni · Piazza del Mercato",
  "PDF istituzionale con biografia e schede delle opere \"L'abbandono di un abbraccio\" e \"L'ombra dei sussurri\", con note critiche sulla sua poetica.",
  "https://bct.comune.terni.it/sites/default/files/adriano_segarelli.pdf"
 ],
 [
  "2021",
  "Personale d'arte",
  "Destrutturalismo interiore",
  "Roma · Ex Mattatio - Testaccio",
  "Mostra personale all'Ex Mattatoio di Testaccio con oltre 20 opere tra tele e sculture dedicate a questa nuova corrente artistica da lui fondata.",
  "https://www.arte.it/calendario-arte/roma/mostra-adriano-segarelli-destrutturalismo-interiore-77955"
 ],
 [
  "2021",
  "Personale d'arte",
  "Destrutturalismo interiore",
  "Roma · Ex Mattatio - Testaccio",
  "Scheda evento dettagliata della mostra all'Ex Mattatoio, che spiega il concetto di decostruzione della forma per rivelare l'interiorità.",
  "https://segnonline.it/events/adriano-segarelli-destrutturalismo-interiore/"
 ],
 [
  "2021",
  "Personale d'arte",
  "Destrutturalismo interiore",
  "Roma · Ex Mattatio - Testaccio",
  "Report sul successo della mostra all'Ex Mattatoio, spiegando il movimento che \"smonta\" la forma del corpo dall'interno per rivelare le emozioni.",
  "https://www.eventiculturalimagazine.com/arte-e-cultura/successo-adriano-segarelli-meetart-al-ex-mattatoio/"
 ],
 [
  "2021",
  "Collettiva d'arte",
  "ONYRICON. La pittura sogna",
  "Zagarolo (Roma) · Palazzo Rospigliosi",
  "La mostra, dal titolo “Onyricon – la pittura sogna”, è un invito ad abbandonarsi nel gioco di materia e pensiero, alla ricerca di sfumature di esistenza, sospesi tra esperienza immaginifica ed azione concreta, ragione ed irrazionale, inquietudine e stasi, nell’abbraccio con il mondo onirico.",
  "https://www.exibart.com/evento-arte/onyricon-la-pittura-sogna/"
 ],
 [
  "2021",
  "Collettiva d'arte",
  "Arte.Uomo.Natura.3 - arte contemporanea e letteratura",
  "Bolognano (PE) · Santa Maria Entroterra",
  "Articolo presentazione evento ARTE.UOMO.NATURA.3 mostra d’arte contemporanea e incontri letterari",
  "https://www.notizienazionali.it/notizie/attualita/30878/arte-pittura-installazioni-scultura-natale-mostra-inclusione-scrittura-love-amore"
 ],
 [
  "2022",
  "Collettiva d'arte",
  "Künste 2022 - Ausgang24",
  "Roma · Galleria dei Miracoli",
  "Recensione della mostra collettiva presentata dall'hub artistico sperimentale Ausgang24, co-fondato da Adriano Segarelli e Dario Pellegrino.",
  "https://theparallelvision.com/2022/03/23/kunste-ausgang24-mostra-collettiva/"
 ],
 [
  "2022",
  "Personale d'arte",
  "Memory & Tremor",
  "Milano · Brera - ex studio Piero Manzoni",
  "Mostra personale che indaga la memoria e il tremore interiore attraverso la pittura figurativa e metafisica dell'artista.",
  "https://www.juliet-artmagazine.com/adriano-segarelli-memory-tremor/"
 ],
 [
  "2022",
  "Personale d'arte",
  "L'Io Sospeso",
  "Isernia · Galleria Spazio Arte Petrecca",
  "Mostra alla Galleria Spazio Arte Petrecca. Nota critica che analizza il contatto concettuale tra pittura figurativa e metafisica, con riferimenti a De Chirico.",
  "https://www.aboutartonline.com/lio-sospeso-di-adriano-segarelli-tra-figurativo-e-metafisico-alla-galleria-spazio-arte-petrecca-isernia-dal-18-novembre-al-3-dicembre/"
 ],
 [
  "2022",
  "Personale d'arte",
  "Mobilitazioni Interiori",
  "Pescara · Ci vuole un villaggio aps-ArtGallery",
  "Evento di arte pubblica e flashmob che coinvolge la comunità attraverso il linguaggio artistico di Segarelli, incentrato sulla mobilitazione delle emozioni.",
  "https://abruzzo.life/2022/01/27/adriano-segarelli-presenta-flashmob_mobilitazioni-interiori/"
 ],
 [
  "2022",
  "Collettiva d'arte",
  "Festa del Cinema di Roma 17th edition",
  "Roma · Acquario Romano",
  "“PROIEZIONI” architettura, cinema e arte",
  "https://www.artelive360.it/cosa-facciamo/proiezioni-artistiche/"
 ],
 [
  "2023",
  "Premio Combat 2023",
  "Premio Combat 2023 14th edition",
  "Livorno · Museo G. Fattori",
  "Pagina dedicata alla partecipazione dell'artista al prestigioso Premio Combat, riconoscimento di rilievo nell'arte contemporanea italiana.",
  "https://www.premiocombat.it/2023/adriano-segarelli-97433"
 ],
 [
  "2023",
  "Collettiva d'arte",
  "Exibart",
  "Roma · Bar del Fico",
  "Pagina artista su Exibart.com con focus sulle opere dall'atmosfera vibrante e sospesa e aggiornamenti sulla produzione contemporanea.",
  "https://www.exibart.com/evento-arte/adriano-segarelli/"
 ],
 [
  "2023",
  "Premiazione Premio Pittura",
  "Premio Pittura Amedeo Modigliani",
  "Roma · Fondazione Modigliani",
  "Pagina ufficiale della Fondazione Amedeo Modigliani che elenca Adriano Segarelli come vincitore assoluto nella categoria Pittura per l'anno 2023.",
  "https://fondazioneamedeomodigliani.org/premiazioni-fondazione-amedeo-modigliani/"
 ],
 [
  "2024",
  "Lux mentis - Profilo Artista RAW",
  "Roma Art Week 11th edition",
  "Roma · Palazzo Velli expo",
  "L'arte non appartiene agli artisti... è di tutti coloro che sanno cogliere l'essenza di ciò provano nell'ammirarla Profilo biografico completo: stile tra figurativo e metafisica, tecniche (olio, creta, affresco), romanzi pubblicati e ruolo di co-fondatore di Ausgang24.",
  "https://romeartweek.com/it/artisti/?code=LOAAXI"
 ],
 [
  "2024",
  "Personale d'arte",
  "Metafisica della Luce",
  "Roma · Fondazione Modigliani",
  "Articolo su Artribune dedicato alla mostra personale dell'artista in qualità di vincitore del Premio Fondazione Amedeo Modigliani 2023.",
  "https://www.artribune.com/mostre-evento-arte/premio-fondazione-amedeo-modigliani-adriano-segarelli/"
 ],
 [
  "2024",
  "Collettiva d'arte",
  "Unerwartet",
  "Roma · Segarelli art Studio",
  "Mostra collettiva del 14 dicembre presso Adriano Segarelli Art Studio, con talk, musica e presentazione della produzione metafisica dell'artista.",
  "https://www.exibart.com/evento-arte/unerwartet/"
 ],
 [
  "2024",
  "Collettiva d'arte",
  "Touch of Light",
  "Roma · Segarelli art Studio",
  "Mostra del Collettivo Lux Mentis (21-26 ottobre) presso lo studio dell'artista, incentrata sulle variazioni della luce e atmosfere metafisiche.",
  "https://www.exibart.com/evento-arte/touch-of-light/"
 ],
 [
  "2024",
  "Personale d'arte",
  "Mostre in Studio",
  "Roma · Segarelli art Studio",
  "Pagina ufficiale dello studio e galleria d'arte di Segarelli, con l'elenco degli eventi ospitati (Unerwartet, Touch of Light).",
  "https://www.exibart.com/museo-galleria-arte/adriano-segarelli-art-studio/"
 ],
 [
  "2024",
  "Personale d'arte",
  "Metafisica della Luce",
  "Roma · Fondazione Modigliani",
  "Scheda evento della mostra personale tenutasi presso la Fondazione Amedeo Modigliani in Trastevere, dedicata ai vincitori del premio 2023.",
  "https://www.artrabbit.com/events/adriano-segarelli-metafisica-della-luce?__cc=1"
 ],
 [
  "2024",
  "Intervista",
  "Because the Art",
  "Roma",
  "Articolo che definisce Segarelli \"l'artista più rock dell'anno\", approfondendo la sua vittoria al Premio Modigliani 2023 e la ricerca sulla luce.",
  "https://www.controluce.it/because-the-art-adriano-segarelli-lartista-piu-rock-dellanno/"
 ],
 [
  "2024",
  "Personale d'arte",
  "Metafisica della luce",
  "Roma · Fondazione Amedeo Modigliani",
  "Annuncio della mostra personale alla Fondazione Amedeo Modigliani, lodando la capacità dell'artista di trattare temi universali con originalità.",
  "https://www.oggiroma.it/eventi/mostre/adriano-segarelli-metafisica-della-luce/76925/"
 ],
 [
  "2024",
  "Personale d'arte",
  "Luci Interiori",
  "Pescara · Ci vuole un villaggio aps-ArtGallery",
  "Mostra personale presso Ci vuole un villaggio aps-ART Gallery, con opere che rientrano nel filone del destrutturalismo come flusso eruttivo di emozioni.",
  "https://www.ladolcevita.tv/luci-interiori-adriano-segarelli/"
 ],
 [
  "2024",
  "Personale d'arte",
  "Luci interiori",
  "Pescara · Ci vuole un villaggio aps-ArtGallery",
  "Articolo locale sull'inaugurazione della mostra personale dell'artista, premiato come Vincitore Pittura 2023 dalla Fondazione Amedeo Modigliani.",
  "https://abruzzo.life/2024/02/01/luci-interiori-di-adriano-segarelli-a-pescara/"
 ],
 [
  "2025",
  "Personale d'arte",
  "Oltre, La Metafisica della Luce",
  "Roma · Villino Hernandez",
  "Mostra inaugurata presso la Sede SanPaolo Invest (Villino Hernandez), esplorando la luce come realtà assoluta oltre l'apparenza fisica.",
  "https://www.agenziacomunica.net/2025/09/11/la-mostra-pittorica-oltre-la-metafisica-della-luce-di-adriano-segarelli/"
 ],
 [
  "2025",
  "Collettiva d'arte",
  "Mythos - Viaggio nel mito contemporaneo",
  "Firenze · Fondazione Bellini",
  "Partecipazione su invito MYTOS, il primo percorso espositivo organizzato presso la Fondazione BELLINI e proposto da ELITE MUNDILIVE che celebra appunto l’essenza del Mito stesso in chiave contemporanea.",
  "https://iltaccodibacco.it/en/toscana/eventi/303495.html"
 ],
 [
  "2025",
  "Collettiva d'arte",
  "Premio Point de vue",
  "Zagarolo (Roma) · Palazzo Rospigliosi",
  "Riconoscimento ricevuto alla inaugurazione della mostra d'arte contemporanea \"Un battito di ciglia\" a palazzo Rospigliosi di Zagarolo.",
  "https://www.juliet-artmagazine.com/events/aa-vv-un-battito-di-ciglia/"
 ]
]

# Libri (foglio Libri): (anno, titolo, sinossi, link carta, link digitale, status).
# Si pubblicano solo i libri con status diverso da "N". Cella vuota = pulsante non attivo.
# "Opera in ristampa" (in una delle due colonne) = niente pulsanti, appare il testo.
LIBRI = [
 [
  "2024",
  "L'interpretazione della vita",
  "Roma, 2041. Rachele compie vent’anni. Appartiene, come tutte le persone della sua età, alla generazione post-pandemia. È cresciuta e vive in un mondo ormai caratterizzato da un’enorme distanziamento sociale. La causa di questo cambiamento fu un virus che, vent’anni prima, costrinse tutta la popolazione a non uscire di casa. Furono emanati dal governo dei decreti legge, che prevedevano rigidi divieti e restrizioni, applicati per evitare i contagi e limitare il più possibile le vittime di quel terribile micro organismo. Il mondo durante quel periodo si ritrovò lontano dagli affetti e dalla vita sociale e si abituò, così nel tempo, a quella condizione di distanziamento, ritrovandosi a vivere in quel modo come fosse ormai la normalità. In questo futuro distopico le persone svolgono qualsiasi attività direttamente dalla propria abitazione e le città sono diventate dei fatiscenti deserti urbani. Tecnologie avanzate hanno preso il posto di qualsiasi essere umano. Sofisticati programmi simulano aggregazioni sociali, attraverso la creazione di ologrammi identici agli eventuali partecipanti che, al contrario del loro alter ego digitale, restano comodamente a casa.",
  "https://www.ibs.it/interpretazione-della-vita-libro-adriano-segarelli/e/9788833437323#:~:text=Descrizione.%20Roma,%202041.%20Rachele%20compie%20vent%E2%80%99anni.",
  "",
  ""
 ],
 [
  "2020",
  "L'ignoto protagonista della storia",
  "Alessandro è uno scrittore in erba alle prese col suo primo romanzo autobiografico.\nComincerà ad avere enormi difficoltà nel trovare il finale della storia nel momento in cui inizierà a provare nostalgia per i personaggi, persone che hanno fatto parte realmente della sua vita e che non è più riuscito a risanare con loro vecchi rancori del passato.\nQuesta sua crisi lo porterà ad allontanarsi dalla sua compagna, Beatrice, che si sentirà trascurata dalle sue disattenzioni.\nQuesto romanzo scorrerà alternandosi tra la sua vita presente e tutto ciò che ha vissuto nel suo passato.\nCercherà di ricontattare i suoi personaggi per tentare di risanare il loro vecchio rapporto e per tentare di trovare il suo finale.\nAlessandro si renderà conto che la sua crisi non è nata per caso e capirà che dietro alla non riuscita della sua opera c’è una vera e propria cospirazione. Tutto ciò lo trascinerà in un vortice di sospetti e incomprensibili eventi, che lo condurranno verso una difficilissima ricerca della verità, scoprendo cose delle persone che hanno ruotato nella sua vita del tutto inimmaginabili.\nE quando crederà di aver trovato la soluzione a questo enigma e la tanto attesa fine del romanzo, qualcosa metterà in dubbio nuovamente il finale della storia.",
  "https://www.libreriauniversitaria.it/ignoto-protagonista-storia-segarelli-adriano/libro/9788833432717",
  "https://www.libreriauniversitaria.it/ignoto-protagonista-storia-segarelli-adriano/libro/9788833432717",
  ""
 ],
 [
  "2019",
  "L'uomo che vedeva opaco",
  "Vivere una seconda opportunità, conservando memoria e consapevolezza della precedente esistenza: un’utopia, un sogno irrealizzabile, una possibilità inquietante. Basato sulla teoria del multiverso, il romanzo di Segarelli racconta il percorso di un uomo che ha una grandiosa rivelazione e scopre di aver vissuto una vita parallela. Conoscendo la più importante verità del cosmo si connetterà alla sua coscienza giunta dal passato nella nuova dimensione e avrà l’opportunità di portare a termine ciò che non ha potuto realizzare nella sua vita precedente.",
  "Opera in ristampa",
  "",
  ""
 ],
 [
  "2022",
  "Dal punto di vista",
  "E se dopo il lockdown 2020, le persone non fossero mai tornate alla normalità? Siamo nel 2040, non vige nessuna regola di distanziamento sociale, ma le persone non escono di casa. Organizzano feste di compleanno telematiche con l'uso di una moderna tecnologica in 4D e fanno tutto il loro shopping attraverso qualche pratico click. Nessuno li obbliga, ma questa è la vita alla quale ogni persona si è adattata. Tutti, tranne qualcuno. È il caso di Gabriele, marito e padre di famiglia, che si guarda attorno e rimpiange ogni singolo istante del suo passato. E mentre si domanda che fine abbia fatto il vivere davvero, il dilemma etico si infittisce riflettendo sul futuro della sua famiglia. Si è innamorato della sua Roberta proprio durante il lockdown, ascoltandola suonare il pianoforte. Ma quando tutto è cambiato, anche il suo amore ha subito delle trasformazioni, senza che nessuno se ne rendesse conto.",
  "Opera in ristampa",
  "",
  "N"
 ]
]
LIBRI_PUBBLICATI = [l for l in LIBRI if l[5].strip().upper() != "N"]

# ─────────────────────────── COMPONENTI ───────────────────────────
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="ig" viewBox="0 0 24 24"><path d="M12 7.4A4.6 4.6 0 1 0 16.6 12 4.6 4.6 0 0 0 12 7.4zm0 7.6a3 3 0 1 1 3-3 3 3 0 0 1-3 3zM17.8 5.9a1.1 1.1 0 1 0 1.1 1.1 1.1 1.1 0 0 0-1.1-1.1z"/><path d="M12 3.8c2.7 0 3 0 4 .1a5.5 5.5 0 0 1 1.9.4 3.2 3.2 0 0 1 1.2.8 3.2 3.2 0 0 1 .8 1.2 5.5 5.5 0 0 1 .4 1.9c.1 1 .1 1.4.1 4s0 3-.1 4a5.5 5.5 0 0 1-.4 1.9 3.4 3.4 0 0 1-2 2 5.5 5.5 0 0 1-1.9.4c-1 .1-1.4.1-4 .1s-3 0-4-.1a5.5 5.5 0 0 1-1.9-.4 3.2 3.2 0 0 1-1.2-.8 3.2 3.2 0 0 1-.8-1.2 5.5 5.5 0 0 1-.4-1.9c-.1-1-.1-1.4-.1-4s0-3 .1-4a5.5 5.5 0 0 1 .4-1.9 3.2 3.2 0 0 1 .8-1.2 3.2 3.2 0 0 1 1.2-.8 5.5 5.5 0 0 1 1.9-.4c1-.1 1.4-.1 4-.1M12 2C9.3 2 8.9 2 7.9 2.1a7.4 7.4 0 0 0-2.4.5 5 5 0 0 0-1.8 1.2A5 5 0 0 0 2.5 5.6a7.4 7.4 0 0 0-.5 2.4C2 9 2 9.3 2 12s0 3.1.1 4.1a7.4 7.4 0 0 0 .5 2.4 5 5 0 0 0 1.2 1.8 5 5 0 0 0 1.8 1.2 7.4 7.4 0 0 0 2.4.5c1 .1 1.4.1 4.1.1s3.1 0 4.1-.1a7.4 7.4 0 0 0 2.4-.5 5.1 5.1 0 0 0 2.9-3 7.4 7.4 0 0 0 .5-2.4c.1-1 .1-1.4.1-4.1s0-3.1-.1-4.1a7.4 7.4 0 0 0-.5-2.4 5 5 0 0 0-1.2-1.8 5 5 0 0 0-1.8-1.2 7.4 7.4 0 0 0-2.4-.5C15.1 2 14.7 2 12 2z"/></symbol>
<symbol id="be" viewBox="0 0 24 24"><path d="M7.8 11.2a3 3 0 0 0 1.5-2.7C9.3 6.4 7.8 5.5 5.6 5.5H0v13h6c2.5 0 4.3-1.2 4.3-3.5a3.2 3.2 0 0 0-2.5-3.8zM2.9 7.8h2.4c.9 0 1.5.4 1.5 1.2s-.6 1.3-1.6 1.3H2.9zm2.8 8.4H2.9v-3h2.9c1.1 0 1.8.6 1.8 1.5s-.8 1.5-1.9 1.5zM19 8.2c-3.1 0-4.7 2.2-4.7 4.6s1.5 4.6 4.9 4.6c2.3 0 3.7-1 4.3-3h-2.4c-.2.5-.8 1-1.8 1-1.4 0-2.1-.7-2.2-2h6.7c.2-3.1-1.3-5.2-4.8-5.2zm-2.1 3.6c.1-1 .8-1.7 2-1.7s1.8.6 1.9 1.7zM15.5 6.2h5.3v1.4h-5.3z"/></symbol>
<symbol id="mk" viewBox="0 0 40 40"><path d="M6 30 L20 6 L34 30 Z" stroke="#c0472a" stroke-width="2" fill="none"/><path d="M13 24 L27 24" stroke="#8b4226" stroke-width="2" fill="none"/></symbol>
</svg>'''
SOCIAL = ('<div class="social"><a href="%s" target="_blank" rel="noopener" aria-label="Instagram"><svg><use href="#ig"/></svg></a>'
          '<a href="%s" target="_blank" rel="noopener" aria-label="Behance"><svg><use href="#be"/></svg></a></div>') % (INSTAGRAM, BEHANCE)

ICONE = ('<link rel="icon" href="%sfavicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="32x32" href="%simg/icone/favicon-32.png">\n'
         '<link rel="icon" type="image/png" sizes="16x16" href="%simg/icone/favicon-16.png">\n<link rel="apple-touch-icon" sizes="180x180" href="%simg/icone/favicon-180.png">\n'
         '<link rel="manifest" href="%ssite.webmanifest">\n<meta name="theme-color" content="#14100d">\n')

def page(root, title, desc, body, active=None, home=False, fname=''):
    """root = prefisso verso la cartella principale ('' o '../')."""
    nav = ''.join('<a href="%s%s.html"%s>%s</a>' % (root, k, ' class="on"' if k == active else '', E(t)) for k, t in MENU)
    head = '' if home else '<header>\n<a class="logo" href="%sindex.html"><svg class="mark" aria-hidden="true"><use href="#mk"/></svg>%s</a>\n<nav>%s</nav>\n</header>\n' % (root, NOME, nav)
    foot = '' if home else (
        '<footer>\n<div class="fg">\n'
        '<div><div class="fn"><svg class="mark" aria-hidden="true"><use href="#mk"/></svg>%s</div>\n%s</div>\n'
        '<div><h4>Sezioni</h4><ul>%s</ul></div>\n'
        '<div><h4>Bottega</h4><ul><li>Via Laura Mantegazza 20a, Roma</li><li><a href="mailto:%s">%s</a></li></ul></div>\n'
        '</div>\n<div class="fb"><span>© 2026 %s</span><span>ideazione Nycheia</span></div>\n</footer>\n'
    ) % (NOME, SOCIAL, ''.join('<li><a href="%s%s.html">%s</a></li>' % (root, k, E(t)) for k, t in MENU), EMAIL, EMAIL, NOME)
    out = '''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<link rel="stylesheet" href="%scss/style.css">
<script src="%sjs/data/opere.js" defer></script>
<script src="%sjs/main.js" defer></script>
</head>
<body%s>
%s%s%s%s</body>
</html>
''' % (E(title), E(desc), E(title), E(desc), root, root, root, ' class="home"' if home else '', SPRITE, head, body, foot)
    return out.replace('<link rel="stylesheet"', ICONE % ((root,) * 5) + '<link rel="stylesheet"', 1)

def main_(inner): return '<main>\n%s\n</main>\n' % inner
def frames(n, label): return '<div class="thumbs">%s</div>' % ''.join('<div class="frame"><span>%s</span></div>' % label for _ in range(n))
def write(path, content):
    p = os.path.join(ROOT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)

# ───────────────────────────── PAGINE ─────────────────────────────
# Home
home = '<div class="hm">\n<h1>%s</h1>\n<p class="role">Pittore · Scultore · Scrittore</p>\n<nav>%s</nav>\n</div>\n' % (
    NOME, ''.join('<a href="%s.html">%s</a>' % (k, E(t)) for k, t in MENU))
write('index.html', page('', NOME + ' — Pittore, scultore, scrittore', 'Sito ufficiale di Adriano Segarelli, pittore, scultore e scrittore. Roma.', home, home=True))

# Biografia: foto dello studio + introduzione, poi un'opera accanto a ogni capoverso (BIO_IMMAGINI, nello stesso ordine dei capoversi 2-8)
BIO_IMMAGINI = json.load(open(os.path.join(ROOT, '_sorgenti', 'biografia-immagini.json')))
BIO_EXTRA = json.load(open(os.path.join(ROOT, '_sorgenti', 'biografia-extra.json')))  # sezione 6 della skill as-biografia (la 5, cortometraggi, e' tolta dal sito per ora)
def fig(im):
    cap = '<figcaption>%s<small>%s</small></figcaption>' % (E(im['titolo']), E(im['scheda']))
    return '<figure><a class="zoom" href="img/biografia/%s" aria-label="Ingrandisci: %s"><img src="img/biografia/%s" width="%d" height="%d" alt="%s" loading="lazy"></a>%s</figure>' % (
        im['file'], E(im['titolo']), im['file'], im['w'], im['h'], E(im['titolo'] + ' — ' + im['scheda']), cap)
righe = ''.join('<article class="bio-row%s">\n%s\n<p>%s</p>\n</article>\n' % (' rev' if i % 2 else '', fig(im), E(p))
                for i, (p, im) in enumerate(zip(BIOGRAFIA[1:], BIO_IMMAGINI)))
# Ultimo capoverso (pubblicazioni, sezione 6 della skill as-biografia) con la copertina del libro piu' vecchio tra quelli pubblicati
primo_libro = min(LIBRI_PUBBLICATI, key=lambda l: int(l[0]))
_slug_libro = re.sub(r'[^a-z0-9]+', '-', primo_libro[1].lower().replace("'", '-')).strip('-')
fig_libro = ('<figure><a class="zoom" href="img/libri/%s.jpg" aria-label="Ingrandisci: %s"><img src="img/libri/%s.jpg" width="%d" height="%d" alt="Copertina de %s" loading="lazy"></a>'
             '<figcaption>%s<small>%s</small></figcaption></figure>') % (_slug_libro, E(primo_libro[1]), _slug_libro, 321, 522, E(primo_libro[1]), E(primo_libro[1]), E(primo_libro[0]))
riga_libri = '<article class="bio-row%s">\n%s\n<p>%s</p>\n</article>\n' % (' rev' if len(BIO_IMMAGINI) % 2 else '', fig_libro, E(BIO_EXTRA[0]))
bio = ('<h2>Biografia</h2>\n<p class="sub">Roma, 1978</p>\n'
       '<div class="bio-top">\n<figure><img src="img/biografia/studio.jpg" width="784" height="774" alt="Adriano Segarelli nel suo studio"></figure>\n<p class="lead">%s</p>\n</div>\n%s'
       '<div class="bio-end"><a class="btn" href="pittura.html">Continua a conoscermi</a></div>') % (E(BIOGRAFIA[0]), righe + riga_libri)
write('biografia.html', page('', 'Biografia — ' + NOME, 'Biografia di Adriano Segarelli, nato a Roma nel 1978: pittura, scultura, affresco e libri.', main_(bio), 'biografia'))

# La mia pittura: schede (tab) per tema. Anteprima di 5 righe + "Leggi di più" (pagina col testo intero) + opere piccole (si ingrandiscono)
TEMI_OPERE = json.load(open(os.path.join(ROOT, '_sorgenti', 'pittura-immagini.json')))
def src_img(f):
    # file in img/pittura/ oppure indirizzo completo (es. immagini del Portfolio)
    return f if f.startswith('http') else 'img/pittura/' + f
def tessere(k):
    out = ''.join('<figure><a class="zoom" href="%s" aria-label="Ingrandisci: %s"><img src="%s"%s alt="%s" loading="lazy" onerror="this.closest(\'figure\').classList.add(\'manca\')"></a><figcaption>%s<small>%s</small></figcaption></figure>' % (
        src_img(o['file']), E(o['titolo']), src_img(o['file']), (' width="%d" height="%d"' % (o['w'], o['h'])) if o.get('w') else '', E(o['titolo'] + ' — ' + o['scheda']), E(o['titolo']), E(o['scheda'])) for o in TEMI_OPERE.get(k, []))
    return '<div class="mini">%s</div>' % out
tabs = ''.join('<button role="tab" type="button" id="t-%s" data-k="%s" aria-controls="p-%s" aria-selected="%s">%s</button>' % (k, k, k, 'true' if i == 0 else 'false', E(t)) for i, (k, t) in enumerate(TEMI))
# File scaricabili (allegati di una release GitHub; GitHub conta i download): _sorgenti/download.json
DOWNLOAD = json.load(open(os.path.join(ROOT, '_sorgenti', 'download.json')))
def pannello(i, k, t):
    ps = TEMI_TESTI.get(k, [])
    testo = ('<p class="clamp">%s</p>\n<p><a class="more" href="tema-%s.html">Leggi di più →</a></p>' % (E(' '.join(ps)), k)) if ps else '<p class="ph">Testo in arrivo.</p>'
    scarica = ''.join('\n<a class="btn" href="%s" rel="noopener">%s</a>' % (E(d['url']), E(d['label'])) for d in DOWNLOAD if d['tema'] == k)
    return '<div class="tp%s" role="tabpanel" id="p-%s" aria-labelledby="t-%s">\n<div class="tx"><h3>%s</h3>\n%s\n<a class="btn" href="%s" target="_blank" rel="noopener">Portfolio</a>%s</div>\n%s\n</div>\n' % (
        ' on' if i == 0 else '', k, k, E(t), testo, PORTFOLIO, scarica, tessere(k))
pit = '<h2>La mia pittura</h2>\n<p class="sub">Un percorso attraverso i temi</p>\n<div class="tabs">\n<div role="tablist" aria-label="Temi">%s</div>\n%s</div>' % (tabs, ''.join(pannello(i, k, t) for i, (k, t) in enumerate(TEMI)))
write('pittura.html', page('', 'La mia pittura — ' + NOME, 'Il percorso pittorico di Adriano Segarelli: ' + ', '.join(t for _, t in TEMI) + '.', main_(pit), 'pittura'))
# Pagina con il testo intero di ogni tema (solo per i temi che hanno il testo)
for k, t in TEMI:
    ps = TEMI_TESTI.get(k)
    if not ps: continue
    inner = ('<a class="back" href="pittura.html#%s">← La mia pittura</a>\n<div class="d-head"><div class="k">Tema</div><h1>%s</h1></div>\n<div class="lungo">%s</div>\n'
             '<p style="text-align:center"><a class="btn" href="pittura.html#%s">Torna a La mia pittura</a></p>') % (k, E(t), ''.join(('<p class="nota">%s</p>' if p.startswith('[') else '<p>%s</p>') % E(p) for p in ps), k)
    write('tema-%s.html' % k, page('', '%s — %s' % (t, NOME), ps[0][:150], main_(inner), 'pittura'))

# Pagine semplici
def semplice(fn, key, titolo, sub, desc, bottone=None):
    b = '\n<a class="btn" href="%s" target="_blank" rel="noopener">%s</a>' % bottone if bottone else ''
    inner = '<h2>%s</h2>\n<p class="sub">%s</p>\n<div class="path"><div class="solo">\n<p class="ph">Testo in arrivo.</p>\n%s%s\n</div></div>' % (E(titolo), E(sub), frames(3,'Foto'), b)
    write(fn, page('', titolo + ' — ' + NOME, desc, main_(inner), key))
# L'affresco: testo dal foglio Pagine (Argomento = "L'affresco"); foto in arrivo
AFF = json.load(open(os.path.join(ROOT, '_sorgenti', 'affresco.json')))
# Anteprima di 5 righe (primo blocco) + "Leggi di più" verso la pagina con il testo intero
prima = AFF[0]
testo_aff = ('<h3>%s</h3>\n<p class="clamp">%s</p>\n<p><a class="more" href="affresco-testo.html">Leggi di più →</a></p>\n'
             % (E(prima.get('h', "L'affresco")), E(' '.join(prima['p']))))
AFF_FOTO = json.load(open(os.path.join(ROOT, '_sorgenti', 'affresco-immagini.json')))
foto_aff = ''.join('<figure><a class="zoom" href="img/affresco/%s" aria-label="Ingrandisci: %s"><img src="img/affresco/%s" width="%d" height="%d" alt="%s" loading="lazy"></a><figcaption>%s<small>%s</small></figcaption></figure>' % (
    o['file'], E(o['titolo']), o['file'], o['w'], o['h'], E(o['titolo']), E(o['titolo']), E(o['scheda'])) for o in AFF_FOTO)
aff = ('<h2>L\'affresco</h2>\n<p class="sub">Affresco e strappo d\'affresco</p>\n<div class="tp solo-tp">\n<div class="tx">\n%s<a class="btn" href="%s" target="_blank" rel="noopener">Scopri il servizio</a></div>\n<div class="mini alto">%s</div>\n</div>'
       % (testo_aff, LINK_AFFRESCO, foto_aff))
write('affresco.html', page('', "L'affresco — " + NOME, AFF[0]['p'][0][:160], main_(aff), 'affresco'))
# Pagina con il testo intero
intero = ''.join(('<h3>%s</h3>\n' % E(x['h']) if x.get('h') else '') + ''.join('<p>%s</p>\n' % E(p) for p in x['p']) for x in AFF)
inner = ('<a class="back" href="affresco.html">← L\'affresco</a>\n<div class="d-head"><div class="k">L\'affresco</div><h1>Affresco e strappo d\'affresco</h1></div>\n<div class="lungo">%s</div>\n'
         '<p style="text-align:center"><a class="btn" href="%s" target="_blank" rel="noopener">Scopri il servizio</a> <a class="btn" href="affresco.html">Torna a L\'affresco</a></p>') % (intero, LINK_AFFRESCO)
write('affresco-testo.html', page('', "Affresco e strappo d'affresco — " + NOME, AFF[0]['p'][0][:160], main_(inner), 'affresco'))
# Le mie sculture: stessa impostazione di La mia pittura, senza schede. Testo dal foglio Pagine (Argomento = "Le mie sculture"), foto piccole che si ingrandiscono
SCU = json.load(open(os.path.join(ROOT, '_sorgenti', 'sculture.json')))
foto_scu = ''.join('<figure><a class="zoom" href="img/sculture/%s" aria-label="Ingrandisci: %s"><img src="img/sculture/%s" width="%d" height="%d" alt="%s" loading="lazy"></a><figcaption>%s<small>%s</small></figcaption></figure>' % (
    o['file'], E(o['titolo']), o['file'], o['w'], o['h'], E(o['titolo'] + ' — ' + o['scheda']), E(o['titolo']), E(o['scheda'])) for o in SCU['opere'])
scu = ('<h2>Le mie sculture</h2>\n<p class="sub">%s</p>\n<div class="tp solo-tp">\n<div class="tx">\n%s\n<a class="btn" href="%s" target="_blank" rel="noopener">Vedi le sculture</a></div>\n<div class="mini">%s</div>\n</div>'
       % (E(SCU['sub']), '\n'.join('<p>%s</p>' % E(p) for p in SCU['testo']), LINK_SCULTURE, foto_scu))
write('sculture.html', page('', 'Le mie sculture — ' + NOME, SCU['testo'][0][:160], main_(scu), 'sculture'))
# I miei libri: copertine in img/libri/<titolo-con-trattini>.jpg (o png/webp); se manca appare un riquadro vuoto
def slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower().replace("'",'-').replace('à','a').replace('è','e').replace('é','e')).strip('-')
def copertina(t):
    for ext in ('jpg','jpeg','png','webp'):
        if os.path.exists(os.path.join(ROOT,'img','libri','%s.%s' % (slug(t),ext))):
            return '<div class="frame cop"><img src="img/libri/%s.%s" alt="Copertina de %s"></div>' % (slug(t),ext,E(t))
    return '<div class="frame"><span>Locandina</span></div>'
def btn(label,url):
    url=url.split('#')[0].strip()
    return '<a class="btn" href="%s" target="_blank" rel="noopener">%s ↗</a>' % (E(url),label) if url else '<span class="btn off" aria-disabled="true">%s</span>' % label
blocchi=[]
for anno,titolo,sin,carta,dig,_stato in sorted(LIBRI_PUBBLICATI,key=lambda l:-int(l[0])):
    rist=next((x for x in (carta,dig) if 'ristampa' in x.lower()),None)
    azioni='<p class="rist">%s</p>' % E(rist) if rist else '<div class="acq">%s%s</div>' % (btn('Carta',carta),btn('Digitale',dig))
    par=''.join('<p>%s</p>' % E(p.strip()) for p in re.split(r'\n+',sin) if p.strip())
    blocchi.append('<article class="libro">\n%s\n<div>\n<div class="li-y">%s</div>\n<h3>%s</h3>\n<div class="li-s">%s</div>\n%s\n</div>\n</article>' % (copertina(titolo),E(anno),E(titolo),par,azioni))
lib_page='<h2>I miei libri</h2>\n<p class="sub">Pubblicazioni</p>\n<div class="libri">\n%s\n</div>' % '\n'.join(blocchi)
write('libri.html', page('', 'I miei libri — '+NOME, 'I libri di Adriano Segarelli: '+', '.join(l[1] for l in LIBRI_PUBBLICATI)+'.', main_(lib_page), 'libri'))

# Esperienze: elenco + una pagina per evento
from urllib.parse import urlparse
def dominio(u):
    d = urlparse(u).netloc.lower()
    return d[4:] if d.startswith('www.') else d
ordine = sorted(range(len(EVENTI)), key=lambda i: (-int(EVENTI[i][0]), i))
eventi = []
for n, i in enumerate(ordine):
    y, k, t, p, d, u = EVENTI[i]
    eventi.append(dict(id='e%02d' % (n+1), year=y, kind=k, title=t, place=p, desc=d, url=u))
gruppi = []
for e in eventi:
    g = next((g for g in gruppi if g[0] == e['year']), None)
    if not g: g = (e['year'], []); gruppi.append(g)
    g[1].append(e)
lista = ''.join('<div class="xg"><div class="xy">%s</div><div>\n%s</div></div>\n' % (E(y), ''.join(
    '<a class="xe" href="%s" target="_blank" rel="noopener"><div class="xk">%s</div><div class="xt">%s</div>%s%s<span class="xl">Leggi i dettagli ↗</span></a>\n' % (
        E(e['url']), E(e['kind']), E(e['title']), '<div class="xp">%s</div>' % E(e['place']) if e['place'] else '',
        '<div class="xa">%s</div>' % E(e['desc']) if e['desc'] else '') for e in L)) for y, L in gruppi)
esp = '<h2>Esperienze</h2>\n<p class="sub">Mostre e premi</p>\n<div id="news">\n%s</div>' % lista
write('esperienze.html', page('', 'Esperienze — ' + NOME, 'Mostre, premi e apparizioni di Adriano Segarelli.', main_(esp), 'esperienze'))

for e in eventi:
    sl = ''.join('<figure class="frame"><span>Foto %d</span></figure>' % n for n in (1,2,3))
    det = ('<a class="back" href="../esperienze.html">← Esperienze</a>\n<div class="d-head"><div class="k">%s · %s</div><h1>%s</h1>%s</div>\n'
           '<div class="car">\n<button class="pv" aria-label="Precedente">‹</button>\n%s\n<button class="nx" aria-label="Successiva">›</button>\n<div class="cnt"></div>\n</div>\n'
           '<div class="facts"><div><b>Anno</b>%s</div><div><b>Tipologia</b>%s</div><div><b>Luogo</b>%s</div><div><b>Fonte</b>%s</div></div>\n'
           '<div class="cols">%s</div>\n<p style="text-align:center"><a class="btn" href="%s" target="_blank" rel="noopener">Leggi la fonte ↗</a></p>'
           % (E(e['kind']), E(e['year']), E(e['title']), '<p>%s</p>' % E(e['place']) if e['place'] else '', sl,
              E(e['year']), E(e['kind']), E(e['place'] or '—'), E(dominio(e['url'])), '<p>%s</p>' % E(e['desc']), E(e['url'])))
    write('esperienze/%s.html' % e['id'], page('../', '%s — %s' % (e['title'], NOME), (e['desc'] or 'Esperienza di Adriano Segarelli: %s.' % e['title'])[:300], main_(det), 'esperienze'))

# Contatti
con = '''<h2>Contatti</h2>
<p class="sub">Parliamo della vostra idea</p>
<div class="contact">
<div class="info">
<p><b>Bottega</b>Via Laura Mantegazza 20a, Roma</p>
<p><b>Email</b><a href="mailto:%s">%s</a></p>
<p><b>Orari sopralluoghi</b>Su prenotazione</p>
%s
</div>
<form id="f">
<h3>Scrivimi</h3>
<label>Nome e cognome<input name="n" required></label>
<label>Email<input name="e" type="email" required></label>
<label>Tipo di richiesta<input name="t" required></label>
<label>Messaggio<textarea name="m" required></textarea></label>
<div><button class="btn noMt" type="submit">Invia email</button></div>
<p class="ok" id="ok">Grazie! Si apre il tuo programma di posta per completare l'invio.</p>
</form>
</div>''' % (EMAIL, EMAIL, SOCIAL)
write('contatti.html', page('', 'Contatti — ' + NOME, 'Contatta Adriano Segarelli: bottega a Roma, affreschi e strappi d\'affresco su commissione.', main_(con), 'contatti'))

# Opere: sfondo home + filigrana (js/data/opere.js)
wm = json.load(open(os.path.join(ROOT,'_sorgenti','opere-filigrane.json'))); hb = json.load(open(os.path.join(ROOT,'_sorgenti','opere-sfondi.json')))
opere = [dict(titolo=w['title'], filigrana='img/filigrane/' + w['file'], sfondo='img/sfondi/' + h['file'], orizzontale=w['land'],
              punto=w['m'], opacita=w['o'], velo1=h['o1'], velo2=h['o2']) for w, h in zip(wm, hb)]
write('js/data/opere.js', '/* Opere usate come sfondo della home (a colori) e come filigrana (negativo) nelle altre pagine.\n   Per aggiungerne una: copiare i due file in img/sfondi e img/filigrane e aggiungere una riga. */\nconst OPERE = ' + json.dumps(opere, ensure_ascii=False, indent=1) + ';\n')
print('pagine generate:', 8 + len(eventi))
