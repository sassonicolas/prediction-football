import streamlit as st
import numpy as np
import requests

# 1. CHIAVE API PERSONALE
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.title("⚽ Predittore Super-IA PRO: Match, Player, Angoli & Arbitri")
st.write("Configurazione Mondiale 2026 & Serie A. Trova l'arbitro ufficiale del match e selezionalo per calcolare i cartellini!")

# 2. DIZIONARIO COMPLETO (Tutte le 48 Nazionali del Mondiale 2026 + Serie A)
DIZIONARIO_SQUADRE = {
    # --- SERIE A ---
    "Atalanta (Serie A)": 499, "Bologna (Serie A)": 504, "Cagliari (Serie A)": 490,
    "Como (Serie A)": 511, "Empoli (Serie A)": 512, "Fiorentina (Serie A)": 502,
    "Frosinone (Italia)": 506, "Genoa (Serie A)": 495, "Inter (Serie A)": 496,
    "Juventus (Serie A)": 498, "Lazio (Serie A)": 487, "Lecce (Serie A)": 449,
    "Milan (Serie A)": 489, "Monza (Serie A)": 1579, "Napoli (Serie A)": 492,
    "Parma (Serie A)": 500, "Roma (Serie A)": 497, "Torino (Serie A)": 503,
    "Udinese (Serie A)": 494, "Venezia (Serie A)": 517, "Verona (Serie A)": 505,
    
    # --- TUTTE LE 48 NAZIONALI DEL MONDIALE 2026 ---
    "Algeria (Mondiale)": 32, "Angola (Mondiale)": 1530, "Arabia Saudita (Mondiale)": 24,
    "Argentina (Mondiale)": 26, "Australia (Mondiale)": 20, "Belgio (Mondiale)": 7,
    "Brasile (Mondiale)": 6, "Camerun (Mondiale)": 1502, "Canada (Mondiale)": 549,
    "Cile (Mondiale)": 17, "Cina (Mondiale)": 1493, "Colombia (Mondiale)": 12,
    "Corea del Sud (Mondiale)": 19, "Costa d'Avorio (Mondiale)": 1503, "Costa Rica (Mondiale)": 18,
    "Croazia (Mondiale)": 3, "Danimarca (Mondiale)": 21, "Ecuador (Mondiale)": 13,
    "Egitto (Mondiale)": 33, "Francia (Mondiale)": 2, "Galles (Mondiale)": 767,
    "Germania (Mondiale)": 25, "Ghana (Mondiale)": 1504, "Giappone (Mondiale)": 1024,
    "Honduras (Mondiale)": 1109, "Inghilterra (Mondiale)": 10, "Iran (Mondiale)": 22,
    "Iraq (Mondiale)": 1523, "Italia (Mondiale)": 31, "Marocco (Mondiale)": 30,
    "Messico (Mondiale)": 16, "Nigeria (Mondiale)": 34, "Nuova Zelanda (Mondiale)": 2282,
    "Olanda (Mondiale)": 11, "Panama (Mondiale)": 1105, "Paraguay (Mondiale)": 14,
    "Perù (Mondiale)": 15, "Polonia (Mondiale)": 24, "Portogallo (Mondiale)": 27,
    "Qatar (Mondiale)": 1524, "Repubblica Ceca (Mondiale)": 771, "Senegal (Mondiale)": 1501,
    "Spagna (Mondiale)": 9, "Stati Uniti (Mondiale)": 2383, "Sudafrica (Mondiale)": 1515,
    "Svizzera (Mondiale)": 15, "Tunisia (Mondiale)": 29, "Uruguay (Mondiale)": 8
}

# 3. DATABASE ARBITRI ATTUALI E INTERNAZIONALI
DIZIONARIO_ARBITRI = {
    "Davide Massa (ITA)": {"media_cartellini": 5.1, "severita": "Molto Alta"},
    "Marco Guida (ITA)": {"media_cartellini": 4.2, "severita": "Media"},
    "Fabio Maresca (ITA)": {"media_cartellini": 5.4, "severita": "Estrema"},
    "Simone Sozza (ITA)": {"media_cartellini": 4.4, "severita": "Media"},
    "Maurizio Mariani (ITA)": {"media_cartellini": 4.7, "severita": "Alta"},
    "Michael Oliver (ENG)": {"media_cartellini": 3.6, "severita": "Bassa"},
    "Szymon Marciniak (POL)": {"media_cartellini": 4.0, "severita": "Media"},
    "Clement Turpin (FRA)": {"media_cartellini": 3.8, "severita": "Bassa"},
    "Felix Zwayer (GER)": {"media_cartellini": 4.6, "severita": "Alta"},
    "Wilmar Roldán (COL)": {"media_cartellini": 5.8, "severita": "Estrema"},
    "César Ramos (MEX)": {"media_cartellini": 4.3, "severita": "Media"},
    "Anthony Taylor (ENG)": {"media_cartellini": 4.8, "severita": "Alta"}
}

# 4. RECUPERO DATI LIVE CON CACHE
@st.cache_data(ttl=86400)
def recupera_giocatori_live(team_id):
    url = f"https://v3.football.api-sports.io/players/squads?team={team_id}"
    headers = {'x-rapidapi-key': API_KEY}
    try:
        risposta = requests.get(url, headers=headers).json()
        if risposta.get("response") and len(risposta["response"]) > 0:
            lista_calc = risposta["response"][0]["players"]
            return [g["name"] for g in lista_calc if g["position"] in ["Attacker", "Midfielder"]]
    except:
        pass
    return ["Giocatore Star 1", "Giocatore Star 2"]

@st.cache_data(ttl=86400)
def recupera_statistiche_live(team_id, is_naz):
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
    return (1.8, 1.0) if not is_naz else (2.1, 0.7)

