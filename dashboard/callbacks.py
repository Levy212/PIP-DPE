from dash.dependencies import Input, Output
from app import app
from pages import (
    accueil,
    presentation,
    analyse_descriptive_bar,
    analyse_descriptive_pie,
    analyse_descriptive_surface,
    analyse_descriptive_cost,
    gains_energetiques,
    gain_usage_energetique,
    Carte_dynamique_des_consommations,
)

# Callback pour gérer les routes
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return accueil.layout
    elif pathname == "/presentation-projet":
        return presentation.layout
    elif pathname == "/analyse-descriptive-bar":
        return analyse_descriptive_bar.layout
    elif pathname == "/analyse-descriptive-pie":
        return analyse_descriptive_pie.layout
    elif pathname == "/analyse-descriptive-surface":
        return analyse_descriptive_surface.layout
    elif pathname == "/analyse-descriptive-cost":
        return analyse_descriptive_cost.layout
    elif pathname == "/gains-energetiques":
        return gains_energetiques.layout
    elif pathname == "/gain-usage-energetique":
        return gain_usage_energetique.layout
    elif pathname == "/carte-dynamique-consommations":
        return Carte_dynamique_des_consommations.layout
    else:
        return html.H1("404: Page non trouvée", style={"textAlign": "center"})
