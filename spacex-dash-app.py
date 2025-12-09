# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
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
                                dcc.Dropdown(id='site-dropdown',  options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},], value = 'ALL', placeholder = "Select a Launch Site here", searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                2000: '2000', 4000: '4000', 6000: '6000', 8000: '8000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launch rates for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_specific_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        outcome_counts = site_specific_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count'] # Rename columns for clarity

        fig = px.pie(outcome_counts, values='Count', 
        names='Outcome', 
        title=f'Success launch rate for site: {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))
def get_scatter_chart(entered_site, entered_payload):
    # Ensure entered_payload is a list or tuple of [min_payload, max_payload]
    min_payload, max_payload = entered_payload[0], entered_payload[1]

    # First, filter the DataFrame based on the payload mass range
    # This ensures both 'ALL' sites and specific sites are filtered by payload
    filtered_payload_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= min_payload) &
        (spacex_df['Payload Mass (kg)'] <= max_payload)
    ]

    if entered_site == 'ALL':
        # If 'ALL' sites are selected, use the payload-filtered DataFrame
        # to render a scatter plot for all sites
        fig = px.scatter(filtered_payload_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for All Sites (Payload: {min_payload}-{max_payload} kg)',
                         #labels={'class': 'Launch Outcome (0=Failure, 1=Success)'},
                         #color_discrete_sequence=['#2649B2', '#4A74F3', '#8E7DE3', '#9D5CE6', '#B55CE6', '#6C8BE0', '#D4D9F0'] # L'Oréal color palette
                        )
        return fig
    else:
        # If a specific launch site is selected,
        # filter the payload-filtered DataFrame further for the selected site
        site_specific_df = filtered_payload_df[filtered_payload_df['Launch Site'] == entered_site]

        fig = px.scatter(site_specific_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Outcome for {entered_site} (Payload: {min_payload}-{max_payload} kg)',
                         #labels={'class': 'Launch Outcome (0=Failure, 1=Success)'},
                         #color_discrete_sequence=['#2649B2', '#4A74F3', '#8E7DE3', '#9D5CE6', '#B55CE6', '#6C8BE0', '#D4D9F0'] # L'Oréal color palette
                        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run()