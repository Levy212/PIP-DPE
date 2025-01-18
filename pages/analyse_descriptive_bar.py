from dash import html, dcc, Input, Output
import plotly.express as px
from app import app, df

# Récupérer les données globales
df = app.server.df
df_appartements = app.server.df_appartements

# Couleurs des étiquettes
etiquette_colors = {
    'A': '#00cc00',  # Vert foncé
    'B': '#66ff66',  # Vert clair
    'C': '#ffff00',  # Jaune
    'D': '#ffcc00',  # Orange clair
    'E': '#ff9900',  # Orange foncé
    'F': '#ff3300',  # Rouge clair
    'G': '#cc0000',  # Rouge foncé
}

# Forcer l'ordre des catégories
etiquette_order = list(etiquette_colors.keys())

# Layout de la page
layout = html.Div([
    html.H1(
        "Diagramme en bâtons des étiquettes DPE en fonction du type de bâtiment et du département",
        style={"text-align": "center"}
    ),

    # Filtres interactifs
    html.Div([
        html.Label("Filtrer par Type de Bâtiment :"),
        dcc.Dropdown(
            id="filter-type-batiment",
            options=[{"label": val, "value": val} for val in df["Type_bâtiment"].dropna().unique()],
            value=[],
            placeholder="Sélectionnez un ou plusieurs Types de Bâtiment",
            multi=True,  # Permet la sélection multiple
        ),
    ], style={"margin-bottom": "20px"}),

    html.Div([
        html.Label("Filtrer par Département :"),
        dcc.Dropdown(
            id="filter-departement",
            options=[{"label": val, "value": val} for val in df["N°_département_(BAN)"].dropna().unique()],
            value=[],
            placeholder="Sélectionnez un ou plusieurs Départements",
            multi=True,  # Permet la sélection multiple
        ),
    ], style={"margin-bottom": "20px"}),

    # Titre interactif
    html.H3(id="dynamic-title", style={"text-align": "center", "margin-top": "20px"}),

    # Histogramme interactif
    dcc.Graph(id="graph-histogram"),
])

# Callback pour mettre à jour le titre et l'histogramme
@app.callback(
    [Output("dynamic-title", "children"),
     Output("graph-histogram", "figure")],
    [
        Input("filter-type-batiment", "value"),
        Input("filter-departement", "value"),
    ]
)
def update_dashboard(filter_batiments, filter_departements):
    # Appliquer les filtres
    filtered_df = df.copy()
    if filter_batiments:  # Vérifier si une liste non vide de types de bâtiment est fournie
        filtered_df = filtered_df[filtered_df["Type_bâtiment"].isin(filter_batiments)]
    if filter_departements:  # Vérifier si une liste non vide de départements est fournie
        filtered_df = filtered_df[filtered_df["N°_département_(BAN)"].isin(filter_departements)]

    # Titre dynamique pour le graphique
    if filter_batiments or filter_departements:
        graph_title = "Statistiques en fonction du filtre appliqué"
    else:
        graph_title = "Statistiques sur la base de données entière"

    # Titre interactif
    title_parts = []
    if filter_batiments:
        title_parts.append(f"Type(s) de Bâtiment : {', '.join(filter_batiments)}")
    if filter_departements:
        title_parts.append(f"Département(s) : {', '.join(map(str, filter_departements))}")
    title = " | ".join(title_parts) if title_parts else "Statistiques sur la base de données entière"

    # Vérification des données filtrées
    if filtered_df.empty:
        return "Aucune donnée disponible", px.scatter(title="Aucune donnée disponible après filtrage.")

    # Créer l'histogramme pour Etiquette_DPE
    fig = px.histogram(
        filtered_df,
        x="Etiquette_DPE",
        color="Etiquette_DPE",
        category_orders={"Etiquette_DPE": etiquette_order},
        title=graph_title,
        labels={"Etiquette_DPE": "Étiquette DPE"},
        color_discrete_map=etiquette_colors
    )
    fig.update_layout(xaxis_title="Étiquette DPE", yaxis_title="Nombre", bargap=0.2)

    return title, fig
