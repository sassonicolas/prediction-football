import streamlit as st
import numpy as np
import requests

# Configurazione Pagina
st.set_page_config(page_title="Predittore Super-IA PRO", layout="wide")
st.title("⚽ Predittore Super-IA PRO")

# Inizializzazione Session State per evitare NameError
if 'dati_simulati' not in st.session_state:
    st.session_state.dati_simulati = None

# Esempio Semplificato di Struttura
squadra_casa = st.selectbox("Squadra in Casa", ["Inter", "Juventus", "Milan"])
squadra_ospite = st.selectbox("Squadra Ospite", ["Roma", "Lazio", "Napoli"])
giocatore_scelto = st.text_input("Giocatore da monitorare")

if st.button("🚀 GENERA ANALISI"):
    # Logica di calcolo (Qui simuliamo i dati)
    p_gol = 45.0
    p_assist = 30.0
    p_gol_assist = 65.0
    
    st.session_state.dati_simulati = {
        "p_gol": p_gol,
        "p_assist": p_assist,
        "p_gol_assist": p_gol_assist
    }

# Display dei risultati (Manteniamo la struttura con le colonne)
st.write("---")
c1, c2, c3 = st.columns(3)

with c2:
    st.write(f"### 📈 Performance {giocatore_scelto}")
    if st.session_state.dati_simulati:
        d = st.session_state.dati_simulati
        st.info(f"⚽ Probabilità GOL: **{d['p_gol']:.1f}%**")
        st.info(f"🎯 Probabilità ASSIST: **{d['p_assist']:.1f}%**")
        st.warning(f"🚀 **Probabilità GOL o ASSIST: {d['p_gol_assist']:.1f}%**")
    else:
        st.write("Premi il bottone per le statistiche.")
