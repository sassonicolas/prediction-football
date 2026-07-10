import streamlit as st
import numpy as np
import requests

# 1. CONFIGURAZIONE CHIAVE API
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.title("⚽ Il Mio Predittore di Risultati IA - LIVE")
st.write("L'applicazione è connessa a API-Sports tramite la tua chiave personale!")

# 2. FUNZIONE LIVE PER VERIFICARE LA CONNESSIONE
def controlla_api():
    url = "https://v3.football.api-sports.io/status"
    headers = {'x-rapidapi-key': API_KEY}
    try:
        risposta = requests.get(url, headers=headers).json()
        if risposta.get("response"):
            rimanenti = risposta["response"]["requests"]["limit_day"] - risposta["response"]["requests"]["current"]
            return True, rimanenti
    except:
        pass
    return False, 0

connesso, chiamate_rimanenti = controlla_api()

if connesso:
    st.success(f"🟢 Connessione Internet OK! Ti rimangono {chiamate_rimanenti} simulazioni per oggi.")
else:
    st.error("🔴 Errore di connessione all'API. Controlla la chiave.")

# 3. DATABASE DELLE SQUADRE (Puoi personalizzare questi dati storici come vuoi)
database_squadre = {
    "Spagna": {"id": 9, "gol_fatti": 2.10, "gol_subiti": 0.50},
    "Belgio": {"id": 7, "gol_fatti": 1.80, "gol_subiti": 1.20},
    "Francia": {"id": 2, "gol_fatti": 1.95, "gol_subiti": 0.60},
    "Inghilterra": {"id": 10, "gol_fatti": 1.70, "gol_subiti": 0.80},
    "Germania": {"id": 25, "gol_fatti": 2.20, "gol_subiti": 1.10},
    "Italia": {"id": 31, "gol_fatti": 1.40, "gol_subiti": 0.90}
}

# 4. INTERFACCIA GRAFICA
col1, col2 = st.columns(2)
squadre_disponibili = list(database_squadre.keys())

with col1:
    squadra_casa = st.selectbox("Squadra in Casa", squadre_disponibili, index=0)
    gol_fatti_casa = database_squadre[squadra_casa]["gol_fatti"]
    gol_subiti_casa = database_squadre[squadra_casa]["gol_subiti"]

with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", squadre_disponibili, index=1)
    gol_fatti_ospite = database_squadre[squadra_ospite]["gol_fatti"]
    gol_subiti_ospite = database_squadre[squadra_ospite]["gol_subiti"]

# 5. SIMULAZIONE MATEMATICA CON MONTE CARLO (100.000 partite simulate)
if st.button("🔥 AVVIA SIMULAZIONE COMPLETA"):
    lambda_casa = gol_fatti_casa * (gol_subiti_ospite / 1.0)
    lambda_ospite = gol_fatti_ospite * (gol_subiti_casa / 1.0)
    
    simulazioni = 100000
    gol_casa_simulati = np.random.poisson(lambda_casa, simulazioni)
    gol_ospite_simulati = np.random.poisson(lambda_ospite, simulazioni)
    
    risultati = {}
    for i in range(simulazioni):
        ris = f"{gol_casa_simulati[i]} - {gol_ospite_simulati[i]}"
        risultati[ris] = risultati.get(ris, 0) + 1
        
    risultati_ordinati = sorted(risultati.items(), key=lambda x: x[1], reverse=True)
    
    st.write("---")
    st.subheader(f"📊 Risultati per {squadra_casa} vs {squadra_ospite}")
    
    for ris, conteggio in risultati_ordinati[:3]:
        prob = (conteggio / simulazioni) * 100
        st.success(f"Risultato Esatto: **{ris}** — Probabilità: **{prob:.2f}%**")
