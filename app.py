# 6. ELABORAZIONE DELLE PROBABILITÀ STATISTICHE (Versione aggiornata che garantisce varietà nei risultati)
if st.button("🚀 GENERA ANALISI PREDIZIONE COMPLETA"):
    # Usiamo un seed basato sulle squadre per avere risultati diversi a ogni match
    seed_dinamico = int(str(id_casa) + str(id_ospite))
    np.random.seed(seed_dinamico)
    
    simulazioni = 100000
    
    # Calcolo con piccola variabilità casuale per non avere risultati sempre identici
    var_c = np.random.uniform(0.95, 1.05)
    var_o = np.random.uniform(0.95, 1.05)
    
    lambda_casa = (gol_fatti_casa * (gol_subiti_ospite / 1.2)) * var_c
    lambda_ospite = (gol_fatti_ospite * (gol_subiti_casa / 1.2)) * var_o
    
    gol_casa_sim = np.random.poisson(lambda_casa, simulazioni)
    gol_ospite_sim = np.random.poisson(lambda_ospite, simulazioni)
    
    # Calcolo risultati esatti
    risultati = {}
    for i in range(simulazioni):
        ris = f"{gol_casa_sim[i]} - {gol_ospite_sim[i]}"
        risultati[ris] = risultati.get(ris, 0) + 1
    risultati_ordinati = sorted(risultati.items(), key=lambda x: x[1], reverse=True)
    
    # Calcolo mercati (tutto il resto invariato)
    angoli_attesi = 5.2 * (gol_fatti_casa / 1.5) + 4.3 * (gol_fatti_ospite / 1.5)
    angoli_sim = np.random.poisson(angoli_attesi, simulazioni)
    prob_over_8_5_angoli = (np.sum(angoli_sim >= 9) / simulazioni) * 100
    prob_over_9_5_angoli = (np.sum(angoli_sim >= 10) / simulazioni) * 100
    
    falli_sim = np.random.poisson(falli_attesi, simulazioni)
    prob_falli_1_5 = (np.sum(falli_sim >= 2) / simulazioni) * 100
    
    cartellini_sim = np.random.poisson(dati_arbitro["media_cartellini"], simulazioni)
    prob_over_3_5_cartellini = (np.sum(cartellini_sim >= 4) / simulazioni) * 100
    prob_over_4_5_cartellini = (np.sum(cartellini_sim >= 5) / simulazioni) * 100

    tot_gol_sim = gol_casa_sim + gol_ospite_sim
    p_1 = (np.sum(gol_casa_sim > gol_ospite_sim) / simulazioni) * 100
    p_X = (np.sum(gol_casa_sim == gol_ospite_sim) / simulazioni) * 100
    p_2 = (np.sum(gol_casa_sim < gol_ospite_sim) / simulazioni) * 100
    p_GG = (np.sum((gol_casa_sim > 0) & (gol_ospite_sim > 0)) / simulazioni) * 100
    p_NG = 100 - p_GG
    p_casa_vince_0 = (np.sum((gol_casa_sim > gol_ospite_sim) & (gol_ospite_sim == 0)) / simulazioni) * 100

    m_1_2 = (np.sum((tot_gol_sim >= 1) & (tot_gol_sim <= 2)) / simulazioni) * 100
    m_2_4 = (np.sum((tot_gol_sim >= 2) & (tot_gol_sim <= 4)) / simulazioni) * 100
    m_3_5 = (np.sum((tot_gol_sim >= 3) & (tot_gol_sim <= 5)) / simulazioni) * 100

    m_c_1_2 = (np.sum((gol_casa_sim >= 1) & (gol_casa_sim <= 2)) / simulazioni) * 100
    m_c_2_3 = (np.sum((gol_casa_sim >= 2) & (gol_casa_sim <= 3)) / simulazioni) * 100
    m_o_1_2 = (np.sum((gol_ospite_sim >= 1) & (gol_ospite_sim <= 2)) / simulazioni) * 100
    m_o_2_3 = (np.sum((gol_ospite_sim >= 2) & (gol_ospite_sim <= 3)) / simulazioni) * 100
