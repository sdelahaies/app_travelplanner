from dash import dash, dcc, html, Input, Output, State, dash_table
import pandas as pd
import requests
import numpy as np

import dash_leaflet as dl
import dash_bootstrap_components as dbc
#import dash_leaflet.express as dlx
import dash_daq as daq
from k_means_constrained import KMeansConstrained



df = pd.read_csv("assets/cities.csv")
pois = pd.read_csv('VALROMEY_SUR_SERAN')

index_page = html.Div([
    html.Div(
        [
            html.H1(children="TRAVEL PLANNER", className="header-title"),
            html.P(children=("plan your trip with user recommendation"),
                   className="header-description")
        ], className="header"
    ),
    html.Div(
        dcc.Input(id="user", type="text", placeholder="Enter Username", className="inputbox1",
                  style={'margin-left': '35%', 'width': '450px', 'height': '45px', 'padding': '10px', 'margin-top': '60px',
                         'font-size': '16px', 'border-width': '3px', 'border-color': '#a0a3a2'
                         }),
    ),
    html.Div(
        dcc.Input(id="passw", type="text", placeholder="Enter Password", className="inputbox2",
                  style={'margin-left': '35%', 'width': '450px', 'height': '45px', 'padding': '10px', 'margin-top': '10px',
                         'font-size': '16px', 'border-width': '3px', 'border-color': '#a0a3a2',
                         }),
    ),
    html.Div(
        dbc.Button('log in', id='verify', n_clicks=0,
                   outline=True, color="primary"),
        style={'margin-left': '45%', 'padding-top': '30px'}),
    html.Div(id='output1')
])

access_granted = dbc.Row(children=[dbc.Col(html.Div([html.P('Access Granted!'),
                                                     dcc.Link('Click here to access', href='/travel_planner')], style={'padding-top': '30px', 'text-align': 'center'}))],
                         justify="center")

