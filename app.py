import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import os 
dossier = os.path.dirname(__file__)
fichier = os.path.join(dossier, "data.csv")

st.title("📊 Dashboard E-commerce")
st.markdown("---")
st.write("Analyse des performances e-commerce à partir d'un dataset réel.")

# Charger données
df = pd.read_csv(fichier)

# Nettoyage
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["CA"] = df["Quantity"] * df["UnitPrice"]

# KPI
st.header("📈 Indicateurs clés")

ca_total = df["CA"].sum()
nb_commandes = df["InvoiceNo"].nunique()
panier_moyen = ca_total / nb_commandes

col1, col2, col3 = st.columns(3)

col1.metric("💰 CA total", f"{round(ca_total, 2)} €")
col2.metric("🧾 Commandes", nb_commandes)
col3.metric("🛒 Panier moyen", f"{round(panier_moyen, 2)} €")

# Filtre pays
st.markdown("---")
st.header("🌍 Analyse par pays")

countries = ["Tous les pays"] + list(df["Country"].unique())
country = st.selectbox("Choisir un pays", countries)

if country =="Tous les pays":
    df_filtre = df
else:
    df_filtre = df[df["Country"] == country]

# CA par produit
st.markdown("---")
st.header("📦 Produits")
st.subheader("Top 5 produits par chiffre d'affaires")
ca_produit = df_filtre.groupby("Description")["CA"].sum().sort_values(ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10,6))
ca_produit.plot(kind="bar", ax=ax)

ax.set_title("Top 5 produits (CA)")

plt.xticks(rotation=30, ha="right")
ax.grid(axis="y")
plt.tight_layout()

st.pyplot(fig)

# Évolution mensuelle
st.markdown("---")
st.header("📅 Évolution temporelle")

df_filtre["Mois"] = df_filtre["InvoiceDate"].dt.to_period("M")
ca_mois = df_filtre.groupby("Mois")["CA"].sum()

fig2, ax2 = plt.subplots()
ca_mois.plot(kind="line", ax=ax2)

plt.title("Évolution mensuelle")

st.pyplot(fig2)