# 5. INTERFACCIA GRAFICA DI SELEZIONE
st.subheader("📋 1. Seleziona le Squadre del Match")
col1, col2 = st.columns(2)
squadre_disponibili = sorted(list(DIZIONARIO_SQUADRE.keys()))

with col1:
    squadra_casa = st.selectbox("Squadra in Casa", squadre_disponibili, index=0)
    id_casa = DIZIONARIO_SQUADRE[squadra_casa]
    gol_fatti_casa, gol_subiti_casa = recupera_statistiche_live(id_casa, "Mondiale" in squadra_casa)

with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", squadre_disponibili, index=1)
    id_ospite = DIZIONARIO_SQUADRE[squadra_ospite]
    gol_fatti_ospite, gol_subiti_ospite = recupera_statistiche_live(id_ospite, "Mondiale" in squadra_ospite)

st.write("---")

# Sezione di scelta Arbitro e Giocatore messi in evidenza
st.subheader("🏁 2. Designazione Arbitro & Giocatore Chiave")
col_a, col_g = st.columns(2)

with col_a:
    arbitro_scelto = st.selectbox("Chi arbitra l'incontro?", list(DIZIONARIO_ARBITRI.keys()))
    dati_arbitro = DIZIONARIO_ARBITRI[arbitro_scelto]
    st.info(f"📊 **Stile di arbitraggio:** Stile {dati_arbitro['severita']} | Media: {dati_arbitro['media_cartellini']} gialli/partita")

with col_g:
    tutti_giocatori = recupera_giocatori_live(id_casa) + recupera_giocatori_live(id_ospite)
    giocatore_scelto = st.selectbox("Scegli il calciatore da monitorare:", tutti_giocatori)

# Calcolo tiri e falli attesi
tiri_base = 2.8 if giocatore_scelto in recupera_giocatori_live(id_casa) else 2.1
tiri_attesi = tiri_base * ((gol_subiti_ospite if giocatore_scelto in recupera_giocatori_live(id_casa) else gol_subiti_casa) / 1.0)

falli_subiti_base = 1.9 if giocatore_scelto in recupera_giocatori_live(id_casa) else 1.6
falli_attesi = falli_subiti_base * ((gol_subiti_ospite if giocatore_scelto in recupera_giocatori_live(id_casa) else gol_subiti_casa) / 0.9)

# 6. ELABORAZIONE DELLE PROBABILITÀ STATISTICHE
if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    simulazioni = 100000
    
    # Simulazione Risultato Esatto
    lambda_casa = gol_fatti_casa * (gol_subiti_ospite / 1.0)
    lambda_ospite = gol_fatti_ospite * (gol_subiti_casa / 1.0)
    gol_casa_sim = np.random.poisson(lambda_casa, simulazioni)
    gol_ospite_sim = np.random.poisson(lambda_ospite, simulazioni)
    
    risultati = {}
    for i in range(simulazioni):
        ris = f"{gol_casa_sim[i]} - {gol_ospite_sim[i]}"
        risultati[ris] = risultati.get(ris, 0) + 1
    risultati_ordinati = sorted(risultati.items(), key=lambda x: x[1], reverse=True)
    
    # Simulazione Angoli
    angoli_attesi = 5.2 * (gol_fatti_casa / 1.5) + 4.3 * (gol_fatti_ospite / 1.5)
    angoli_sim = np.random.poisson(angoli_attesi, simulazioni)
    prob_over_8_5_angoli = (np.sum(angoli_sim >= 9) / simulazioni) * 100
    prob_over_9_5_angoli = (np.sum(angoli_sim >= 10) / simulazioni) * 100
    
    # Simulazione Prestazioni Giocatore
    falli_sim = np.random.poisson(falli_attesi, simulazioni)
    prob_falli_1_5 = (np.sum(falli_sim >= 2) / simulazioni) * 100
    
    # Simulazione Cartellini basata sull'Arbitro
    cartellini_sim = np.random.poisson(dati_arbitro["media_cartellini"], simulazioni)
    prob_over_3_5_cartellini = (np.sum(cartellini_sim >= 4) / simulazioni) * 100
    prob_over_4_5_cartellini = (np.sum(cartellini_sim >= 5) / simulazioni) * 100

    # 7. DISPLAY RISULTATI
    st.write("---")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("### 🏆 Match & Angoli")
        st.success(f"**Top Risultato:** {risultati_ordinati[0][0]} ({(risultati_ordinati[0][1]/simulazioni)*100:.1f}%)")
        st.success(f"**Secondo Migliore:** {risultati_ordinati[1][0]} ({(risultati_ordinati[1][1]/simulazioni)*100:.1f}%)")
        st.write(f"Stima Corner Totali: **{angoli_attesi:.1f}**")
        st.info(f"Probabilità Over 8.5 Angoli: **{prob_over_8_5_angoli:.1f}%**")
        st.info(f"Probabilità Over 9.5 Angoli: **{prob_over_9_5_angoli:.1f}%**")
        
    with c2:
        st.write(f"### 📈 Statistiche {giocatore_scelto}")
        st.write(f"Falli subiti stimati: **{falli_attesi:.1f}**")
        st.info(f"Probabilità Subisce 2+ Falli: **{prob_falli_1_5:.1f}%**")
        
    with c3:
        st.write(f"### 🟨 Sanzioni & Cartellini")
        st.write(f"Fischietto: *{arbitro_scelto}*")
        st.warning(f"Probabilità Over 3.5 Cartellini: **{prob_over_3_5_cartellini:.1f}%**")
        st.warning(f"Probabilità Over 4.5 Cartellini: **{prob_over_4_5_cartellini:.1f}%**")
