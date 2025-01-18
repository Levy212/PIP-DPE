from dash import html, dcc
from app import app

# Récupérer les données globales
df = app.server.df
df_appartements = app.server.df_appartements

# Layout pour la page d'accueil
layout = html.Div([
    html.H1(
        "Présentation du Projet",
        style={"text-align": "center", "margin-bottom": "30px", "font-size": "2.5rem"}
    ),

    # Section présentation
    html.Div([
        html.H2(
            "Contexte",
            style={"text-align": "center", "margin-top": "20px", "text-decoration": "underline", "font-size": "2rem"}
        ),
        html.P(
            """
            Face aux défis climatiques et à la hausse des coûts énergétiques, la performance énergétique des bâtiments joue un rôle central 
            dans la transition énergétique. En France, le Diagnostic de Performance Énergétique (DPE), classant les logements de A (économe) 
            à G (énergivore), est un outil clé pour identifier les logements à rénover en priorité et orienter les politiques publiques. 
            Cependant, il existe souvent un écart entre les consommations énergétiques estimées par les DPE et les consommations réelles des logements.
            """,
            style={"text-align": "justify", "margin": "10px 50px", "font-size": "1.2rem"}
        ),

        html.H2(
            "Objectifs",
            style={"text-align": "center", "margin-top": "20px", "text-decoration": "underline", "font-size": "2rem"}
        ),
        html.P(
            """
            Ce projet a pour but d’évaluer les impacts des classes énergétiques DPE sur les consommations électriques, de comparer les estimations 
            des DPE avec les mesures réelles et d’analyser les facteurs de variabilité liés aux caractéristiques des logements et aux comportements individuels.
            """,
            style={"text-align": "justify", "margin": "10px 50px", "font-size": "1.2rem"}
        ),

        html.H2(
            "Description des données",
            style={"text-align": "center", "margin-top": "20px", "text-decoration": "underline", "font-size": "2rem"}
        ),
        html.P(
            """
            Les données utilisées dans ce tableau de bord proviennent des diagnostics de performance énergétique (DPE) publiés par l’ADEME. 
            Ces données couvrent les logements existants et neufs depuis juillet 2021. Les informations clés comprennent :
            """,
            style={"text-align": "justify", "margin": "10px 50px", "font-size": "1.2rem"}
        ),
        html.Ul([
            html.Li("Étiquette DPE : Classe énergétique du logement (A à G).", style={"font-size": "1.2rem"}),
            html.Li("Consommation énergétique prédite (kWh/m²) : Estimation calculée par la méthode 3CL.", style={"font-size": "1.2rem"}),
            html.Li("Consommation réelle électrique (kWh/m²) : Basée sur les cinq usages énergétiques principaux.", style={"font-size": "1.2rem"}),
            html.Li("Coût total énergétique (en euros) : Estimation des dépenses énergétiques annuelles.", style={"font-size": "1.2rem"}),
            html.Li("Surface habitable : Taille du logement (en m²).", style={"font-size": "1.2rem"}),
            html.Li("Type de logement : Maison, appartement, etc.", style={"font-size": "1.2rem"}),
            html.Li("Département : Localisation géographique du logement.", style={"font-size": "1.2rem"}),
            html.Li("Année de construction : Ancienneté du bâtiment.", style={"font-size": "1.2rem"}),
        ], style={"margin": "10px 70px"}),

        html.H2(
            "Méthodologie",
            style={"text-align": "center", "margin-top": "20px", "text-decoration": "underline", "font-size": "2rem"}
        ),
        html.P(
            """
            Les données initiales, contenant des millions de lignes et 286 colonnes, ont été filtrées pour garantir leur qualité. 
            Un focus a été réalisé sur plusieurs départements, notamment Paris (75), Haute-Garonne (31), Bouches-du-Rhône (13), 
            Morbihan (56), et Puy-de-Dôme (63). Une analyse des corrélations et un nettoyage des colonnes ont permis de conserver 
            uniquement les variables pertinentes pour l’étude.
            """,
            style={"text-align": "justify", "margin": "10px 50px", "font-size": "1.2rem"}
        ),

        html.H2(
            "Portée et limites",
            style={"text-align": "center", "margin-top": "20px", "text-decoration": "underline", "font-size": "2rem"}
        ),
        html.P(
            """
            Les données couvrent environ 20 % des logements français, car le DPE est obligatoire uniquement lors de ventes, 
            mises en location ou pour les logements neufs. Ce tableau de bord se concentre principalement sur les consommations 
            électriques, permettant des comparaisons géographiques et énergétiques selon divers critères.
            """,
            style={"text-align": "justify", "margin": "10px 50px", "font-size": "1.2rem"}
        ),
    ]),
], style={"padding": "20px"})
