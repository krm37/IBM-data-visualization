#!/usr/bin/env python
# coding: utf-8





import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",style={'textAlign':'center','color':'#503D36','fontsize':0}),#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={'width': '70%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
        )
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            style={'width': '70%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
            
        )),
    html.Div([
        #TASK 2.3: Add a division for output display
        html.Div(id='output-container',
                className='chart-grid',
                style={'display':'flex'}
                ),
        ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value')
    )

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the output container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics,selected_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
            ).update_layout(title_text='Average Automobile Sales fluctuation over Recession Period', title_x=0.5),)
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                ).update_layout(title_text='Average Number Of Vehicles Sold By Vehicle Type', title_x=0.5),
            )
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                ).update_layout(title_text='Total Expenditure Share by Vehicle Type', title_x=0.5),

            )     
        exp_bar= recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        R_chart4=dcc.Graph(
            figure=px.bar(
                exp_bar,
                x='Vehicle_Type',
                y='unemployment_rate',
                ).update_layout(title_text='Average Unemployment Rate For Vehicle Type', title_x=0.5)
            )
        return [
            html.Div(className='chart-item', children=[html.Div(children=[R_chart1]),html.Div(children=[R_chart2])],style={'flex': '50%'}),
            html.Div(className='chart-item', children=[html.Div(children=[R_chart3]),html.Div(children=[R_chart4])],style={'flex': '50%'})]
        
    elif(selected_year and selected_statistics=='Yearly Statistics'):
        
        yearly_data = data[data['Year'] == selected_year]
        
        
        # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            ).update_layout(title_text='Yearly Automobile Sales', title_x=0.5)
            )
            
        # Plot 2 :Total Monthly Automobile sales using line chart.
        mas=yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
            ).update_layout(title_text='Monthly Automobile Sales in the year {}'.format(selected_year), title_x=0.5)
        )
        
        # Plot bar chart for average number of vehicles sold during the given year
  
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                ).update_layout(title_text='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year), title_x=0.5)
            )
                
        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        total_adv_exp=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4=dcc.Graph(
            figure=px.pie(
                total_adv_exp,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Sum Of Advertising Expenditure in the year {}'.format(selected_year)
            ).update_layout(title_text='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year), title_x=0.5)
        )
        return [
            html.Div(className='chart-item', children=[html.Div(children=[Y_chart1]),html.Div(children=[Y_chart2])],style={'flex':'%50'}),
            html.Div(className='chart-item', children=[html.Div(children=[Y_chart3]),html.Div(children=[Y_chart4])],style={'flex':'%50'})]
    
if __name__ == '__main__':
    app.run_server(debug=True)



