from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from app import app

# Charger les données
file_path = "data/dpe_dashboard2.csv"
df = pd.read_csv(file_path, sep=",", low_memory=False)

# Échantillonner les données
df_1000 = df.sample(n=100000, random_state=42)  # random_state pour reproductibilité
df_filtered = df_1000[df_1000['Type_bâtiment'].isin(['APPARTEMENT', 'MAISON'])]  # Inclure APPARTEMENTS et MAISONS

# Calcul des quantiles pour filtrer la consommation énergétique
lower_bound = df_filtered['Conso_5_usages_é_finale'].quantile(0.005)
upper_bound = df_filtered['Conso_5_usages_é_finale'].quantile(0.70)

df_filtered = df_filtered[
    (df_filtered['Conso_5_usages_é_finale'] >= lower_bound) &
    (df_filtered['Conso_5_usages_é_finale'] <= upper_bound)
]

# Vérifier que les données de surface habitable ne contiennent pas de valeurs nulles
df_filtered = df_filtered[df_filtered["Surface_habitable_logement"].notna()]

# Convertir les coordonnées projetées en lat/lon (WGS84)
gdf = gpd.GeoDataFrame(
    df_filtered,
    geometry=[Point(xy) for xy in zip(df_filtered['Coordonnée_cartographique_X_(BAN)'],
                                      df_filtered['Coordonnée_cartographique_Y_(BAN)'])],
    crs="EPSG:2154"
)
gdf = gdf.to_crs(epsg=4326)

# Extraire les nouvelles colonnes Latitude et Longitude
df_filtered['Latitude'] = gdf.geometry.y
df_filtered['Longitude'] = gdf.geometry.x
df_filtered = df_filtered.dropna(subset=['Latitude', 'Longitude'])

# Mise en page pour Problème 5
layout = html.Div([
    html.H1("Carte dynamique des consommations", style={"text-align": "center"}),



    # Filtres interactifs
    html.Div([
        html.H4("Choisir la variable pour la couleur des points"),
        dcc.Dropdown(
            id="color-variable",
            options=[
                {"label": col, "value": col}
                for col in df_filtered.select_dtypes(include=["float64", "int64"]).columns
            ],
            placeholder="Choisir une variable...",
            style={"width": "100%"},
        ),

        html.H4("Filtrer par surface habitable (m²)"),
        dcc.RangeSlider(
            id="surface-habitable-slider",
            min=df_filtered["Surface_habitable_logement"].min(),
            max=df_filtered["Surface_habitable_logement"].max(),
            step=1,
            marks={i: str(i) for i in range(
                int(df_filtered["Surface_habitable_logement"].min()),
                int(df_filtered["Surface_habitable_logement"].max()) + 1, 50
            )},
            value=[
                df_filtered["Surface_habitable_logement"].min(),
                df_filtered["Surface_habitable_logement"].max(),
            ],
        ),

        html.H4("Choisir la variable pour la taille des points"),
        dcc.Dropdown(
            id="size-variable",
            options=[
                {"label": col, "value": col}
                for col in df_filtered.select_dtypes(include=["float64", "int64"]).columns
            ],
            placeholder="Choisir une variable...",
            style={"width": "100%"},
        ),

        html.H4("Filtrer par Numéro de Département"),
        dcc.Dropdown(
            id="departement-filter",
            options=[
                {"label": f"{int(dept)}", "value": dept}
                for dept in sorted(df_filtered["N°_département_(BAN)"].dropna().unique().astype(int))
            ],
            multi=False,
            placeholder="Choisir un département",
            style={"width": "100%", "marginBottom": "10px"},
        ),

        html.H4("Choisir les quantiles pour le filtrage"),
        dcc.RangeSlider(
            id="quantile-slider",
            min=0,
            max=100,
            step=1,
            marks={i: f"{i}%" for i in range(0, 101, 10)},
            value=[0.5, 70],
        ),
    ], style={"padding": "20px", "backgroundColor": "#EAEAEA"}),

    # Graphique interactif
    dcc.Graph(id="carte-consommation"),
], style={"backgroundColor": "#F7F7FF", "color": "black", "fontFamily": "Arial, sans-serif"})


# Callback pour Problème 5
@app.callback(
    Output("carte-consommation", "figure"),
    [
        Input("color-variable", "value"),
        Input("quantile-slider", "value"),
        Input("surface-habitable-slider", "value"),
        Input("size-variable", "value"),
        Input("departement-filter", "value")
    ],
)
def update_carte(color_var, quantile_range, surface_range, size_var, selected_departement):
    min_surface, max_surface = surface_range

    # Filtrage par surface habitable
    df_temp = df_filtered[
        (df_filtered["Surface_habitable_logement"] >= min_surface) &
        (df_filtered["Surface_habitable_logement"] <= max_surface)
    ]

    # Filtrer par département
    if selected_departement:
        df_temp = df_temp[df_temp["N°_département_(BAN)"] == selected_departement]

    # Calculer les coordonnées du centre de la carte
    if selected_departement:
        dept_coords = df_temp[["Latitude", "Longitude"]].mean()
        center_lat = dept_coords["Latitude"]
        center_lon = dept_coords["Longitude"]
    else:
        center_lat, center_lon = 46.603354, 1.888334  # France par défaut

    # Appliquer les quantiles
    if color_var:
        lower_percentile = quantile_range[0] / 100
        upper_percentile = quantile_range[1] / 100
        lower_bound = df_temp[color_var].quantile(lower_percentile)
        upper_bound = df_temp[color_var].quantile(upper_percentile)
        df_temp = df_temp[(df_temp[color_var] >= lower_bound) & (df_temp[color_var] <= upper_bound)]

    # Vérifier les données
    if df_temp.empty:
        return px.scatter_mapbox(
            pd.DataFrame(columns=["Latitude", "Longitude"]),
            lat="Latitude",
            lon="Longitude",
            title="Aucune donnée à afficher. Vérifiez vos filtres.",
        )

    # Choisir une taille par défaut si aucune n'est sélectionnée
    if not size_var:
        size_var = "Surface_habitable_logement"

    # Créer la carte
    fig = px.scatter_mapbox(
        df_temp,
        lat="Latitude",
        lon="Longitude",
        color=color_var,
        size=size_var,
        hover_name="N°_département_(BAN)",
        title="Carte dynamique des consommations",
        color_continuous_scale=["green", "yellow", "red"],
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(zoom=5 if not selected_departement else 8, center=dict(lat=center_lat, lon=center_lon)),
        dragmode="zoom",
        height=1000,
        width=1600,
    )

    return fig
