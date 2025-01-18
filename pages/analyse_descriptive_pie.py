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

# Mise en page pour le diagramme circulaire
layout = html.Div([
    html.H1(
        "Diagramme circulaire des étiquettes DPE en fonction du type de bâtiment et du département",
        style={"text-align": "center", "margin-bottom": "30px"}
    ),

    # Filtres interactifs centrés
    html.Div([
        html.Div([
            html.Label("Filtrer par Type de Bâtiment :", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="filter-type-batiment-pie",
                options=[{"label": val, "value": val} for val in df["Type_bâtiment"].dropna().unique()],
                value=[],
                placeholder="Sélectionnez un ou plusieurs Types de Bâtiment",
                multi=True,
            ),
        ], style={"width": "40%", "margin": "10px auto"}),

        html.Div([
            html.Label("Filtrer par Département :", style={"font-weight": "bold"}),
            dcc.Dropdown(
                id="filter-departement-pie",
                options=[{"label": val, "value": val} for val in df["N°_département_(BAN)"].dropna().unique()],
                value=[],
                placeholder="Sélectionnez un ou plusieurs Départements",
                multi=True,
            ),
        ], style={"width": "40%", "margin": "10px auto"}),
    ], style={"text-align": "center"}),

    # Diagramme circulaire centré
    html.Div(
        dcc.Graph(id="pie-chart"),
        style={"display": "flex", "justify-content": "center", "align-items": "center", "margin-top": "30px"}
    )
])


# Callback pour mettre à jour le diagramme circulaire
@app.callback(
    Output("pie-chart", "figure"),
    [Input("filter-type-batiment-pie", "value"),
     Input("filter-departement-pie", "value")]
)
def update_pie_chart(filter_batiments, filter_departements):
    filtered_df = df.copy()
    if filter_batiments:
        filtered_df = filtered_df[filtered_df["Type_bâtiment"].isin(filter_batiments)]
    if filter_departements:
        filtered_df = filtered_df[filtered_df["N°_département_(BAN)"].isin(filter_departements)]

    # Vérification des données filtrées
    if filtered_df.empty:
        return px.pie(
            names=["Aucune donnée"],
            values=[1],
            title="Aucune donnée disponible",
            color_discrete_sequence=["#d3d3d3"]  # Couleur grise
        )

    # Compter les occurrences des étiquettes DPE
    dpe_counts = filtered_df["Etiquette_DPE"].value_counts(normalize=True) * 100  # Convertir en pourcentage
    dpe_counts = dpe_counts.reindex(["A", "B", "C", "D", "E", "F", "G"], fill_value=0)  # Garder l'ordre A-G

    # Créer le diagramme circulaire
    fig = px.pie(
        names=dpe_counts.index,
        values=dpe_counts.values,
        title="Répartition des bâtiments par étiquette DPE",
        color=dpe_counts.index,
        color_discrete_map=etiquette_colors,
        labels={"values": "Pourcentage", "names": "Étiquette DPE"}
    )
    fig.update_traces(textinfo="percent+label", textfont_size=14)
    fig.update_layout(
        title_font_size=24,
        title_x=0.5,  # Centrer le titre
        width=1000,  # Largeur du graphique
        height=700,  # Hauteur du graphique
        margin=dict(t=50, b=50, l=50, r=50),
        legend=dict(
            title="Étiquettes DPE",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.1,
            yanchor="top"
        )
    )

    return fig
