# Immobilien-Kalkulator

Interaktiver Wohnungskauf-Rechner mit Apple-Design, gebaut mit Streamlit.

## Features

- **Annuitätenrechner** mit 3 Berechnungsmodi (Tilgungssatz, Rate, Laufzeit)
- **Rückwärtsrechnung** — Wie viel Immobilie kann ich mir leisten?
- **Kaufnebenkosten** nach Bundesland (Grunderwerbsteuer, Notar, Grundbuch, Makler)
- **Sondertilgungen** & Zinsbindung mit Anschlussfinanzierung
- **Interaktive Diagramme** (Restschuld, Zins/Tilgung, Kostenverteilung)
- **Tilgungsplan** als Tabelle + CSV-Export
- **Kalkulationen speichern/laden** mit Titel
- **Szenario-Vergleich** nebeneinander
- **JSON Export/Import** aller gespeicherten Kalkulationen
- **Budget- und Zinssensitivitätsanalyse**

## Lokal starten

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Auf Streamlit Cloud hosten

1. Repository auf GitHub pushen
2. [share.streamlit.io](https://share.streamlit.io) besuchen
3. Repository, Branch und `app.py` als Main file auswählen
4. Deploy klicken

## Tech Stack

- Python 3.10+
- Streamlit
- Plotly
- Pandas / NumPy
