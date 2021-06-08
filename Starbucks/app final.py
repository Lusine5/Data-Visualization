import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# data for map
data = pd.read_csv("Starbucks World.csv")


div_map_radioitem = html.Div(
					children = dcc.RadioItems(
							id = 'map-radio',
						    options=[
								{'label': 'Bubble Map', 'value': 'BM'},
								{'label': 'Choropleth Map', 'value': 'CM'},
						    ],
						    value='CM',
						    labelStyle={'display': 'inline-block'}
						)
			    )


# importing data
# This dataset is composed of a survey questions of over 100 respondents for their buying behavior at Starbucks.

df = pd.read_csv("Starbucks satisfactory survey.csv")

# column names
df.columns = ['Time','Gender','Age','Occupation','Income','Visit','Service_preferred',
              'Time_Spent_Frequency','Nearest_Store_Distance','Membership',
              'Frequent_Product','Avg_Money_Spent','Quality_Rating_vs_Other_Brands',
              'Price_Rating','Sales_Promotion_Importance','Ambiance_Rating','WiFi_Rating',
              'Service_Rating','Meetings','Promotion_Source','Loyalty']

# replace column values
df["Service_preferred"].replace({"never": "Never", "Never buy": "Never","Never ": "Never",}, inplace=True)

# Caculate the sum of each column and store it into a DataFrame

# dict Score
Score = {}
Score['Comparing with other coffee shop']=df['Quality_Rating_vs_Other_Brands'].mean()
Score['Price']=df['Price_Rating'].mean()
Score['SPImportance']=df['Sales_Promotion_Importance'].mean()
Score['Ambient'] = df['Ambiance_Rating'].mean()
Score['Wifi'] = df['WiFi_Rating'].mean()
Score['Service'] = df['Service_Rating'].mean()
Score['Meetings'] = df['Meetings'].mean()

# Convert Score into DataFrame
score_df = pd.DataFrame(Score.items(), columns=['Rate','Average Score'])
score_df

# dict Score
ScoreSum = {}
ScoreSum['Comparing with other coffee shop']=df['Quality_Rating_vs_Other_Brands'].sum()
ScoreSum['Price']=df['Price_Rating'].sum()
ScoreSum['SPImportance']=df['Sales_Promotion_Importance'].sum()
ScoreSum['Ambient'] = df['Ambiance_Rating'].sum()
ScoreSum['Wifi'] = df['WiFi_Rating'].sum()
ScoreSum['Service'] = df['Service_Rating'].sum()
ScoreSum['Meetings'] = df['Meetings'].sum()

# Convert ScoreSum into DataFrame
score_sum_df = pd.DataFrame(ScoreSum.items(), columns=['Rate','Sum of the Scores'])
score_sum_df

################

div_radioitem_1 = html.Div(
					children = dcc.RadioItems(
							id = 'survey-radio',
						    options=[
								{'label': 'Sum', 'value': 'Sum'},
								{'label': 'Average', 'value': 'Average'},
						    ],
						    value='Average',
						    labelStyle={'display': 'inline-block'}
						)
			    )

##############

div__radio = html.Div(
    dcc.RadioItems(
    id='checklist',
    options=[
        {'label': str(Occupation), 'value': str(Occupation)} for Occupation in df['Occupation'].unique()
    ],
    labelStyle={'display': 'inline-block'},
    value='Student'
)
)

#####################
div__drop = html.Div(
    dcc.RadioItems(
    id='dropdown',
    options=[
        {'label': str(Occupation), 'value': str(Occupation)} for Occupation in df['Occupation'].unique()

    ],
    labelStyle={'display': 'inline-block'},
    value='Student'
)
)

div_serv_graph = dcc.Graph(
    id='histogram_service',

)

div_Service = html.Div(children=[div__drop, div_serv_graph],
                   # className = 'test',
                   style={
                       'border': '1px {} solid'.format('block-borders'),
                       'margin': 'block-margins',
                       'width': '50%',
                       # 'height': sizes['subblock-heights'],
                   },

                   )

