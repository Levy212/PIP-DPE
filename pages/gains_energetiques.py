from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from app import app, df

# Récupérer les données globales
df = app.server.df
df_appartements = app.server.df_appartements

# Couleurs des étiquettes
dpe_colors = {
    'A': '#00cc00',  # Vert foncé
    'B': '#66ff66',  # Vert clair
    'C': '#ffff00',  # Jaune
    'D': '#ffcc00',  # Orange clair
    'E': '#ff9900',  # Orange foncé
    'F': '#ff3300',  # Rouge clair
    'G': '#cc0000',  # Rouge foncé
}

# Mise en page pour le graphique interactif
layout = html.Div([
    html.H1(
        "Gains énergétiques par étiquette DPE",
        style={"text-align": "center", "margin-bottom": "30px"}
    ),

    # Filtres interactifs
    html.Div([
        html.Div([
            html.Label("Filtrer par Étiquette DPE :", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="filter-dpe",
                options=[{"label": etiq, "value": etiq} for etiq in df["Etiquette_DPE"].dropna().unique()],
                value="A",
                placeholder="Sélectionnez une étiquette",
                multi=False,
                style={"width": "50%", "margin": "0 auto"}
            ),
        ], style={"margin-bottom": "20px", "text-align": "center"}),

        html.Div([
            html.Label("Choisir l'unité des gains :", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="unit-selector",
                options=[
                    {"label": "kWh", "value": "kwh"},
                    {"label": "€", "value": "euro"},
                    {"label": "%", "value": "percent"},
                ],
                value="kwh",
                placeholder="Sélectionnez une unité",
                multi=False,
                style={"width": "50%", "margin": "0 auto"}
            ),
        ], style={"margin-bottom": "40px", "text-align": "center"}),
    ]),

    # Graphique interactif
    html.Div([
        dcc.Graph(id="interactive-graph", style={"display": "inline-block"})
    ], style={"text-align": "center", "margin-top": "20px"}),
])

# Callback pour mettre à jour le graphique
@app.callback(
    Output("interactive-graph", "figure"),
    [Input("filter-dpe", "value"), Input("unit-selector", "value")]
)
def update_graph(selected_dpe, selected_unit):
    # Calculs pour les gains
    mean_total_conso = df.groupby("Etiquette_DPE")["Conso_5_usages_é_finale"].mean()
    comparison_labels = [label for label in mean_total_conso.index if label != selected_dpe]

    gains = []
    for other_label in comparison_labels:
        gain_kwh = mean_total_conso[other_label] - mean_total_conso[selected_dpe]
        if selected_unit == "kwh":
            gains.append(gain_kwh)
        elif selected_unit == "euro":
            gains.append(gain_kwh * 0.2)
        elif selected_unit == "percent":
            gains.append((gain_kwh / mean_total_conso[selected_dpe]) * 100)

    # Création du graphique
    fig = px.bar(
        x=comparison_labels,
        y=gains,
        labels={"x": "Étiquette DPE", "y": f"Gain ({selected_unit.upper()})"},
        color=comparison_labels,
        color_discrete_map=dpe_colors,
        title=f"Gains énergétiques pour l'étiquette DPE : {selected_dpe}"
    )

    fig.update_traces(texttemplate="%{y:.2f}", textposition="outside")
    fig.update_layout(
        title={"x": 0.5},
        xaxis_title="Étiquette DPE",
        yaxis_title=f"Gains ({selected_unit.upper()})",
        height=600,  # Augmenter la hauteur
        width=1000,  # Augmenter la largeur
        margin=dict(l=40, r=40, t=60, b=40),  # Marges équilibrées
    )

    return fig
