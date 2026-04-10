import pandas as pd 
import matplotlib.pyplot as plt

import os 
dossier = os.path.dirname(__file__)
fichier = os.path.join(dossier, "data.csv")

# Charger dataset
df = pd.read_csv(fichier)

print(df.head())

# Aperçu initial 
print("\n--- INFO DATASET ---")
print(df.info())

print("\n--- VALEURS MANQUANTES ---")
print(df.isnull().sum())

# Supprimer lignes sans client
df = df.dropna(subset=["CustomerID"])

# Supprimer quantités négatives
df = df[df["Quantity"] > 0]

# Supprimer prix négatifs ou nuls
df = df[df["UnitPrice"] > 0]

# Conversion date 
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Créer le CA
df["CA"] = df["Quantity"] * df["UnitPrice"]

# Vérification après nettoyage
print("\n--- DATA NETTOYÉE ---")
print(df.head())

# KPI
print("\n--- KPI ---")
print("\nCA total :", df["CA"].sum())
print("\nNombres de transactions :", df["InvoiceNo"].nunique())

panier_moyen = df["CA"].sum() / df["InvoiceNo"].nunique()
print("\nPanier moyen :", round(panier_moyen, 2))

ca_pays = df.groupby("Country")["CA"].sum().sort_values(ascending=False)
print("\n--- CA par pays ---")
print(ca_pays.head(10))

top_clients = df.groupby("CustomerID")["CA"].sum().sort_values(ascending=False)
print("\n--- Top clients ---")
print(top_clients.head(10))

top_produits = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False)
print("\n--- Produits les plus vendus ---")
print(top_produits.head(10))

# Analyse temporelle 
# CA par jour 
ca_jour = df.groupby("InvoiceDate")["CA"].sum()
print("\n--- CA par jour ---")
print(ca_jour.head())

# CA par mois
df["Mois"] = df["InvoiceDate"].dt.to_period("M")
ca_mois = df.groupby("Mois")["CA"].sum()
print("\n--- CA par mois ---")
print(ca_mois)

# Graphique CA par mois
ca_mois.plot(kind="line")

plt.title("Évoltuion du chiffre d'affaires mensuel")
plt.xlabel("Mois")
plt.ylabel("CA")
plt.grid()
plt.tight_layout()
plt.savefig("graph_ca_mois.png")
plt.show()

# Insights
print("\n--- INSIGHTS ---")

top_country = df.groupby("Country")["CA"].sum().idxmax()
print("\nPays le plus rentable :", top_country)

print("\nMeilleur client :", top_clients.idxmax())

print("\nProduit le plus vendu :", top_produits.idxmax())

best_month = ca_mois.idxmax()
print("\nMois avec le plus de ventes :", best_month)

