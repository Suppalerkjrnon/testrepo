import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [str(year) for year in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value="Yearly Statistics",
            placeholder='Select a report type',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': year, 'value': year} for year in year_list],
            value=year_list[-1],  # Set the default value to the last year in the list
            placeholder='Select a year',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    dcc.Input(id='input-container', disabled=True, style={'display': 'none'}),  # Hidden input container
    html.Div(id='output-div', className='output-class', style={'width': '80%', 'margin': 'auto', 'marginTop': '20px', 'border': '1px solid #ccc', 'padding': '10px'})
])

# Callbacks
@app.callback(
    Output(component_id='input-container', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

@app.callback(
    Output(component_id='output-div', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_report, selected_year):
    if selected_report == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales Fluctuation over Recession Period"))

        vehicle_sales_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(vehicle_sales_by_type, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles Sold by Vehicle Type"))

        recession_vehicle_ad_expenditure = recession_data[recession_data['Recession'] == 1].groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(recession_vehicle_ad_expenditure, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Advertising Expenditure Share by Vehicle Type during Recessions"))

        unemployment_effect = recession_data.groupby('Vehicle_Type')[['unemployment_rate', 'Automobile_Sales']].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemployment_effect, x='Vehicle_Type', y='Automobile_Sales', color='unemployment_rate', title="Effect of Unemployment Rate on Vehicle Type and Sales"))

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)], style={'display': 'flex', 'flex-direction': 'row', 'margin-bottom': '20px'}),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)], style={'display': 'flex', 'flex-direction': 'row', 'margin-bottom': '20px'})
        ]

    elif selected_report == 'Yearly Statistics':
        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales'))

        total_monthly_sales = data.groupby(['Year', 'Month'])['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(total_monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))

        avr_vdata = data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in the year {selected_year}'))

        total_ad_expenditure = data[data['Recession'] == 1].groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(total_ad_expenditure, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure by Vehicle Type'))

        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)], style={'display': 'flex'})
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