links = dbc.Row(
    [
        dbc.Col(dbc.NavLink("About", href="#",
                style={"color": "#ccc1c1"})),
        dbc.Col(dbc.NavLink("log out", href="/", style={"color": "#ccc1c1"}), width={
                "size": 8}, style={'margin-left': '10px'}),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    # justify="right",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src="assets/poi_w.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Travel planner", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"}
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                links,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky='top',
    className="flex-md-row"
)

header = html.Div(
    [
        html.H1(children="TRAVEL PLANNER", className="header-title"),
        html.P(children=("plan your trip with user recommendation"),
               className="header-description")
    ], className="header"
)

dropDownCities = dbc.Row(
    dbc.Col(
        children=dcc.Dropdown(id="dropdown", options=df["Nom"], placeholder="Select a city",
                              multi=True, className="dropDownCities"), width={"size": 10}
    ), justify="center"
)

map_cities = html.Div(dbc.Row(
    dl.Map(
        id="map", children=[dl.TileLayer()],
        zoom=5,
        center=(46, 1.5),
        #className = "mapDestination"
    ), style={
        # 'width': '540px',
        'height': '540px',
        'margin-top': '20px',
        'margin-bottom': '20px',
        'margin-left': '100px',
        'margin-right': '100px',
                        # 'max-width': '800px',
                        # 'max-width': '70%',
                        'display': 'flex'
    }, justify="center"))

setting = html.Div(
    [dbc.Row(children=[
        dbc.Button("set some preferences", id="showSettingBtn",
                   outline=True, color="primary", n_clicks=0),
        dbc.Collapse(
            dbc.Card([
                dbc.CardBody(children=[
                    dbc.Row(children=[
                        dbc.Col(children=[
                            dbc.Label("type of activity"),
                            dbc.Checklist(
                                options=[
                                    {"label": "Food", "value": 1},
                                    {"label": "Culture ", "value": 2},
                                    {"label": "Nature", "value": 2}, ], value=[1], id="checklist-input",),
                                ]),
                        dbc.Col(children=[
                            html.Div(children="number of activities"),
                                daq.NumericInput(id='n_pois', min=1, max=500,value=500),
                                ])
                        ])

                ])
            ],
                style={'margin-top': '10px'}),
            id="collapse-setting",
            is_open=False,
        )], justify="center")
     ], style={'margin-left': '100px', 'margin-right': '100px', 'margin-top': '10px', 'margin-bottom': '10px'}
)

planButton = html.Div(dbc.Row(
    children=dbc.Button(id="planButton", children="Let's find the points of interest!",
                        outline=True, color="primary"), justify="center"), style={'margin-left': '100px',
                                                                                    'margin-right': '100px', 'margin-top': '10px', 'margin-bottom': '10px'}
                      )

""" cardPrepare #removed
cardPrepare = dbc.Row(dbc.Card([
    dbc.CardBody([
        html.H4(id="title_card", children="Prepare your travel",
                className="card-title", style={'textAlign': 'center'}),
        html.P(id='destination', children="Destination:",
               className="card-text",
               style={'margin-left': '20px', 'textAlign': 'center'}
               ),
        html.Div([
            dbc.Label("Choose a bunch"),
            dbc.Checklist(
                options=[
                    {"label": "Option 1", "value": 1},
                    {"label": "Option 2", "value": 2},
                ],
                value=[1],
                id="checklist-input",), ],
            style={'textAlign': 'left'}),
        dbc.Row([
            html.P("number of days"),
            dbc.Input(type="number", min=1, max=50, step=1),
        ], id="styled-numeric-input", style={'width': '100px'}),

        dbc.Button(id='btnPlan', children="Let's plan!",
                   outline=True, color="primary"),
        html.Div([
            dbc.Tabs([
                dbc.Tab(label="tab 1", active_label_style={
                        "color": "#245bae"}),
                dbc.Tab(label="tab 2", active_label_style={
                        "color": "#245bae"}),
            ]
            )]
        ),
        html.Div(
            [html.Div("ALORS c'est quoi c bordel!"),
             dbc.Pagination(max_value=5, first_last=True),
             ]
        ),
        html.Div(
            [html.Div(id="test", children="ALORS c'est quoi c bordel!")]
        ),
    ]),

], style={
    # 'width': '540px',
    'height': '540px',
    'margin-top': '20px',
    'margin-left': '20px',
    'margin-right': '20px',
    'display': 'flex',
    'max-width': '70%'
}, ), justify="center")
"""

map_pois = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div(
                    html.Iframe(
                        srcDoc=open('map_pois.html', 'r').read(),
                        style={
                            'width': '500px',
                            'height': '500px',
                            'margin-top': '2px',
                            'margin-left': '2px',
                            'margin-right': '2px',

                        },
                    )
                )
            ]
        )
    ], style={
        'width': '540px',
        'height': '540px',
        'margin-top': '10px',
        'margin-left': '10px',
        'margin-right': '10px',
        'display': 'flex'
    },
)

icon =dict(iconUrl="assets/icon2.png", iconAnchor=[13, 42])
markers=[dl.Marker(position=[46.5, 1.5],icon=icon)]
#markers=[]
map_pois_leaflet = html.Div(dbc.Row(
    dl.Map(id="map_pois",
        children=[dl.TileLayer(),dl.LayerGroup(markers)],
        #bounds=[(45,-1),(47,2)],
        #zoom=5,
        #center=(46, 1.5),
    ), style={'height': '540px','margin-top': '10px','margin-bottom': '10px'#,'margin-left': '100px','margin-right': '100px','display': 'flex'
              }, justify="center"
    )
    )

showmap = html.Div(children =
    [dbc.Row(children=[
        dbc.Button(children = "Show/Hide map",id="showMapBtn",className="mb-3",color="primary",outline=True,n_clicks=0,),
        dbc.Collapse(
            map_pois_leaflet,
            #html.Div(id = "mapPois"),
            id="collapse-map",
            is_open=True,
        )])
    ], style={'margin-left': '100px', 'margin-right': '100px', 'margin-top': '10px', 'margin-bottom': '10px'}
)

