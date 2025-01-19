from dash import html, dcc, Input, Output
import pandas as pd
import plotly.graph_objects as go
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

# Mise en page pour le diagramme circulaire
layout = html.Div([
    html.H1(
        "Surface moyenne par classe DPE en fonction du type de bâtiment et du département",
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
    dcc.Graph(id="bar-chart-surface"),
])


# Callback pour Problème 4
@app.callback(
    Output("bar-chart-surface", "figure"),
    [Input("filter-type-batiment-probleme4", "value"),
     Input("filter-departement-probleme4", "value")]
)
def update_bar_chart_surface(filter_batiments, filter_departements):
    filtered_df = df.copy()
    if filter_batiments:
        filtered_df = filtered_df[filtered_df["Type_bâtiment"].isin(filter_batiments)]
    if filter_departements:
        filtered_df = filtered_df[filtered_df["N°_département_(BAN)"].isin(filter_departements)]

    # Vérification des données filtrées
    if filtered_df.empty:
        return go.Figure(
            data=[],
            layout=go.Layout(
                title="Aucune donnée disponible",
                xaxis=dict(title="Classe DPE"),
                yaxis=dict(title="Surface moyenne (m²)"),
            )
        )

    # Calcul de la surface moyenne par étiquette DPE
    average_surface_by_dpe = filtered_df.groupby("Etiquette_DPE")["Surface_habitable_logement"].mean()

    # Créer le graphique en barres
    fig = go.Figure()

    for dpe_class, surface in average_surface_by_dpe.items():
        fig.add_trace(go.Bar(
            x=[dpe_class],
            y=[surface],
            name=f"Classe {dpe_class}",
            text=[f"{int(surface):,} m²"],  # Texte des annotations
            textposition="outside",
            marker=dict(color=etiquette_colors.get(dpe_class, "#d3d3d3"))  # Couleur selon la classe DPE
        ))

    # Mise en page du graphique
    fig.update_layout(
        title="Surface moyenne par classe DPE",
        xaxis_title="Classe DPE",
        yaxis_title="Surface moyenne (m²)",
        xaxis=dict(
            categoryorder="array",
            categoryarray=["A", "B", "C", "D", "E", "F", "G"],  # Ordre des classes DPE
        ),
        yaxis=dict(gridcolor="lightgrey"),
        height=600,  # Agrandir la figure
        barmode="group",  # Barres regroupées
        plot_bgcolor="white",  # Fond blanc
        showlegend=False  # Désactiver la légende
    )

    return fig
