from dash import html
from app import app

# Layout pour la page d'accueil
layout = html.Div([
    # Titre principal
    html.H1(
        "Projet Inter Promo : Les Diagnostics de Performance Energétique",
        style={
            "text-align": "center",
            "font-weight": "bold",
            "margin-top": "30px",
            "font-size": "32px"
        }
    ),

    # Section des noms
    html.Div([
        html.H2("Réalisé par :", style={"text-align": "center", "margin-top": "20px"}),
        html.Div([
            html.P("Master 2 :", style={"font-size": "22px", "font-weight": "bold", "text-align": "center"}),
            html.P("ALBOUY Raphaël, FOURATI Ahmed, JEANFAIVRE Yohann, CANARD Estelle",
                   style={"text-align": "center", "font-size": "20px"}),
            html.P("Master 1 :",
                   style={"font-size": "22px", "font-weight": "bold", "text-align": "center", "margin-top": "10px"}),
            html.P("OKU YELIME Simonss, TALHA Ali, KODJOVI Paulin, DUPORTE Alexandre",
                   style={"text-align": "center", "font-size": "20px"}),
        ]),
    ], style={"margin-bottom": "30px"}),

    # Image ajoutée
    html.Div([
        html.Img(
            src=app.get_asset_url("Ditribition des technologies.png"),
            style={"width": "50%", "margin": "0 auto", "display": "block", "margin-top": "20px"}
        )
    ], style={"text-align": "center", "margin-bottom": "40px"}),

    # Section Sommaire
    html.Div([
        html.H2("Sommaire", style={
            "text-align": "center",
            "margin-bottom": "20px",
            "text-decoration": "underline"
        }),
        html.Ul([
            html.Li(html.A("Présentation du projet", href="/presentation-projet")),
            html.Li(html.A("Analyse descriptive", href="#"), style={"font-weight": "bold"}),
            html.Ul([
                html.Li(html.A("Diagramme en bâtons des étiquettes DPE", href="/analyse-descriptive-bar")),
                html.Li(html.A("Diagramme circulaire des étiquettes DPE", href="/analyse-descriptive-pie")),
                html.Li(html.A("Surface moyenne par classe DPE", href="/analyse-descriptive-surface")),
                html.Li(html.A("Coût annuel moyen par étiquette DPE", href="/analyse-descriptive-cost")),
            ]),
            html.Li(html.A("Gains énergétiques", href="/gains-energetiques")),
            html.Li(html.A("Gain Usage Energétique", href="/gain-usage-energetique")),
            html.Li(html.A("Carte dynamique des consommations", href="/carte-dynamique-consommations")),
        ], style={"margin-left": "0", "text-align": "center", "font-size": "18px", "display": "inline-block"})
    ], style={"text-align": "center", "margin-top": "30px"}),
], style={"padding": "20px"})
