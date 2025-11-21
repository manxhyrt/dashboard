import streamlit as st
import pandas as pd
import plotly as px

# ================================
# 🚇 Dashboard RATP - 1er trimestre
# ================================

st.set_page_config(page_title="Dashboard RATP", layout="wide")

# --- Titre principal ---
st.title("📊 Dashboard RATP - Validations des titres de transport (1er trimestre)")

# --- Chargement des données ---
data = pd.read_csv(
    "TP Dashboard/validations-reseau-ferre-nombre-validations-par-jour-1er-trimestre.csv",
    sep=";"
)

# Conversion des dates
data["jour"] = pd.to_datetime(data["jour"], dayfirst=True)

# ================================
# 🚇 KPI en haut du dashboard
# ================================
col1, col2 = st.columns(2)

# Nombre de stations uniques
nb_stations = data["libelle_arret"].nunique()

# Nombre total de validations
nb_validations = data["nb_vald"].sum()

with col1:
    st.metric(
        label="Nombre de stations",
        value=f"{nb_stations}"
    )

with col2:
    st.metric(
        label="Nombre total de validations",
        value=f"{nb_validations:,}"  # séparateur de milliers
    )
    

# ================================
# 🎛️ Filtres
# ================================
st.sidebar.header("Filtres")

mois = st.sidebar.selectbox("Choisir un mois", sorted(data["Mois"].unique()))

# --- Application des filtres ---
data_filtered = data[(data["Mois"] == mois)]

st.subheader("📂 Données filtrées")
st.dataframe(data_filtered, use_container_width=True)




# ================================
# 📈 Graphique 1 : Courbe par jour
# ================================
data_grouped_jour = (
    data.groupby("jour")["nb_vald"]
    .sum()
    .reset_index()
)

fig_jour = px.line(
    data_grouped_jour,
    x="jour",
    y="nb_vald",
    title="Évolution des validations par jour",
    labels={"jour": "Jour", "nb_vald": "Nombre de validations"},
    markers=True
)
st.plotly_chart(fig_jour, use_container_width=True)

# ================================
# 📊 Graphique 2 : Barres par mois et catégorie
# ================================
data_grouped_mois = (
    data.groupby(["Mois", "categorie_titre"])["nb_vald"]
    .sum()
    .reset_index()
)
# --- Préparer les données en pourcentage ---
data_grouped_mois_pct = (
    data_grouped_mois
    .groupby("Mois")
    .apply(lambda d: d.assign(pct = d["nb_vald"] / d["nb_vald"].sum() * 100))
    .reset_index(drop=True)
)

# --- Graphique en 100% ---
fig_mois_pct = px.bar(
    data_grouped_mois_pct,
    x="Mois",
    y="pct",
    color="categorie_titre",
    title="Répartition en % des validations par mois et par catégorie",
    labels={"pct": "Part (%)", "Mois": "Mois"},
    text_auto=".1f"  # affiche les % sur les barres
)

# Barres empilées en 100%
fig_mois_pct.update_layout(barmode="stack", yaxis=dict(ticksuffix="%"))

st.plotly_chart(fig_mois_pct, use_container_width=True)
# ================================
# 🚉 Graphique 3 : Top 10 des arrêts
# ================================
data_grouped_arret = (
    data.groupby("libelle_arret")["nb_vald"]
    .sum()
    .reset_index()
    .sort_values(by="nb_vald", ascending=False)
    .head(10)
)

fig_arret = px.bar(
    data_grouped_arret,
    x="libelle_arret",
    y="nb_vald",
    title="Top 10 des arrêts les plus validés",
    labels={"libelle_arret": "Arrêt", "nb_vald": "Nombre de validations"},
    color="nb_vald",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_arret, use_container_width=True)


