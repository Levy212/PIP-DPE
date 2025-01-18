from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Initialisation de l'application Dash
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashbard DPE PIP 2025"

# Chargement des données globales
file_path = "data/dpe_dashboard2.csv"
df = pd.read_csv(file_path, sep=",", low_memory=False)
df = df[df["Surface_habitable_logement"].notna()]  # Supprimer les lignes avec des surfaces invalides
df_appartements = df[df["Type_bâtiment"].isin(["APPARTEMENT", "MAISON"])].copy()

# Ajouter les données globales dans l'application
app.server.df = df
app.server.df_appartements = df_appartements



# Layout principal
app.layout = html.Div([
    dcc.Location(id="url"),  # Composant pour gérer les URL
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Accueil", href="/", active="exact"),
            dbc.NavLink("Présentation du projet", href="/presentation-projet", active="exact"),
            dbc.DropdownMenu(
                label="Analyse descriptive",
                children=[
                    dbc.DropdownMenuItem("Diagramme en bâtons des étiquettes DPE", href="/analyse-descriptive-bar"),
                    dbc.DropdownMenuItem("Diagramme circulaire des étiquettes DPE", href="/analyse-descriptive-pie"),
                    dbc.DropdownMenuItem("Surface moyenne par classe DPE", href="/analyse-descriptive-surface"),
                    dbc.DropdownMenuItem("Coût annuel moyen par étiquette DPE", href="/analyse-descriptive-cost"),
                ],
                nav=True,
                in_navbar=True,
            ),
            dbc.NavLink("Gains énergétiques", href="/gains-energetiques", active="exact"),
            dbc.NavLink("Gain Usage Energétique", href="/gain-usage-energetique", active="exact"),
            dbc.NavLink("Carte dynamique des consommations", href="/carte-dynamique-consommations", active="exact"),
        ],
        brand="Tableau de Bord DPE",
        brand_href="/",
        color="primary",
        dark=True,
    ),
    html.Div(id="page-content")  # Conteneur des pages
])

if __name__ == "__main__":
    from callbacks import *  # Importez les callbacks ici pour éviter les boucles d'import
    app.run_server(debug=True)