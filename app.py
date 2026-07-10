import streamlit as st
import numpy as np
import requests

# Inizializziamo le variabili per evitare NameError
p_NG = 0.0 

st.title("⚽ Predittore Super-IA PRO")

# Definizione logica
if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    # Qui vanno i tuoi calcoli...
    p_GG = 50.0 # Esempio
    p_NG = 100.0 - p_GG
    st.write(f"Probabilità No Goal: {p_NG}%")

# Se devi stampare p_NG fuori dal bottone, assicurati che sia inizializzato
st.write(f"Stato corrente: {p_NG}")
