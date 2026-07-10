import streamlit as st
import numpy as np
import requests

# 1. CHIAVE API
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.set_page_config(page_title="Predittore Super-IA PRO", page_icon="⚽", layout="wide")
st.title("⚽ Predittore Super-IA PRO")

# --- INIZIALIZZAZIONE SICURA ---
if 'dati_simulati' not in st.session_state:
    st.session_state.dati_simulati = None

# --- DIZIONARI (Omettiamo per brevità, mantieni i tuoi originali) ---
# [INSERISCI QUI IL TUO DIZIONARIO_SQUADRE E DIZIONARIO_ARBITRI]

# ... (funzioni recupera_giocatori_live e recupera_statistiche_live invariate) ...

# 5. INTERFACCIA
squadra_casa = st.selectbox("Squadra in Casa", sorted(list(DIZIONARIO_SQUADRE.keys())))
squadra_ospite = st.selectbox("Squadra Ospite", sorted(list(DIZIONARIO_SQUADRE.keys())))
id_casa = DIZIONARIO_SQUADRE[squadra_casa]
id_ospite = DIZIONARIO_SQUADRE[squadra_ospite]

arbitro_scelto = st.selectbox("Arbitro", list(DIZIONARIO_ARBITRI.keys()))
lista_casa = recupera_giocatori_live(squadra_casa, id_casa)
giocatore_scelto = st.selectbox("Giocatore da monitorare:", lista_casa + recupera_giocatori_live(squadra_ospite, id_ospite))

# 6. CALCOLI
if st.button("🚀 GENERA ANALISI"):
    gol_fatti_casa, gol_subiti_casa = recupera_statistiche_live(squadra_casa, id_casa, "Mondiale" in squadra_casa)
    gol_fatti_ospite, gol_subiti_ospite = recupera_statistiche_live(squadra_ospite, id_ospite, "Mondiale" in squadra_ospite)
    
    # Logica GOL/ASSIST
    potenziale = (gol_fatti_casa if giocatore_scelto in lista_casa else gol_fatti_ospite) / 2.0
    p_gol = min(potenziale * 0.40, 0.80) * 100
    p_assist = min(potenziale * 0.30, 0.60) * 100
    p_gol_assist = min(p_gol + p_assist - (p_gol * p_assist / 100) + 10, 95)
    
    # Salvataggio in session_state per non perdere i dati
    st.session_state.dati_simulati = {
        "p_gol": p_gol, "p_assist": p_assist, "p_gol_assist": p_gol_assist,
        "risultato": "1-1", "angoli": 9.5, "cartellini": 4.2 # Esempio valori
    }

# 7. DISPLAY (Mantiene la tua struttura originale)
st.write("---")
c1, c2, c3 = st.columns(3)

with c2
