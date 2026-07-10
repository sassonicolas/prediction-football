import streamlit as st
import numpy as np
import requests

# 1. CHIAVE API PERSONALE
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.set_page_config(page_title="Predittore Super-IA PRO", page_icon="⚽", layout="wide")

st.title("⚽ Predittore Super-IA PRO: Match, Player, Angoli & Arbitri")

# --- INIZIALIZZAZIONE DI SICUREZZA (Evita NameError all'avvio) ---
if 'risultati_calcolati' not in st.session_state:
    st.session_state.risultati_calcolati = False
    st.session_state.dati = {}

# [DATABASE SQUADRE E ARBITRI RIMANGONO INVARIATI - OMETTO PER BREVITÀ]
# ... (usa il tuo dizionario DIZIONARIO_SQUADRE e DIZIONARIO_ARBITRI originale) ...

# 5. INTERFACCIA GRAFICA (Semplificata per mantenere la struttura)
col1, col2 = st.columns(2)
squadre_disponibili = sorted(list(DIZIONARIO_SQUADRE.keys()))
squadra_casa = col1.selectbox("Squadra in Casa", squadre_disponibili)
squadra_ospite = col2.selectbox("Squadra Ospite", squadre_disponibili)

col_a, col_g = st.columns(2)
arbitro_scelto = col_a.selectbox("Arbitro", list(DIZIONARIO_ARBITRI.keys()))
# ... (codice recupero giocatori) ...

if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    # ESECUZIONE CALCOLI (Monte Carlo)
    # [Qui metti la tua logica di calcolo originale...]
    
    # Salviamo tutto in session_state per non perdere i dati
    st.session_state.risultati_calcolati = True
    st.session_state.dati = {
        "p_1": p_1, "p_X": p_X, "p_2": p_2, "p_GG": p_GG, "p_NG": p_NG,
        "risultati": risultati_ordinati, "angoli": angoli_attesi,
        "cartellini": prob_over_4_5_cartellini
    }

# 7 & 8. DISPLAY SEZIONE RESOCONTO (Solo se i dati esistono)
if st.session_state.risultati_calcolati:
    d = st.session_state.dati
    st.write("---")
    c1, c2, c3 = st.columns(3)
    c1.success(f"**Top Risultato:** {d['risultati'][0][0]}")
    c3.warning(f"Probabilità Over 4.5 Cartellini: **{d['cartellini']:.1f}%**")
    
    # ... (il resto del tuo tabellone tab1, tab2, tab3) ...
else:
    st.info("Premi il bottone sopra per visualizzare l'analisi.")
