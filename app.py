import streamlit as st
import numpy as np

# Inizializzazione sicura: definisci qui tutte le variabili usate
p_GG = 50.0 
p_NG = 50.0

st.title("⚽ Predittore Super-IA PRO")

# Blocco logico separato
if st.button("🚀 GENERA ANALISI"):
    # Esempio di calcolo
    p_GG = 60.0 
    p_NG = 100.0 - p_GG
    st.write(f"Probabilità No Goal: {p_NG}%")

# Stampa di stato che non va in errore perché la variabile è già definita sopra
st.write(f"Stato corrente: {p_NG}")
