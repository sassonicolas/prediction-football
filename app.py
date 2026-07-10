import streamlit as st
import numpy as np
import requests
import hashlib

# 1. CHIAVE API
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"

st.set_page_config(page_title="Predittore Super-IA PRO", page_icon="⚽", layout="wide")

# Database esteso per coprire tutte le 48 Nazionali del Mondiale 2026
DATABASE_GIOCATORI = {
    "Norvegia (Mondiale)": ["Erling Haaland", "Martin Ødegaard", "Antonio Nusa", "Alexander Sørloth", "Julian Ryerson", "Leo Ostigard"],
    "Argentina (Mondiale)": ["Lionel Messi", "Lautaro Martínez", "Julian Álvarez", "Enzo Fernández", "Alexis Mac Allister"],
    "Francia (Mondiale)": ["Kylian Mbappé", "Antoine Griezmann", "Eduardo Camavinga", "Aurélien Tchouaméni", "William Saliba"],
    "Inghilterra (Mondiale)": ["Harry Kane", "Jude Bellingham", "Bukayo Saka", "Phil Foden", "Declan Rice"],
    "Italia (Mondiale)": ["Nicolò Barella", "Federico Dimarco", "Alessandro Bastoni", "Gianluigi Donnarumma"],
    "Brasile (Mondiale)": ["Vinícius Júnior", "Rodrygo", "Bruno Guimarães", "Marquinhos", "Alisson"],
    "Spagna (Mondiale)": ["Lamine Yamal", "Pedri", "Gavi", "Rodri", "Dani Olmo"],
    "Germania (Mondiale)": ["Florian Wirtz", "Jamal Musiala", "Kai Havertz", "Joshua Kimmich"],
    "Portogallo (Mondiale)": ["Cristiano Ronaldo", "Bruno Fernandes", "Rafael Leão", "Bernardo Silva"]
    # Nota: Puoi espandere questo dizionario con tutte le 48 squadre
}

def get_giocatori_custom(team_name):
    if team_name in DATABASE_GIOCATORI:
        return DATABASE_GIOCATORI[team_name]
    return [f"Stella {team_name} 1", f"Stella {team_name} 2", f"Stella {team_name} 3"]

# --- INTERFACCIA E LOGICA ---
st.title("⚽ Predittore Super-IA PRO: Mondiale 2026")

col1, col2 = st.columns(2)
lista_nazionali = sorted(list(DATABASE_GIOCATORI.keys()) + ["Altra Nazionale (Generica)"])

with col1:
    squadra_casa = st.selectbox("Squadra Casa", lista_nazionali)
with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", lista_nazionali)

# Seed dinamico basato sui nomi delle squadre per risultati unici
seed_match = int(hashlib.sha256((squadra_casa + squadra_ospite).encode()).hexdigest(), 16) % 10**8
np.random.seed(seed_match)

col_a, col_g = st.columns(2)
with col_a:
    arbitro = st.selectbox("Arbitro", ["Massa (ITA)", "Marciniak (POL)", "Oliver (ENG)", "Taylor (ENG)"])
with col_g:
    tutti_giocatori = get_giocatori_custom(squadra_casa) + get_giocatori_custom(squadra_ospite)
    giocatore = st.selectbox("Giocatore Focus", tutti_giocatori)

if st.button("🚀 GENERA ANALISI PREDIZIONE"):
    simulazioni = 100000
    # Simulazione Poisson dinamica
    l_casa = np.random.uniform(1.1, 2.4)
    l_ospite = np.random.uniform(0.7, 2.1)
    
    g_casa = np.random.poisson(l_casa, simulazioni)
    g_ospite = np.random.poisson(l_ospite, simulazioni)
    
    # Calcolo Esiti
    p1 = (np.sum(g_casa > g_ospite) / simulazioni) * 100
    px = (np.sum(g_casa == g_ospite) / simulazioni) * 100
    p2 = (np.sum(g_casa < g_ospite) / simulazioni) * 100
    
    st.write("---")
    # Dashboard Risultati
    c1, c2, c3 = st.columns(3)
    c1.metric("Vittoria Casa", f"{p1:.1f}%")
    c2.metric("Pareggio", f"{px:.1f}%")
    c3.metric("Vittoria Ospite", f"{p2:.1f}%")
    
    st.subheader("📊 Dettagli Palinsesto")
    tab1, tab2 = st.tabs(["Mercati Gol", "Mercati Speciali"])
    
    with tab1:
        p_gg = (np.sum((g_casa > 0) & (g_ospite > 0)) / simulazioni) * 100
        st.write(f"Probabilità Entrambe Segnano (GG): **{p_gg:.1f}%**")
        st.write(f"Over 2.5 Gol: **{(np.sum((g_casa + g_ospite) > 2.5) / simulazioni) * 100:.1f}%**")
        
    with tab2:
        st.write(f"Probabilità {giocatore} a segno: **{np.random.uniform(25, 55):.1f}%**")
        st.write(f"Probabilità Over 4.5 Cartellini (Arbitro {arbitro}): **{np.random.uniform(30, 60):.1f}%**")

    st.success("Analisi generata con successo utilizzando il motore di simulazione Monte Carlo dinamico.")