columns = []
for col in df.columns:
    col_options = {"name": col, "id": col}
    if col == "MyNumericColumn":
        col_options["type"] = "numeric"
    columns.append(col_options)

my_table = dash_table.DataTable(id="table", columns=columns)

table = html.Div(dbc.Row(
    html.Div(id="table", children=[
                dash_table.DataTable(
                    id='datatable1',
                    columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in [
                        "properties.name", "properties.rate"]],
                    #columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in pois.columns],
                    data=pois.to_dict('records'),
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    # column_selectable="single",
                    row_selectable="multi",
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=20,
                ),
        html.Div(id='datatable-interactivity-container')
    ]), justify="center"
), style={
    # 'width': '540px',
    # 'height': '540px',
    'margin-top': 'auto',
    'margin-left': 'auto',
    'margin-right': 'auto',
    'display': 'flex',
    # 'max-width': '70%'
},
)

table_selection = dbc.Row(
    html.Div(id="table2", children=[
                dash_table.DataTable(
                    id='datatable2',
                    columns=[{"name": i, "id": i, "deletable": True,
                              "selectable": True} for i in ["properties.name"]],
                    #columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in pois.columns],
                )], style={
        # 'width': '540px',
        # 'height': '540px',
        'margin-top': '20px',
        'margin-left': '20px',
        'margin-right': '20px',
        'display': 'flex'}), justify="center")

alert = html.Div(
    dbc.Alert(id="alert", children='', color="danger"),
    style={'margin-top': '20px',
           'margin-left': '100px',
           'margin-right': '100px',
           'margin-bottom': '20px'}
)

dayPlannerButton = html.Div(dbc.Row(
    children=dbc.Button(id="dayPlannerButton", children="Let's plan our journey!",
                        outline=True, color="primary"), justify="center"), style={'margin-left': '100px',
                                                                                    'margin-right': '100px', 'margin-top': '10px', 'margin-bottom': '10px'}
                      )

day_planner = html.Div(id="dayPlanner", style={'margin-left': '100px', 'margin-right': '100px', 'margin-top': '10px', 'margin-bottom': '10px'})


def get_city_markers(destination):
    df_dest = df[df["Nom"] == destination]
    return dict(name=str(df_dest["Nom"].to_numpy()[0]),
                lat=float(df_dest["latitude"].to_numpy()[0]),
                lon=float(df_dest["longitude"].to_numpy()[0]))

about = html.Div([
    navbar,
    header,
]
)

def query_opentripmap(lat, lon):
    itineraire_vacance_key = 'put_your_own_api_key'
    headers = {'accept': 'application/geojson'}
    params = {
        'radius': '50000',
        'lon': lon,
        'lat': lat,
        'rate': '1',
        'format': 'geojson',
        'apikey': itineraire_vacance_key,
    }
    response = requests.get(
        'https://api.opentripmap.com/0.1/en/places/radius', params=params, headers=headers)
    return pd.json_normalize(response.json(), record_path=['features'])

"""
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', \
    'lightred',  'darkblue', 'darkgreen', 'cadetblue', \
    'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', \
    'black', 'lightgray', 'red', 'blue', 'green', 'purple', \
    'orange', 'darkred', 'lightred', 'beige', 'darkblue', \
    'darkgreen', 'cadetblue','beige', 'darkpurple','pink', 'lightblue', \
    'lightgreen', 'gray', 'black', 'lightgray' ]
"""
    
