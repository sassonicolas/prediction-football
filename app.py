import streamlit as st
import numpy as np
import requests

# 1. CONFIGURAZIONE CHIAVE API
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.title("⚽ Predittore IA - Richieste Ottimizzate")

# 2. 🌟 TRUCCO DELLO SVILUPPATORE: MEMORIA CACHE (st.cache_data)
# Questa riga dice all'IA: "Controlla internet solo una volta. Se l'hai già fatto, riusa la risposta senza consumare crediti!"
@st.cache_data(ttl=3600)  # Memorizza i dati per 1 ora intera prima di ricontrollare internet
def controlla_api_protetto():
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

connesso, chiamate_rimanenti = controlla_api_protetto()

if connesso:
    st.success(f"🟢 Sistema Ottimizzato con Cache! Crediti API rimanenti: {chiamate_rimanenti}")
else:
    st.error("🔴 Errore di connessione API.")

# 3. DATABASE COMPLETO
database_completo = {
    "Spagna": {
        "gol_fatti": 2.10, "gol_subiti": 0.50,
        "giocatori": {
            "Lamine Yamal": {"tiri_medi": 2.8, "passaggi_chiave": 1.9},
            "Dani Olmo": {"tiri_medi": 2.4, "passaggi_chiave": 2.1},
            "Nico Williams": {"tiri_medi": 2.1, "passaggi_chiave": 1.5}
        }
    },
    "Belgio": {
        "gol_fatti": 1.80, "gol_subiti": 1.20,
        "giocatori": {
            "Kevin De Bruyne": {"tiri_medi": 2.3, "passaggi_chiave": 3.4},
            "Jeremy Doku": {"tiri_medi": 1.9, "passaggi_chiave": 1.8},
            "Leandro Trossard": {"tiri_medi": 2.0, "passaggi_chiave": 1.2}
        }
    },
    "Francia": {
        "gol_fatti": 1.95, "gol_subiti": 0.60,
        "giocatori": {
            "Kylian Mbappé": {"tiri_medi": 4.2, "passaggi_chiave": 2.0},
            "Antoine Griezmann": {"tiri_medi": 2.2, "passaggi_chiave": 2.8}
        }
    }
}

# 4. INTERFACCIA UTENTE
col1, col2 = st.columns(2)
squadre_disponibili = list(database_completo.keys())

with col1:
    squadra_casa = st.selectbox("Squadra in Casa", squadre_disponibili, index=0)
    gol_fatti_casa = database_completo[squadra_casa]["gol_fatti"]
    gol_subiti_casa = database_completo[squadra_casa]["gol_subiti"]

with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", squadre_disponibili, index=1)
    gol_fatti_ospite = database_completo[squadra_ospite]["gol_fatti"]
    gol_subiti_ospite = database_completo[squadra_ospite]["gol_subiti"]

st.write("---")
st.subheader("🎯 Analisi Prestazioni Giocatore")
tutte_le_scelte = list(database_completo[squadra_casa]["giocatori"].keys()) + list(database_completo[squadra_ospite]["giocatori"].keys())
giocatore_scelto = st.selectbox("Seleziona un giocatore per il match:", tutte_le_scelte)

if giocatore_scelto in database_completo[squadra_casa]["giocatori"]:
    dati_giocatore = database_completo[squadra_casa]["giocatori"][giocatore_scelto]
    difesa_avversaria = gol_subiti_ospite
else:
    dati_giocatore = database_completo[squadra_ospite]["giocatori"][giocatore_scelto]
    difesa_avversaria = gol_subiti_casa

tiri_attesi = dati_giocatore["tiri_medi"] * (difesa_avversaria / 1.0)

# 5. BOTTONE SIMULAZIONE INFINITA (Calcolata sul server Streamlit, consumo API = 0)
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
    
    tiri_simulati = np.random.poisson(tiri_attesi, simulazioni)
    prob_over_1_5_tiri = (np.sum(tiri_simulati >= 2) / simulazioni) * 100
    prob_over_2_5_tiri = (np.sum(tiri_simulati >= 3) / simulazioni) * 100

    col_ris1, col_ris2 = st.columns(2)
    
    with col_ris1:
        st.write("### 🏆 Top Risultati Esatti:")
        for ris, conteggio in risultati_ordinati[:3]:
            prob = (conteggio / simulazioni) * 100
            st.success(f"**{ris}** — Probabilità: {prob:.2f}%")
            
    with col_ris2:
        st.write(f"### 📈 Statistiche per {giocatore_scelto}:")
        st.write(f"**Tiri totali stimati:** {tiri_attesi:.2f}")
        st.info(f"Probabilità Over 1.5 Tiri: **{prob_over_1_5_tiri:.2f}%**")
        st.info(f"Probabilità Over 2.5 Tiri: **{prob_over_2_5_tiri:.2f}%**")
