import streamlit as st
import numpy as np
import requests

# 1. CHIAVE API PERSONALE
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.title("⚽ SASSO BET - PREDICTION MONDIALE & SERIE A ")
st.write("Seleziona una squadra della Serie A o una Nazionale del Mondiale 2026 per scaricare la rosa in tempo reale!")

# 2. DIZIONARIO COMPLETO DELLE SQUADRE (AGGIORNATO CON FROSINONE)
DIZIONARIO_SQUADRE = {
    # --- SERIE A & SQUADRE ITALIANE ---
    "Atalanta (Serie A)": 499,
    "Bologna (Serie A)": 504,
    "Cagliari (Serie A)": 490,
    "Como (Serie A)": 511,
    "Empoli (Serie A)": 512,
    "Fiorentina (Serie A)": 502,
    "Frosinone (Italia)": 506,
    "Genoa (Serie A)": 495,
    "Inter (Serie A)": 496,
    "Juventus (Serie A)": 498,
    "Lazio (Serie A)": 487,
    "Lecce (Serie A)": 449,
    "Milan (Serie A)": 489,
    "Monza (Serie A)": 1579,
    "Napoli (Serie A)": 492,
    "Parma (Serie A)": 500,
    "Roma (Serie A)": 497,
    "Torino (Serie A)": 503,
    "Udinese (Serie A)": 494,
    "Venezia (Serie A)": 517,
    "Verona (Serie A)": 505,
    
    # --- NAZIONALI MONDIALE 2026 ---
    "Argentina (Mondiale)": 26,
    "Belgio (Mondiale)": 7,
    "Brasile (Mondiale)": 6,
    "Canada (Mondiale)": 549,
    "Croazia (Mondiale)": 3,
    "Francia (Mondiale)": 2,
    "Germania (Mondiale)": 25,
    "Giappone (Mondiale)": 1024,
    "Inghilterra (Mondiale)": 10,
    "Italia (Mondiale)": 31,
    "Marocco (Mondiale)": 30,
    "Messico (Mondiale)": 16,
    "Olanda (Mondiale)": 11,
    "Portogallo (Mondiale)": 27,
    "Spagna (Mondiale)": 9,
    "Stati Uniti (Mondiale)": 2383,
    "Uruguay (Mondiale)": 20
}

# 3. FUNZIONE LIVE PER SCARICARE I GIOCATORI DELLA SQUADRA SELEZIONATA
@st.cache_data(ttl=86400)
def recupera_giocatori_live(team_id):
    url = f"https://v3.football.api-sports.io/players/squads?team={team_id}"
    headers = {'x-rapidapi-key': API_KEY}
    try:
        risposta = requests.get(url, headers=headers).json()
        if risposta.get("response") and len(risposta["response"]) > 0:
            lista_calc = risposta["response"][0]["players"]
            nomi = [g["name"] for g in lista_calc if g["position"] in ["Attacker", "Midfielder"]]
            return nomi if nomi else ["Nessun giocatore trovato"]
    except:
        pass
    return ["Caricamento giocatori completato / Usa lista live"]

# 4. FUNZIONE PER ESTIMARE LE MEDIE GOL LIVE
@st.cache_data(ttl=86400)
def recupera_statistiche_squadra(team_id, is_naz):
    league_id = 1 if is_naz else 135
    season = 2026 if is_naz else 2025
    
    url = f"https://v3.football.api-sports.io/teams/statistics?league={league_id}&season={season}&team={team_id}"
    headers = {'x-rapidapi-key': API_KEY}
    try:
        risposta = requests.get(url, headers=headers).json()
        if risposta.get("response"):
            fatti = risposta["response"]["goals"]["for"]["average"]["total"]
            subiti = risposta["response"]["against"]["average"]["total"]
            return float(fatti), float(subiti)
    except:
        pass
    return (1.8, 1.0) if not is_naz else (2.0, 0.8)

# 5. INTERFACCIA SELEZIONE SQUADRE
col1, col2 = st.columns(2)
squadre_disponibili = sorted(list(DIZIONARIO_SQUADRE.keys()))

with col1:
    squadra_casa = st.selectbox("Squadra in Casa", squadre_disponibili, index=0)
    id_casa = DIZIONARIO_SQUADRE[squadra_casa]
    is_naz_casa = "Mondiale" in squadra_casa
    gol_fatti_casa, gol_subiti_casa = recupera_statistiche_squadra(id_casa, is_naz_casa)
    st.caption(f"Media Stimata: Fatti {gol_fatti_casa:.2f} | Subiti {gol_subiti_casa:.2f}")

with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", squadre_disponibili, index=1)
    id_ospite = DIZIONARIO_SQUADRE[squadra_ospite]
    is_naz_ospite = "Mondiale" in squadra_ospite
    gol_fatti_ospite, gol_subiti_ospite = recupera_statistiche_squadra(id_ospite, is_naz_ospite)
    st.caption(f"Media Stimata: Fatti {gol_fatti_ospite:.2f} | Subiti {gol_subiti_ospite:.2f}")

st.write("---")

# 6. CARICAMENTO DELLE ROSE REALI DAL WEB
st.subheader("🎯 Seleziona il Giocatore dalle Rose Attuali")
giocatori_casa = recupera_giocatori_live(id_casa)
giocatori_ospite = recupera_giocatori_live(id_ospite)
tutti_i_giocatori = giocatori_casa + giocatori_ospite

tutti_i_giocatori = [g for g in tutti_i_giocatori if "Errore" not in g and "Caricamento" not in g]
if not tutti_i_giocatori:
    tutti_i_giocatori = ["Seleziona una squadra per caricare la rosa"]

giocatore_scelto = st.selectbox("Scegli un calciatore attualmente in attività:", tutti_i_giocatori)

tiri_base_giocatore = 2.8 if giocatore_scelto in giocatori_casa else 2.1
difesa_avversaria = gol_subiti_ospite if giocatore_scelto in giocatori_casa else gol_subiti_casa
tiri_attesi = tiri_base_giocatore * (difesa_avversaria / 1.0)

# 7. PULSANTE SIMULAZIONE MONTE CARLO
if st.button("🚀 GENERA PRONOSTICO LIVE"):
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
    prob_over_1_5 = (np.sum(tiri_simulati >= 2) / simulazioni) * 100
    prob_over_2_5 = (np.sum(tiri_simulati >= 3) / simulazioni) * 100

    col_ris1, col_ris2 = st.columns(2)
    
    with col_ris1:
        st.write("### 🏆 Top Risultati Esatti:")
        for ris, conteggio in risultati_ordinati[:3]:
            prob = (conteggio / simulazioni) * 100
            st.success(f"**{ris}** — Probabilità: {prob:.2f}%")
            
    with col_ris2:
        st.write(f"### 📈 Statistiche per {giocatore_scelto}:")
        st.write(f"**Tiri totali stimati per questo match:** {tiri_attesi:.2f}")
        st.info(f"Probabilità Over 1.5 Tiri: **{prob_over_1_5:.2f}%**")
        st.info(f"Probabilità Over 2.5 Tiri: **{prob_over_2_5:.2f}%**")