####################

div_gend_button = dcc.RadioItems(
    id='Checklist',
    options=[
        {'label': 'Female', 'value': 'Female'},
        {'label': 'Male', 'value': 'Male'},

    ],
    value = "Male",
    labelStyle={'display': 'inline-block'}
)

div_gend_graph = dcc.Graph(
						id = 'gend-histogram'
		    )


div_gender = html.Div(children = [div_gend_button, div_gend_graph],
					style = {
							'border': '1px {} solid'.format('block-borders'),
							'margin': 'block-margins',
							'width': '50%',
							#'height': sizes['subblock-heights'],
					}
				)

############

div_row = html.Div(children =	[div_Service,
								div_gender],
					style ={
							'border': '3px {} solid'.format('block-borders'),
							'margin': 'block-margins',
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

###############

div_ra = html.Div(
    dcc.RadioItems(
    id='radioit',
    options=[
        {'label': str(Occupation), 'value': str(Occupation)} for Occupation in df['Occupation'].unique()

    ],
    labelStyle={'display': 'inline-block'},
    value='Student'
)
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Starbucks", className="display-4"),
        html.Hr(),
        html.P("Starbucks has never just sold coffee.", className="lead"),
        html.Hr(),
        html.P("Starbucks has always sold an experience, with coffee adjacent."),
        dbc.Nav(
            [
                dbc.NavLink("Starbucks in California", href="/", active="exact"),
                dbc.NavLink("Customer Survey", href="/page-1", active="exact"),
                dbc.NavLink("Interactive Map", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            children=[html.H1(children='Starbucks in California'),
                      dcc.Markdown('''
                ### Starbucks History
                
                Starbucks, American company that is the largest coffeehouse chain in the world. Its headquarters are in Seattle, Washington.
                It was started in 1971 in Seattle, Washington by Jerry Baldwin, Gordon Bowker, and Zev Siegl who originally began by selling roasted coffee beans.
                Eventually, in 1987, employee Howard Schulz bought the company and began its rapid expansion.
                It is this global expansion that has ultimately allowed Starbucks to nearly double its number of locations over the past decade.
                As it stands, the number of Starbucks stores worldwide reached 31.3 thousand in 2019.
                
                
                The datasets contain information on Starbucks, as scraped in September 2014.
                Source: [Data World] (https://data.world/alice-c/starbucks) .
                '''),
                      #################

                      ]
        )

    elif pathname == "/page-1":
        return html.Div(
            children=[
                html.H1(children='Starbucks Customer Survey'),
                dcc.Markdown('''
        ### Survey from Malaysia on Starbucks Customer Behaviour
        
        #### Content
        
        * Demographic info about customers – gender, age range, employment status, income range
        * Their current behavior in buying Starbucks
        * Facilities and features of Starbucks that contribute to the behavior
        
        Starbucks started as a roaster and retailer of whole bean and ground coffee, tea and spices with a single store in Seattle’s Pike Place Market in 1971. 
        The company now operates more than 24,000 retail stores in 70 countries.
        As of today, Starbucks is the largest coffeehouse company in the world.
        
        Source: [Kaggle] (https://www.kaggle.com/mahirahmzh/starbucks-customer-retention-malaysia-survey).
        '''),
                dcc.Markdown('''
                * Comparing with other coffee shop: How would you rate the quality of Starbucks compared to other brands?
                * Price: How would you rate the price range at Starbucks?
                * SPImportance: How important are sales and promotions in your purchase decision?
                * Ambient : How would you rate the ambiance at Starbucks? (lighting, music, etc...)
                * Wifi : You rate the WiFi quality at Starbucks as..
                * Service : How would you rate the service at Starbucks? (Promptness, friendliness, etc..)
                * Meetings : How likely you will choose Starbucks for doing business meetings or hangout with friends?            
                '''),

                ###################
                div_radioitem_1,
                ###################
                dcc.Graph(
                    id='chart',
                ),
                #################
                div__radio,
                dcc.Graph(
                    id='visiting_frequency',
                    style={
                        'border': '1px {} solid'.format('block-borders'),
                        'margin': 'block-margins',
                        'width': '80%',
                        # 'height': sizes['subblock-heights'],
                    },
                ),
                dcc.Graph(
                    figure=px.pie(df, names='Occupation', title = "Pie chart of Occupation"),
                    style={
                        'border': '1px {} solid'.format('block-borders'),
                        'margin': 'block-margins',
                        'width': '100%',
                        # 'height': sizes['subblock-heights'],
                    },
                ),

                div_ra,
                dcc.Graph(
                    id='hist',
                ),
                div_row,


            ]
        )

    ################
    elif pathname == "/page-2":
        return html.Div(
            children=[
                html.H1(children='Number of Starbucks Stores Globally'),
                dcc.Markdown('''
        ### Starbucks World Statistic: 2014


        How many Starbucks are there worldwide?
        
        As of today, Starbucks is the largest coffeehouse company in the world.
        
        Source: [Data World] (https://data.world/alice-c/starbucks).
        '''),
                ###################
                div_map_radioitem,
                ###################
                dcc.Graph(
                    id='map-chart',
                ),
            ],
            style={
                'width': '100%',
                'height': 'subblock-heights',
            },

        )
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

###############
@app.callback(
    Output(component_id='map-chart', component_property='figure'),
    [Input(component_id='map-radio', component_property='value')],
)

def update_map_chart(option):

    if option == 'BM':
        return  px.scatter_geo(data,
                    # which column to use to set the color of markers
                    color="Numer of Starbucks",
                    # size of markers
                    size="Population",
                    lat=data["Latitude"],
                    lon=data["Longitude"],
                    # column added to hover information
                    hover_name="Country",
                    )

    else:
        return go.Figure(data=go.Choropleth(
    locations = data['Country_Alpha_3'],
    z = data['Numer of Starbucks'],
    text = data['Country'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    #colorbar_tickprefix = '$',
    colorbar_title = 'Numer<br>of Starbucks',
))


###############
@app.callback(
    Output(component_id='chart', component_property='figure'),
    [Input(component_id='survey-radio', component_property='value')],
)

def update_map_chart(option):
    if option == 'Average':
        return px.bar(score_df, x='Rate', y='Average Score', title="Which part of starbucks satisfies customers the most/least?")

    else:
        return px.bar(score_sum_df, x='Rate', y='Sum of the Scores', title="Which part of starbucks satisfies customers the most/least?")

###################

@app.callback(
    Output('visiting_frequency', 'figure'),
    [Input('checklist', 'value')]
)
def update_visiting_frequency(occupation_name):
            return px.histogram(df, x=df[df['Occupation'] == occupation_name]['Visit'],title="Visiting Frequency")


################
@app.callback(
    Output('histogram_service', 'figure'),
    [Input('dropdown', 'value')]
)
def update_histogram_service(occupation_name):
            return px.histogram(df, x=df[df['Occupation'] == occupation_name]['Service_preferred'], title="How do people buy starbucks?")


@app.callback(
    Output('gend-histogram', 'figure'),
    [Input('Checklist', 'value')]
)
def update_gend_histogram(gender):
            return px.histogram(df, x=df[df['Gender'] == gender]['Service_preferred'], title="Buy starbucks by gender?")


@app.callback(
    Output('hist', 'figure'),
    [Input('radioit', 'value')]
)

def update_hist(occ):
    dat = df[df['Occupation'] == occ]
    return px.bar(dat, y="Income", color="Gender", title="Income")
        #px.histogram(df, x=df[df['Occupation'] == occ]['Income'],fill = "Gender", title="Income")


# Run the app
if __name__ == '__main__':
	app.run_server(debug=True, port = 8081, host = '0.0.0.0')




