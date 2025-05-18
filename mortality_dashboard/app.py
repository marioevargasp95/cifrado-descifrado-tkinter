from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sys
import os

# Asegura que src esté en el path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

from layout import (
    fig_mapa, fig_linea, fig_barras,
    fig_pie, fig_tabla, fig_hist, fig_apiladas
)

logo_path = "/assets/Logo_MinSalud_Colombia_2022.svg.png"
background_path = "/assets/fondo_tablero.avif"

# Layout principal
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        # 📌 Panel izquierdo con logo y botones
        dbc.Col([
            html.Div([
                html.Img(src=logo_path, style={"width": "100%", "padding": "10px"}),
                html.H2("Tablero de Mortalidad", className="text-center", style={"marginTop": "20px", "fontSize": "50px", "fontWeight": "bold"}),
                html.Hr(),
                html.P("Visualización de datos de mortalidad en Colombia.", className="text-muted text-center"),

                html.Hr(),
                html.Div([
                    dcc.RadioItems(
                        id="seccion",
                        options=[
                            {"label": "📊 Indicadores generales", "value": "resumen"},
                            {"label": "📋 Análisis detallado", "value": "detalle"},
                        ],
                        value="resumen",
                        labelStyle={"display": "block", "marginBottom": "10px", "fontWeight": "bold"},
                        inputStyle={"marginRight": "10px"},
                        style={"padding": "10px"}
                    )
                ])
            ], style={"backgroundColor": "#f8f9fa", "height": "100vh", "padding": "20px"})
        ], width=2),

        # 📊 Panel derecho para contenido gráfico
        dbc.Col([
            html.Div(style={
                "backgroundImage": f"url('{background_path}')",
                "backgroundSize": "cover",
                "backgroundRepeat": "no-repeat",
                "backgroundAttachment": "fixed",
                "padding": "20px"
            }, children=[
                html.Div(id="contenido")
            ])
        ], width=10)
    ])
])

# Callback para actualizar los gráficos según la sección
@app.callback(
    Output("contenido", "children"),
    Input("seccion", "value")
)
def actualizar_vista(seccion):
    if seccion == "resumen":
        return [
            html.H2(" Distribución de muertes por departamento", className="dash-graph-title"),
            dcc.Graph(figure=fig_mapa, className="dash-graph-container"),

            html.H2("📈 Total de muertes por mes en Colombia", className="dash-graph-title"),
            dcc.Graph(figure=fig_linea, className="dash-graph-container"),

            html.H2("5 municipios con más homicidios (X95)", className="dash-graph-title"),
            dcc.Graph(figure=fig_barras, className="dash-graph-container")
        ]
    elif seccion == "detalle":
        return [
            html.H2("10 municipios con menor mortalidad", className="dash-graph-title"),
            dcc.Graph(figure=fig_pie, className="dash-graph-container"),

            html.H2("📋 Principales causas de muerte", className="dash-graph-title"),
            dcc.Graph(figure=fig_tabla, className="dash-graph-container"),

            html.H2(" Distribución por rangos de edad", className="dash-graph-title"),
            dcc.Graph(figure=fig_hist, className="dash-graph-container"),

            html.H2("👥 Muertes por sexo en cada departamento", className="dash-graph-title"),
            dcc.Graph(figure=fig_apiladas, className="dash-graph-container")
        ]

if __name__ == "__main__":
    app.run(debug=True)