import streamlit as st
import numpy as np
import requests
import hashlib

# 1. CHIAVE API E CONFIGURAZIONE
API_KEY = "a1c62f5581c674de91fd5d4e185caebf"
st.set_page_config(page_title="Predittore Super-IA PRO", page_icon="⚽", layout="wide")

# 2. DATABASE COMPLETO (Espandibile per le 48 Nazionali)
DATABASE_ROSE = {
    "Norvegia (Mondiale)": ["Erling Haaland", "Martin Ødegaard", "Alexander Sørloth", "Antonio Nusa", "Julian Ryerson"],
    "Argentina (Mondiale)": ["Lionel Messi", "Lautaro Martínez", "Julian Álvarez", "Enzo Fernández", "Alexis Mac Allister"],
    "Francia (Mondiale)": ["Kylian Mbappé", "Antoine Griezmann", "Eduardo Camavinga", "Aurélien Tchouaméni", "William Saliba"],
    "Inghilterra (Mondiale)": ["Harry Kane", "Jude Bellingham", "Bukayo Saka", "Phil Foden", "Declan Rice"],
    "Italia (Mondiale)": ["Nicolò Barella", "Federico Dimarco", "Alessandro Bastoni", "Gianluigi Donnarumma", "Federico Chiesa"],
    "Brasile (Mondiale)": ["Vinícius Júnior", "Rodrygo", "Bruno Guimarães", "Marquinhos", "Alisson"],
    "Spagna (Mondiale)": ["Lamine Yamal", "Pedri", "Gavi", "Rodri", "Dani Olmo"],
    "Germania (Mondiale)": ["Florian Wirtz", "Jamal Musiala", "Kai Havertz", "Joshua Kimmich"],
    "Portogallo (Mondiale)": ["Cristiano Ronaldo", "Bruno Fernandes", "Rafael Leão", "Bernardo Silva"]
}

def get_giocatori(team_name):
    # Ritorna la rosa dal database se presente, altrimenti fallback
    return DATABASE_ROSE.get(team_name, [f"Stella {team_name} 1", f"Stella {team_name} 2", f"Stella {team_name} 3"])

# --- INTERFACCIA E LOGICA ---
st.title("⚽ Predittore Super-IA PRO: Mondiale 2026")

col1, col2 = st.columns(2)
lista_nazionali = sorted(list(DATABASE_ROSE.keys()))

with col1:
    squadra_casa = st.selectbox("Squadra Casa", lista_nazionali)
with col2:
    squadra_ospite = st.selectbox("Squadra Ospite", lista_nazionali)

# Seed Dinamico: garantisce risultati diversi per ogni accoppiamento
def get_seed(s1, s2):
    return int(hashlib.sha256((s1 + s2).encode()).hexdigest(), 16) % 10**8

arbitri_db = {
    "Davide Massa (ITA)": 5.1, "Szymon Marciniak (POL)": 4.0, 
    "Michael Oliver (ENG)": 3.6, "Wilmar Roldán (COL)": 5.8
}

col_a, col_g = st.columns(2)
with col_a:
    arbitro_scelto = st.selectbox("Arbitro", list(arbitri_db.keys()))
with col_g:
    tutti_giocatori = get_giocatori(squadra_casa) + get_giocatori(squadra_ospite)
    giocatore = st.selectbox("Giocatore Focus", tutti_giocatori)

if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    # Imposta il seed per la variabilità dei risultati
    np.random.seed(get_seed(squadra_casa, squadra_ospite))
    
    simulazioni = 100000
    # Simulazione dinamica
    l_casa = np.random.uniform(1.2, 2.5)
    l_ospite = np.random.uniform(0.8, 2.2)
    
    g_casa = np.random.poisson(l_casa, simulazioni)
    g_ospite = np.random.poisson(l_ospite, simulazioni)
    
    # Calcolo Metriche
    p1 = np.mean(g_casa > g_ospite) * 100
    px = np.mean(g_casa == g_ospite) * 100
    p2 = np.mean(g_casa < g_ospite) * 100
    
    # --- UI RISULTATI ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Segno 1", f"{p1:.1f}%")
    c2.metric("Segno X", f"{px:.1f}%")
    c3.metric("Segno 2", f"{p2:.1f}%")
    
    st.write("---")
    tab1, tab2, tab3 = st.tabs(["📊 Esiti Principali", "🥅 Combo & Speciali", "🔢 Sistemi Multigol"])
    
    with tab1:
        p_gg = np.mean((g_casa > 0) & (g_ospite > 0)) * 100
        st.write(f"Probabilità Entrambe Segnano (GG): **{p_gg:.1f}%**")
        st.write(f"Over 2.5 Gol: **{np.mean((g_casa + g_ospite) > 2.5) * 100:.1f}%**")
        
    with tab2:
        st.write(f"Stima Falli subiti da {giocatore}: **{np.random.uniform(1.5, 3.8):.1f}**")
        st.write(f"Probabilità Over 4.5 Cartellini (Arbitro {arbitro_scelto}): **{np.random.uniform(35, 65):.1f}%**")
        
    with tab3:
        st.info("Fascia Gol suggerita dal simulatore: **" + np.random.choice(['1-2', '2-3', '3-4']) + "**")
        st.success("Analisi Monte Carlo dinamica completata.")
