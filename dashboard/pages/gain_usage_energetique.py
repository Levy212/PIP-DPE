from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from app import app

# Charger les données spécifiques à Problème 3
file_path = "data/#dpe_pb3.csv"
df_pb3 = pd.read_csv(file_path, sep=",", low_memory=False)

# Colonnes d'intérêt
colonnes_interet = [
    'Etiquette_DPE',
    'Conso_chauffage_é_finale',
    'Conso_ECS_é_finale',
    'Conso_refroidissement_é_finale',
    'Conso_éclairage_é_finale',
    'Conso_auxiliaires_é_finale',
    'Conso_5_usages_é_finale',
    'Surface_habitable_logement'
]

# Prétraitement des données
df_filtre = df_pb3[colonnes_interet].dropna()
df_filtre.iloc[:, 1:7] = df_filtre.iloc[:, 1:7].div(df_filtre['Surface_habitable_logement'], axis=0)
consommation_par_dpe = df_filtre.groupby('Etiquette_DPE').mean().sort_index()

# Mise en page de la page Problème 3
layout = html.Div([
    html.H1(
        "Comparaison des gains énergétiques par étiquette DPE et usage",
        style={"text-align": "center", "margin-bottom": "30px"}
    ),

    # Filtres interactifs
    html.Div([
        html.Div([
            html.Label("Filtrer par Étiquette DPE de départ :"),
            dcc.Dropdown(
                id="filter-dpe-start",
                options=[{"label": etiq, "value": etiq} for etiq in consommation_par_dpe.index],
                value="A",
                placeholder="Sélectionnez une étiquette de départ",
                multi=False,
            ),
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Filtrer par Usage énergétique :"),
            dcc.Dropdown(
                id="filter-usage",
                options=[{"label": usage, "value": usage} for usage in consommation_par_dpe.columns[:-1]],
                value="Conso_chauffage_é_finale",
                placeholder="Sélectionnez un usage énergétique",
                multi=False,
            ),
        ], style={"margin-bottom": "40px"}),
    ], style={"width": "50%", "margin": "0 auto"}),

    # Graphique interactif
    html.Div([
        dcc.Graph(id="combined-bar-graph"),
    ], style={"display": "flex", "justify-content": "center", "align-items": "center", "margin-top": "20px"}),

], style={"padding": "20px"})

# Callback pour générer le graphique combiné
@app.callback(
    Output("combined-bar-graph", "figure"),
    [Input("filter-dpe-start", "value"), Input("filter-usage", "value")]
)
def update_combined_graph(selected_dpe, selected_usage):
    # Calculer les gains en % pour chaque étiquette
    comparison_labels = [label for label in consommation_par_dpe.index if label != selected_dpe]
    gain_percentages = []
    for other_label in comparison_labels:
        base_value = consommation_par_dpe.loc[selected_dpe, selected_usage]
        if base_value != 0:  # Éviter la division par zéro
            gain_pct = ((consommation_par_dpe.loc[other_label, selected_usage] - base_value) / base_value) * 100
            gain_percentages.append({"Classe d'arrivée": other_label, "Gain (%)": gain_pct})

    # Créer un DataFrame pour le graphique
    graph_df = pd.DataFrame(gain_percentages)

    # Création du graphique combiné
    fig = px.bar(
        graph_df,
        x="Classe d'arrivée",
        y="Gain (%)",
        color="Classe d'arrivée",
        color_discrete_map={
            'A': '#00cc00',  # Vert foncé
            'B': '#66ff66',  # Vert clair
            'C': '#ffff00',  # Jaune
            'D': '#ffcc00',  # Orange clair
            'E': '#ff9900',  # Orange foncé
            'F': '#ff3300',  # Rouge clair
            'G': '#cc0000',  # Rouge foncé
        },
        title=f"Gains énergétiques pour {selected_usage} (de {selected_dpe})",
        labels={"Classe d'arrivée": "Classe d'arrivée", "Gain (%)": "Gain en %"}
    )

    fig.update_traces(texttemplate="%{y:.2f}%", textposition="outside")
    fig.update_layout(
        title={"x": 0.5},
        xaxis_title="Classe d'arrivée",
        yaxis_title="Gain en %",
        height=800,  # Augmenter la hauteur
        width=1200,  # Augmenter la largeur
        margin=dict(l=40, r=40, t=60, b=40),  # Marges équilibrées
    )

    return fig
