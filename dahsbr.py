import dash
from dash.dependencies import Input, Output,State
import dash_core_components as dcc
import dash_html_components as html
import requests
import json
import datetime, pytz
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px




#ip_address = request.headers['X-Real-IP']
ip_address='181.26.36.96'

GEO_IP_API_URL  = 'http://ip-api.com/json/'


IP_TO_SEARCH    = ip_address


req             = requests.get(GEO_IP_API_URL+IP_TO_SEARCH)

json_response   = json.loads(req.text)


lat=(json_response['lat'])
lon=(json_response['lon'])

r=requests.get('https://api.openweathermap.org/data/2.5/onecall?lat='+str(lat)+'&lon='+str(lon)+'&lang=pt_br'+'&appid=029e4d13d05bab8a91e8fbe876e20239&units=metric')

weather_data = r.json()


tz = pytz.timezone('America/Sao_Paulo')

dates=[]
temp=[]
rain=[]
wind_speed=[]
humidity=[]

for i in weather_data['hourly']:
    local_time = datetime.datetime.fromtimestamp(i['dt'],tz=tz)
    str_time = local_time.strftime( '%H:%M %m-%d' )
    dates.append(str_time)
    temp.append(i['temp'])
    try:
        rain.append(i['rain'])
    except:
        rain.append(0)
    wind_speed.append(i['wind_speed'])
    humidity.append(i['humidity'])


dates_d=[]
max_d=[]
min_d=[]
temp_d=[]
rain_d=[]
wind_speed_d=[]
humidity_d=[]
for i in weather_data['daily']:
    local_time = datetime.datetime.fromtimestamp(i['dt'],tz=tz)
    str_time = local_time.strftime( '%H:%M %m-%d' )
    dates_d.append(str_time)
    max_d.append(i['temp']['max'])
    min_d.append(i['temp']['min'])
    temp_d.append(i['temp']['day'])
    try:
        rain_d.append(i['rain'])
    except:
        rain_d.append(0)
    wind_speed.append(i['wind_speed'])
    humidity.append(i['humidity'])

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX,FONT_AWESOME])

temperatura =    ['°C','°C Max', '°C Min','Chuva(%)','Umidade(%)','Vento(m/s)'] 

horas=['3h', '6h', '9h','12h','24h','48h']
     

   

app.layout = html.Div([

    html.Div(className='mb-4'),

    html.Div(
    dbc.Row(dbc.Col(
    dcc.Dropdown(
        id='countries-dropdown', 
    
        options=[{'label': k, 'value': k} for k in horas],
        value='3h',
        clearable=False,style={    
                    'color': '#565555',
                    'borderStyle':'solid',
                    # 'width': '50%',                  
                    'font-size': '15px',
                    'textAlign': 'center'}),
    width=6, md={'size':4,'offset':4}),className='mb-4',),),
        
    

    html.Div(
    dbc.Row(dbc.Col(
    dcc.Dropdown(
        id='cities-dropdown',clearable=False, style={    
                    'color': '#565555',
                    'borderStyle':'solid',
                    # 'width': '50%',                  
                    'font-size': '15px',
                    'textAlign': 'center'}  ), 
    width=6,md={'size':4,'offset':4}),className='mb-4',),),

    

    dbc.Row(dbc.Col(html.Div(id='display-selected-values', className="text-center",style={    
                    'color': '#565555',  
                    'font-size': '30px',
                    'font': 'sans-serif',
                    'font-weight': 'bolder',
                    } ),),),


  
   dbc.Button(
            
            id="collapse-button",
            className="fas fa-chart-line",
            color="btn btn-outline-secondary",
            n_clicks=0,
            style={
            'margin': '0 auto',
            'display': 'block',
            'textAlign': 'center'},
            
        ),
        dbc.Collapse(
            dcc.Graph(id='graph-with-slider'),
            id="collapse",
            is_open=False,
        ),
 
]
)



