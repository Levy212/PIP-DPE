from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from app import app, df


# Récupérer les données globales
df = app.server.df
df_appartements = app.server.df_appartements
# Couleurs des étiquettes DPE
etiquette_colors = {
    'A': '#00cc00',  # Vert foncé
    'B': '#66ff66',  # Vert clair
    'C': '#ffff00',  # Jaune
    'D': '#ffcc00',  # Orange clair
    'E': '#ff9900',  # Orange foncé
    'F': '#ff3300',  # Rouge clair
    'G': '#cc0000',  # Rouge foncé
}

# Mise en page pour Problème 3
# Mise en page pour le diagramme circulaire
layout = html.Div([
    html.H1(
        "Coût annuel moyen par étiquette DPE en fonction du type de bâtiment et du département",
        style={"text-align": "center"}
    ),

    # Filtres interactifs
    html.Div([
        html.Label("Filtrer par Type de Bâtiment :"),
        dcc.Dropdown(
            id="filter-type-batiment-probleme4",
            options=[{"label": val, "value": val} for val in df["Type_bâtiment"].dropna().unique()],
            value=[],
            placeholder="Sélectionnez un ou plusieurs Types de Bâtiment",
            multi=True,
        ),
    ], style={"margin-bottom": "20px"}),

    html.Div([
        html.Label("Filtrer par Département :"),
        dcc.Dropdown(
            id="filter-departement-probleme4",
            options=[{"label": val, "value": val} for val in df["N°_département_(BAN)"].dropna().unique()],
            value=[],
            placeholder="Sélectionnez un ou plusieurs Départements",
            multi=True,
        ),
    ], style={"margin-bottom": "20px"}),

    # Graphique interactif
    dcc.Graph(id="bar-chart-cost"),
])


# Callback pour Problème 4
@app.callback(
    Output("bar-chart-cost", "figure"),
    [Input("filter-type-batiment-probleme4", "value"),
     Input("filter-departement-probleme4", "value")]
)
def update_bar_chart(filter_batiments, filter_departements):
    filtered_df = df.copy()
    if filter_batiments:
        filtered_df = filtered_df[filtered_df["Type_bâtiment"].isin(filter_batiments)]
    if filter_departements:
        filtered_df = filtered_df[filtered_df["N°_département_(BAN)"].isin(filter_departements)]

    # Vérification des données filtrées
    if filtered_df.empty:
        return px.bar(
            x=["Aucune donnée"],
            y=[0],
            title="Aucune donnée disponible",
            labels={"x": "Classe DPE", "y": "Coût annuel moyen (€)"},
            color_discrete_sequence=["#d3d3d3"]  # Couleur grise
        )

    # Calcul du coût annuel moyen par étiquette DPE
    average_cost_by_dpe = filtered_df.groupby("Etiquette_DPE")["Coût_total_5_usages"].mean()

    # Créer le graphique en barres
    fig = px.bar(
        x=average_cost_by_dpe.index,
        y=average_cost_by_dpe.values,
        title="Coût annuel moyen par étiquette DPE",
        labels={"x": "Classe DPE", "y": "Coût annuel moyen (€)"},
        color=average_cost_by_dpe.index,
        color_discrete_map=etiquette_colors
    )

    # Ajouter des annotations sur les barres
    fig.update_traces(
        texttemplate='%{y:.0f} €',  # Afficher le coût en euros
        textposition="outside"
    )

    # Mise en page
    fig.update_layout(
        title_font_size=20,
        xaxis_title="Classe DPE",
        yaxis_title="Coût annuel moyen (€)",
        xaxis=dict(categoryorder="array", categoryarray=["A", "B", "C", "D", "E", "F", "G"]),
        height=600  # Agrandir la figure
    )

    return fig
