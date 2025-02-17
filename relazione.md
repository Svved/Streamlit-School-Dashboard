# Relazione Finale Progetto Visualizzazione Dati ITS

## 1. Fasi di Sviluppo

### 1.1 EDA/ETL
- Utilizzo di Notebook (`EDA-ETL.ipynb`) per l'analisi esplorativa iniziale, dal momento che lo strumento favorisce la
- visualizzazione immediata dei risultati dell'EDA e della pulizia dei dati.
- Principali operazioni di pulizia dati:
  - Rimozione colonne non necessarie
  - Gestione valori mancanti
  - Conversione formati (stringhe temporali in float)
  - Standardizzazione nomi colonne
- Next steps:
  - Anonimizzazione dei dati
  - Automazione ETL

### 1.2 Progettazione Architettura
- Struttura modulare con funzioni separate per:
  - Caricamento dati (`get_calendar`, `get_grades`, `get_absences`)
  - Visualizzazione (`create_bar_chart`, `create_student_grade_chart`)
  - Generazione report (`create_report_card`)
- Struttura Main-Test:
  - Main per versione in produzione+
  - Test per implementazione nuove features
- Archiviazione in SQLite, natura del dato non in crescita e tabellare
- Utilizzo di caching Streamlit per ottimizzare le performance
- Utilizzo di Docker per favorire distribuzione e scalabilità
- Utilizzo di GitHub per versionamento 

### 1.3 UX/UI
- Utilizzo layout wide di streamlit per visualizzazione migliore
- Layout a tab per organizzare logicamente le informazioni:
  - Lezioni: visualizzazione ore per docente
  - Valutazioni: analisi voti e presenze
  - ITS's Heroes: metriche principali e KPI
- Design responsive con colonne per visualizzazioni affiancate
- Elementi interattivi (dropdown, radio buttons)
- Rispettati standard leggibilità caratteri
- Esperienza basilare straight-forward, segno di un prodotto in fase di prototipazione

### 1.4 Sviluppo, Testing e Validazione
- Implementazione incrementale delle funzionalità e delle componenti
- Gestione errori con blocco try-except per debug
- Documentazione inline del codice e creazione di documentazione
- Testing manuale delle funzionalità
- Validazione del contenuto con colleghi

## 2. Scelte Tecniche

### 2.1 Stack Tecnologico
- **Streamlit**: framework principale per la dashboard
  - Facilità di sviluppo
  - Componenti predefiniti per data visualization
  - Integrazione nativa con Pandas e Plotly
- **Plotly**: libreria per grafici interattivi
  - Maggiore flessibilità rispetto a matplotlib
  - Interattività nativa
  - Personalizzazione avanzata
- **SQLite3**: libreria python per creare SQLite
  - Facile utilizzo per portare da dato da Pandas a DB
  - Leggero e integrato

### 2.2 Gestione Dati
- Dati esetratti da file CSV/Excel:
  - Semplicità di gestione
  - Facilità di aggiornamento
  - Portabilità della soluzione
- Utilizzo di Pandas per manipolazione dati
  - Operazioni efficienti su dataframe
  - Facilità di aggregazione e trasformazione
- Connettore a DB SQLite:
  - portare il dato in formato DB SQLite
  - garatire integrità, portabilità e disponibilità del dato

### 2.3 Deployment
- Containerizzazione con Docker per:
  - Portabilità
  - Gestione dipendenze
  - Facilità di deployment

### 2.4 Versionamento e Mantenimento
- Piattaforma GitHub per:
  - perfetto per dashboard code-rich
  - gestione versioni
  - aggiunta features 
  - condivisione codice sorgente

## 3. Sfide e Soluzioni

### 3.1 ETL
- **Sfida**: Formati temporali inconsistenti
- **Soluzione**: Funzione `convert_to_float_hours` per standardizzazione
- **Sfida**: Dati mancanti
- **Soluzione**: Rimozione dato il numero basso

### 3.2 Visualizzazione
- **Sfida**: Layout responsivo con multiple visualizzazioni
- **Soluzione**: Utilizzo sistema di colonne Streamlit e parametri `use_container_width`

### 3.3 Performance
- **Sfida**: Caricamento dati ripetuto
- **Soluzione**: Implementazione cache Streamlit (`@st.cache_data`)

### 3.4 UX
- **Sfida**: Visualizzazione efficace di metriche multiple
- **Soluzione**: Organizzazione in tab e utilizzo di metriche comparative

## 4. Possibili Miglioramenti Futuri
- Anonimizzazione dei dati
- Configurare deployment via Streamlit o server proprio
- Implementazione autenticazione utenti
- Aggiunta filtri avanzati
- Automazione aggiornamento e ETL dati
- Implementazione export report in PDF