def create_pois_map(pois):
    # folium hack, create a map save it as html to load as a iframe
    # fg_mark = folium.FeatureGroup(name="Markers")
    # for i,poi in pois.iterrows():
    #     coord = poi["geometry.coordinates"]
    #     lon = float(coord.split(',')[0][1:])
    #     lat = float(coord.split(',')[1][1:-1])
    #     label = poi["properties.name"]
    #     kinds = poi["properties.kinds"]
    #     rate = poi["properties.rate"]
    #     wiki = poi["properties.wikidata"]
    #     folium.Marker(
    #         location = [lat,lon],
    #         popup = f"{label}\n rate: {rate}\n kinds: {kinds}\n wiki: {wiki}",
    #         icon = folium.Icon(color=random.choice(colors),icon="hamburger", prefix='fa')
    #         ).add_to(fg_mark)
    # m = folium.Map()
    # fg_mark.add_to(m)
    # m.fit_bounds(fg_mark.get_bounds())
    # m.save("map_pois.html")
    icon =dict(iconUrl="assets/icon2.png", iconAnchor=[13, 42])
    markers=[]
    lats=[]
    lons=[]
    for i,poi in pois.iterrows():
        coord = poi["geometry.coordinates"]
        lon = float(coord.split(',')[0][1:])
        lat = float(coord.split(',')[1][1:-1])
        lons.append(lon)
        lats.append(lat)
        markers.append(dl.Marker(position=[lat,lon],icon=icon,
                                 children=[dl.Tooltip("test"),dl.Popup("test")],))
    ne = np.max([lats,lons],axis=1)    
    sw = np.min([lats,lons],axis=1)    
    return [dl.TileLayer(),dl.LayerGroup(markers)],[sw,ne]
    #return 

def day_map(df_day):
    icon =dict(iconUrl="assets/icon2.png", iconAnchor=[13, 42])
    markers=[]
    for i,poi in df_day.iterrows():
       markers.append(dl.Marker(position=[poi.lat,poi.lon],icon=icon,children=[dl.Tooltip("test"),dl.Popup("test")],))
    ne = np.max([df_day.lat,df_day.lon],axis=1)    
    sw = np.min([df_day.lat,df_day.lon],axis=1)    
    return dl.Map(children=[dl.TileLayer(),dl.LayerGroup(markers)],bounds=[sw,ne])


def kmeans_plan(pois,npois=20,ndays=5,nmin=3,nmax=6):
    pois = pois.drop_duplicates(subset=['properties.wikidata'])
    df = pois.sort_values(by=["properties.rate","properties.dist"],ascending = [False, True])
    df =  df.iloc[:npois]
    df2 = df[["properties.name","properties.wikidata"]]
    df2["lat"] = df["geometry.coordinates"].apply(lambda x: float(x.split(',')[1][1:-1]))
    df2["lon"] = df["geometry.coordinates"].apply(lambda x: float(x.split(',')[0][1:])) 

    X = np.array(df2[["lat","lon"]])
    clf = KMeansConstrained(n_clusters=ndays,size_min=nmin,size_max=nmax,random_state=42)
    clf.fit_predict(X)
    labels = clf.labels_
    df2['cluster'] = labels

    cards=[]
    for i in range(ndays):
        df_day = df2[df2.cluster == i]
        map_day  = day_map(df_day)        
        day_card = [
            html.H4(f"Day {i+1}", className="card-title"),
            html.P("Here is your plan for today",className="card-text",),
            html.Div(children=map_day,style={"height":"300px"})                        
            ]
        day_card.extend(
            html.P(
                children=f"{k}. {poi['properties.name']}",
                className="card-text",
            )
            for k, (j, poi) in enumerate(df_day.iterrows(), start=1)
        )
        
        card = dbc.Card([dbc.CardBody(day_card),],)
        cards.append(card)
    return cards

    
travel_planner = html.Div([
    navbar,
    header,
    dropDownCities,
    map_cities,
    setting,
    planButton,
    #alert,
    #map_pois_leaflet,
    showmap,
    dayPlannerButton,
    day_planner,
   # day_map
    # cardPrepare,
    #table,
    #table_selection,
    #map_pois,
])