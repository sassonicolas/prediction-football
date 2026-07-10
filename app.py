import streamlit as st
import numpy as np
import requests

# 1. INIZIALIZZAZIONE SICURA (QUI DEFINIAMO LE VARIABILI PRIMA DI USARLE)
p_1 = p_X = p_2 = p_GG = p_NG = p_casa_vince_0 = 0.0
risultati_ordinati = [("0 - 0", 0.0), ("1 - 1", 0.0)]
# ... aggiungi qui l'inizializzazione di tutte le altre variabili usate dopo ...

# [Qui inserisci il resto del tuo codice originale: DIZIONARI, FUNZIONI, ECC.]

# 6. ELABORAZIONE (IL TUO BOTTONE)
if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    # Qui inserisci la tua logica di calcolo (con il seed dinamico come ti ho mostrato prima)
    # ...
    # Assicurati che alla fine del blocco, tutte le variabili (p_1, p_NG, ecc.) siano aggiornate
    st.session_state.calcolato = True

# 7 & 8. DISPLAY
# Se p_NG viene stampata qui, ora esiste già grazie all'inizializzazione iniziale.
# Se vuoi mostrare i dati solo dopo il click, usa:
if 'calcolato' in st.session_state:
    # Qui il tuo codice originale per mostrare i risultati
    pass
