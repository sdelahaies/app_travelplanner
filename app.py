import pandas as pd
from dash import dash, dcc, html, Input, Output, State

import dash_leaflet as dl
import dash_bootstrap_components as dbc
import dash_leaflet.express as dlx

# requires 
#pip install dash-leaflet
#pip install dash-bootstrap-components

import requests

from html_components import index_page, access_granted, travel_planner,get_city_markers,query_opentripmap,create_pois_map,kmeans_plan

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.SKETCHY], suppress_callback_exceptions=True)
app.title = "Travel Planner"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    Output('output1', 'children'),
    [Input('verify', 'n_clicks')],
    [State('user', 'value'),
     State('passw', 'value')])
def update_output(n_clicks, uname, passw):
    # if uname == '' or uname is None or passw == '' or passw is None:
    #    return html.Div(children='', style={'padding-left': '550px', 'padding-top': '10px'})
    if n_clicks:
        li = {'travel': 'planner'}
        if uname not in li:
            return html.Div(children='unknown user', style={'padding-left': '550px', 'padding-top': '40px', 'font-size': '16px'})
        if li[uname] == passw:
            return access_granted
        else:
            return html.Div(children='Invalid Username/Password', style={'padding-left': '550px', 'padding-top': '40px', 'font-size': '16px'})

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    return travel_planner if pathname == '/travel_planner' else index_page


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    return not is_open if n else is_open


# @app.callback(
#     Output('map', 'children'),
#     Output('destination', 'children'),
#     Input('dropdown', 'value'),)
# def update_map(value):
#     if not value:
#         return [dl.TileLayer()],"Destination: "
#     city_markers = [get_city_markers(destination) for destination in value]
#     geojson = dlx.dicts_to_geojson(
#         [{**c, **dict(tooltip=c['name'])} for c in city_markers])
#     return [dl.TileLayer(), dl.GeoJSON(data=geojson, zoomToBounds=True)],"Destination: "+', '.join(value) if value else "Destination:"

@app.callback(
    Output('map', 'children'),
    Input('dropdown', 'value'),)
def update_map(value):
    if not value:
        return [dl.TileLayer()]
    city_markers = [get_city_markers(destination) for destination in value]
    geojson = dlx.dicts_to_geojson(
        [{**c, **dict(tooltip=c['name'])} for c in city_markers])
    return [dl.TileLayer(), dl.GeoJSON(data=geojson, zoomToBounds=True)]

"""
@app.callback(
    #Output('alert', 'children'),
    Output('map_pois','children'),
    Input('planButton', 'n_clicks'),
    State('dropdown', 'value'),)
def lets_plan_alert(click,value):
    if click:
        if not value:
            return "Add a destination first!",[dl.TileLayer()]#html.Iframe(srcDoc=open('map_pois.html', 'r').read())
        city_markers = [get_city_markers(destination) for destination in value]
        for city in city_markers:
            #pois = query_opentripmap(city["lat"],city["lon"])
            fname=city["name"].replace(' ','_')
            pois= pd.read_csv('VALROMEY_SUR_SERAN')
            children = create_pois_map(pois)
            #pois.to_csv(fname)
        return fname.replace(' ','_'),children#,html.Iframe(srcDoc=open('map_pois.html', 'r').read())
"""

@app.callback(
    Output('map_pois','children'),
    Output('map_pois','bounds'),
    Input('planButton', 'n_clicks'),
    State('dropdown', 'value'),)
def lets_plan(click,value):
    if not click:
        return [dl.TileLayer()],[(45,-1),(47,2)]
    if not value:
        return [dl.TileLayer()],[(45,-1),(47,2)]
    city_markers = [get_city_markers(destination) for destination in value]
    for city in city_markers:
        #pois = query_opentripmap(city["lat"],city["lon"])
        fname=city["name"].replace(' ','_')
        pois= pd.read_csv('VALROMEY_SUR_SERAN')
        children,bounds = create_pois_map(pois)
        #pois.to_csv(fname)
    return children,bounds


@app.callback(
    Output('datatable2','data'),
    Input('datatable1','selected_rows'))
def selection(pois_selection):
    pois= pd.read_csv('VALROMEY_SUR_SERAN')
    data = pois.iloc[pois_selection]
    return data.to_dict('records')

@app.callback(
    Output("collapse-setting", "is_open"),
    [Input("showSettingBtn", "n_clicks")],
    [State("collapse-setting", "is_open")],)
def toggle_collapse_setting(n, is_open):
    return not is_open if n else is_open

@app.callback(
    Output("collapse-map", "is_open"),
    [Input("showMapBtn", "n_clicks")],
    [State("collapse-map", "is_open")],)
def toggle_collapse_map(n, is_open):
    if n:
        return not is_open
    else: 
        return is_open
    #return not is_open if n else is_open


@app.callback(
    Output("dayPlanner", "children"),
    Input("dayPlannerButton", "n_clicks"))
def make_journey(n):
    if n:
        pois= pd.read_csv('VALROMEY_SUR_SERAN')
        cards = kmeans_plan(pois)
        return cards
    
    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8050,debug=True)