@app.callback(
    dash.dependencies.Output('cities-dropdown', 'options'),
    [dash.dependencies.Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in temperatura]

@app.callback(
    dash.dependencies.Output('cities-dropdown', 'value'),
    [dash.dependencies.Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    [dash.dependencies.Input('countries-dropdown', 'value'),
     dash.dependencies.Input('cities-dropdown', 'value')])
def set_display_children(selected_country, selected_city):
    if selected_country == '3h' and selected_city=='°C' :
        final=str(temp[2])+'°C'
    elif selected_country=='6h' and selected_city=='°C':
        final=str(temp[5])+'°C'
    elif selected_country=='9h' and selected_city=='°C':
        final=str(temp[8])+'°C'
    elif selected_country=='12h' and selected_city=='°C':
        final=str(temp[11])+'°C'
    elif selected_country=='24h' and selected_city=='°C':
        final=str(temp_d[0])+'°C'
    elif selected_country=='48h' and selected_city=='°C':
        final=str(temp_d[1])+'°C'
    elif selected_country=='3h' and selected_city=='Chuva(%)':
        final=str(rain[2])+'%'
    elif selected_country=='6h' and selected_city=='Chuva(%)':
        final=str(rain[5])+'%'
    elif selected_country=='9h' and selected_city=='Chuva(%)':
        final=str(rain[8])+'%'
    elif selected_country=='12h' and selected_city=='Chuva(%)':
        final=str(rain[11])+'%'
    elif selected_country=='24h' and selected_city=='Chuva(%)':
        final=str(rain_d[0])+'%'
    elif selected_country=='48h' and selected_city=='Chuva(%)':
        final=str(rain_d[1])+'%'
    elif selected_country=='3h' and selected_city=='Umidade(%)':
        final=str(humidity[2])+'%'
    elif selected_country=='6h' and selected_city=='Umidade(%)':
        final=str(humidity[5])+'%'
    elif selected_country=='9h' and selected_city=='Umidade(%)':
        final=str(humidity[8])+'%'
    elif selected_country=='12h' and selected_city=='Umidade(%)':
        final=str(humidity[11])+'%'
    elif selected_country=='24h' and selected_city=='Umidade(%)':
        final=str(humidity_d[0])+'%'
    elif selected_country=='48h' and selected_city=='Umidade(%)':
        final=str(humidity_d[1])+'%'
    elif selected_country=='3h' and selected_city=='Vento(m/s)':
        final=str(wind_speed[2])+'m/s'
    elif selected_country=='6h' and selected_city=='Vento(m/s)':
        final=str(wind_speed[5])+'m/s'
    elif selected_country=='9h' and selected_city=='Vento(m/s)':
        final=str(wind_speed[8])+'m/s'
    elif selected_country=='12h' and selected_city=='Vento(m/s)':
        final=str(wind_speed[11])+'m/s'
    elif selected_country=='24h' and selected_city=='Vento(m/s)':
        final=str(wind_speed_d[0])+'m/s'
    elif selected_country=='48h' and selected_city=='Vento(m/s)':
        final=str(wind_speed_d[1])+'m/s'
    elif selected_country=='3h' and selected_city=='°C Max':
        final='no data'
    elif selected_country=='6h' and selected_city=='°C Max':
        final='no data'
    elif selected_country=='9h' and selected_city=='°C Max':
        final='no data'
    elif selected_country=='12h' and selected_city=='°C Max':
        final='no data'
    elif selected_country=='24h' and selected_city=='°C Max':
        final=str(max_d[0])+'%'
    elif selected_country=='48h' and selected_city=='°C Max':
        final=str(max_d[1])+'%'
    elif selected_country=='3h' and selected_city=='°C Min':
        final='no data'
    elif selected_country=='6h' and selected_city=='°C Min':
        final='no data'
    elif selected_country=='9h' and selected_city=='°C Min':
        final='no data'
    elif selected_country=='12h' and selected_city=='°C Min':
        final='no data'
    elif selected_country=='24h' and selected_city=='°C Min':
        final=str(min_d[0])+'%'
    elif selected_country=='48h' and selected_city=='°C Min':
        final=str(min_d[1])+'%'

    
    
    

    return final



@app.callback(
Output('graph-with-slider',component_property="figure"),
[dash.dependencies.Input('countries-dropdown', 'value'),
    dash.dependencies.Input('cities-dropdown', 'value')])

def tabla(selected_country,selected_city):
    if selected_country=='24h' and selected_city=='°C':
        grafico={'Dia':dates_d,'Temperatura':temp_d}

    elif selected_country=='48h' and selected_city=='°C':
        grafico={'Dia':dates_d,'Temperatura':temp_d}
        
    elif selected_country=='24h' and selected_city=='Chuva(%)':
        grafico={'Dia':dates_d,'Temperatura':rain_d}
    elif selected_country=='48h' and selected_city=='Chuva(%)':
        grafico={'Dia':dates_d,'Temperatura':rain_d}
    elif selected_country=='24h' and selected_city=='Vento(m/s)':
        grafico={'Dia':dates_d,'Temperatura':wind_speed_d}
    elif selected_country=='48h' and selected_city=='Vento(m/s)':
        grafico={'Dia':dates_d,'Temperatura':wind_speed_d}

    elif selected_country=='24h' and selected_city=='°C Max':
        grafico={'Dia':dates_d,'Temperatura':max_d}
    elif selected_country=='48h' and selected_city=='°C Max':
        grafico={'Dia':dates_d,'Temperatura':max_d}

    elif selected_country=='24h' and selected_city=='°C Min':
        grafico={'Dia':dates_d,'Temperatura':min_d}
    elif selected_country=='48h' and selected_city=='°C Min':
        grafico={'Dia':dates_d,'Temperatura':min_d}
    elif selected_country=='24h' and selected_city=='Umidade(%)':
        grafico={'Dia':dates_d,'Temperatura':humidity_d}
    elif selected_country=='48h' and selected_city=='Umidade(%)':
        grafico={'Dia':dates_d,'Temperatura':humidity_d}

    df=pd.DataFrame(grafico)
    print(df.head(5))

    fig=px.line(data_frame=df,x='Dia',y='Temperatura')
    return fig
    


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
    