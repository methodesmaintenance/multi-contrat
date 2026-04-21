import streamlit as st
import pandas as pd
import os

# --- INITIALISATION ---
# Dossier où les contrats seront stockés
WORKING_DIR = "contrats"
if not os.path.exists(WORKING_DIR):
    os.makedirs(WORKING_DIR)

st.set_page_config(page_title="Eiffage Tournées", layout="wide")

# --- FONCTIONS COEUR ---

def get_contracts():
    """Récupère la liste des dossiers de contrats."""
    return [d for d in os.listdir(WORKING_DIR) if os.path.isdir(os.path.join(WORKING_DIR, d))]

@st.cache_data
def load_data(contract_name):
    """Charge les données en cache pour la rapidité."""
    path = os.path.join(WORKING_DIR, contract_name, "data.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# --- BARRE LATÉRALE : NAVIGATION ---

with st.sidebar:
    st.title("Menu")

    page = st.radio("Aller vers :", ["📁 Mes Contrats", "➕ Nouveau Contrat"])

    st.divider()
    if page == "📁 Mes Contrats":
        list_c = get_contracts()
        selection = st.selectbox("Sélectionner un contrat", ["Choisir..."] + list_c)
    else:
        selection = None

# --- PAGE 1 : GESTION DES CONTRATS ---

if page == "📁 Mes Contrats":
    if selection == "Choisir...":
        st.title("Sélection de contrat")
        st.info("Veuillez sélectionner un contrat dans la barre latérale pour visualiser les données.")
    else:
        st.title(f"📍 Contrat : {selection}")

        df = load_data(selection)
        if df is not None:
            st.success(f"Données de {selection} chargées en mémoire.")

            # Affichage des données
            with st.expander("Voir les données brutes"):
                st.dataframe(df, use_container_width=True)

            # Simulation du bouton d'optimisation
            st.divider()
            if st.button(f"🚀 Lancer l'optimisation pour {selection}", type="primary"):
                st.balloons()
                st.info(f"Le moteur d'optimisation utiliserait ici les fichiers de : **{selection}**")
            # Ici s'afficherait le résultat de ton code d'optimisation
            else:
                st.error("Aucun fichier de données trouvé pour ce contrat.")

# --- PAGE 2 : IMPORTATION ---

else:
    st.title("➕ Ajouter un nouveau contrat")
    st.write("Créez un nouvel espace de travail pour un contrat spécifique.")

    with st.form("new_contract_form"):
        new_name = st.text_input("Nom du contrat (ex: La Poste - IDF)")
        uploaded_file = st.file_uploader("Importer le fichier Excel ou CSV", type=["csv", "xlsx"])
        submit = st.form_submit_button("Créer l'interface")

        if submit:
            if new_name and uploaded_file:
                # Création du dossier
                path = os.path.join(WORKING_DIR, new_name)
                os.makedirs(path, exist_ok=True)

                # Sauvegarde (conversion en CSV pour l'uniformité)
                if uploaded_file.name.endswith('.xlsx'):
                    temp_df = pd.read_excel(uploaded_file)
                    temp_df.to_csv(os.path.join(path, "data.csv"), index=False)
                else:
                    with open(os.path.join(path, "data.csv"), "wb") as f:
                        f.write(uploaded_file.getbuffer())

                        st.success(f"Contrat '{new_name}' créé avec succès !")
                        st.info("Vous pouvez maintenant le sélectionner dans le menu 'Mes Contrats'.")
        else:
            st.warning("Veuillez remplir le nom et fournir un fichier.")