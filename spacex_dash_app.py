# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([#TASK 2.2: Add two dropdown menus
                                html.Label("Launch Site selection:"),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                            {'label': 'ALL sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                    ],
                                    value='ALL sites',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                     )
                                    ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 100: '100'},
                                    value=[min_payload, max_payload]),
                
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        filtered_df=filtered_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total succes launches for all Launch Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df=filtered_df.groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, values='Launch Site', 
        names='Launch Site', 
        title=f'Total succes launches for {entered_site}')
        return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatterplot(entered_site,ranger):
    if entered_site == 'ALL':
        minimum=ranger[0]/1
        maximum=ranger[1]/1
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] >= minimum]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] <= maximum]
        fig = px.scatter(filtered_df, 
                x='Payload Mass (kg)',
                y='class',
                color="Launch Site",
                title="Correlation between Payload and Success for all Launch Sites")
        return fig
    else:

        filtered = spacex_df[spacex_df['Payload Mass (kg)'] >= ranger[0]]
        filtered = filtered[filtered['Payload Mass (kg)'] <= ranger[1]]
        filtered = filtered[filtered['Launch Site'] == entered_site]
        fig = px.scatter(filtered, 
                x='Payload Mass (kg)',
                y='class',
                color="Booster Version Category",
                title=f"Correlation between Payload and Booster Version Category for {entered_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
