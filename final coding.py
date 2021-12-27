import csv

import pandas as pd
pd.set_option('max_rows', 20)
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default = "browser"

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

'''---------------------------------------------------
             Read and process data
---------------------------------------------------'''

Cases_Deaths_URL = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
Total_Stat_URL = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'
Vaccine_URL = 'https://covid19.who.int/who-data/vaccination-data.csv'

vaccine = pd.read_csv(Vaccine_URL)
vaccine = vaccine[vaccine['COUNTRY'] == 'Viet Nam']
vaccine = vaccine.reset_index()

vac = pd.read_csv(Cases_Deaths_URL, usecols=['Country','New_cases', 'New_deaths', 'Date_reported'])
vac = vac[vac['Country']=='Viet Nam']

Total = pd.read_csv(Total_Stat_URL)
Total = Total.loc['Viet Nam']


app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

'''---------------------------------------------------
             Set up image, color
---------------------------------------------------'''

image2 = "https://www.sanofi.com.vn/-/media/Project/One-Sanofi-Web/Websites/Asia-Pacific/Sanofi-VN/Home/thong-tin-bao-chi/covid-19-nhan-manh-gia-tri-quan-trong-cua-viec-cham-soc-ban-than/Article-block-Covid-19.jpg?la=vi&hash=9763B0A5603D3FED373554950C0F6854"
image1 = 'https://d18lkz4dllo6v2.cloudfront.net/cumulus_uploads/entry/2020-04-06/COVID%20.jpg?w=660'
colors = {
    'background' : '#2B547E',
    'bodyColor' : '#00008B',
    'text' : '#FF0000',
    'Purple' : '#800080',
    'Red': '#FF0000',
    'Charcoal' : '#34282C',
    'Night blue' : '#151B54',
    'White' : '#FFFFFF',
    'Aquamarine' : '#7FFD4',
    'Purple Flower' : 'A74AC7',
    'Magenta' : '#FF00FF',
    'Orange' : '#FFA500',
    'Gray' : '#808080',
    'Plum' : '#CA226B'
}

'''---------------------------------------------------
                     PAGE HEADER
---------------------------------------------------'''
team_member = [
    dbc.Col(html.H5('Nguyen Phuong Thao Vy', style={'color' : colors['Orange']}), width='auto'),
    dbc.Col(html.H5('Vu Duy Tung', style={'color' : colors['Orange']}), width='auto'),
    dbc.Col(html.H5('Ta Viet Thang', style={'color' : colors['Orange']}), width='auto'),
    dbc.Col(html.H5('Chau Minh Khai', style={'color' : colors['Orange']}), width='auto')
]

def generate_page_header():
    header1 = dbc.Row(
        [
            dbc.Col(
                html.H3("Welcome to COMP1010 project:"),
                style={
                    'textAlign' : 'center',
                    'color' : colors['text']
                }
            ),
        ],
        # justify='center',
        # align='center',
    )
    header2 = dbc.Row(
        [
            dbc.Col(
                html.H1("A Dashboard about Covid-19 Situation in Vietnam"),
                style={
                    'textAlign' : 'center',
                    'color' : colors['text']
                }
            ),
        ],
        # justify='center',
        # align='center',
    )
    header3 = dbc.Row(
        team_member,
        justify='center',
        align='center',
        style={
            'backgroundColor' : colors['Gray']
        }
    )
    header = [header1, header2, header3]
    return header

'''---------------------------------------------------
             Input your email
---------------------------------------------------'''
def Input_email():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H5([
                        "Enter your email:   ",
                        dcc.Input(id='my-input', value='Alibaba@vinuni.edu.vn', type='email')
                    ], style={'textAlign':'center', 'color':'#4C8C0F'})
                    ),
                ]
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(html.H4(id='my-output', style={'textAlign': 'center', 'color' : '#4C8C0F'}))
                ]
            ),

        ]
    )

'''---------------------------------------------------------------
         Generate Card for Total Cases and Total Deaths
---------------------------------------------------------------'''
def Card_with_stat(name, image, num, color):
    if( color == 'Red' ): BG = 'info'
    else: BG = 'warning'
    card = dbc.Card(
        [
            dbc.CardImg(src=image, top=True),
            dbc.CardBody(
                [
                    html.H3(
                        name,
                        style={
                            'textAlign':'center',
                            'color':colors[color]
                        }
                    ),
                    html.H4(
                        '{:,}'.format(num),
                        style={
                            'textAlign':'center',
                            'color':colors[color]
                        }
                    ),
                ]
            ),
        ],
        style={'width' : '18rem'},
        color=BG,
        inverse='True'
    )
    return card

def Generate_card():
    return dbc.Row(
        [
            dbc.Col(Card_with_stat('Total cases', image1, Total['WHO Region'], 'Charcoal'), width='auto'),
            dbc.Col(Card_with_stat('Total deaths', image2, Total['Cases - newly reported in last 24 hours'], 'Red'), width='auto'),
        ],
        align='center',
        justify='center'
    )

'''---------------------------------------------------
               GENERATE TABLE
---------------------------------------------------'''
def Table():
    new_vac = vac.iloc[-15:]
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(new_vac[['Date_reported','New_cases','New_deaths']].columns),
                    line_color='darkslategray',
                    fill_color='royalblue',
                    align='center',
                    font=dict(color='white', size=14),
                    height=35
        ),
        cells=dict(values=[new_vac.Date_reported, new_vac.New_cases, new_vac.New_deaths],
                   line_color='darkslategray',
                   fill_color='paleturquoise',
                   align='center',
                   font=dict(color='black', size=14),
                   height=25
        ))
    ])
    return fig

def Generate_table():
    return html.Div([
        dcc.Graph(
            id = 'Table',
            figure = Table().update_layout(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )
        )
    ])

'''--------------------------------------------------------------------------
        GENERATE LINE GRAPH AND BUTTON TO CHANGE THE STATUS
---------------------------------------------------------------------------'''
def check_list():
    return dcc.RadioItems(
        id='check_list',
        options=[{'label': i, 'value': i} for i in ['New_cases', 'New_deaths']],
        value='New_cases',
        labelStyle={'display': 'block'},
        style={"padding": "10px", "max-width": "800px", "margin": "auto"},
    )

def Cases_Deaths_LineGraph(cases_or_deaths):
    fig = px.line(vac, x = vac.Date_reported, y = cases_or_deaths, title='Daily cases in Vietnam', height=600, color_discrete_sequence =['maroon'], markers=True)
    fig.update_layout(title_x=0.5, xaxis_title="Date", yaxis_title='New Cases')
    fig.update_layout(
        template='plotly_dark',
        # plot_bgcolor=colors['Orange'],
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    fig.update_yaxes(visible=False, fixedrange=True)
    return fig

def graph1():
    return dcc.Graph(id='graph1', figure=Cases_Deaths_LineGraph(vac.New_cases))

'''---------------------------------------------------
               GENERATE BAR CHART
---------------------------------------------------'''
def Cases_Deaths_BarChart():
    fig = px.bar(vac, x = vac.Date_reported, y = [vac.New_deaths, vac.New_cases] * 719, barmode='group')
    fig.update_layout(
        template='plotly_dark',
        # plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    return fig

def bar_chart():
    return dcc.Graph(id='bar_chart', figure=Cases_Deaths_BarChart())


'''---------------------------------------------------
               GENERATE PIE CHART
---------------------------------------------------'''
def Vaccine_Pie_Chart():
    Full_Dose = vaccine.loc[0]['PERSONS_FULLY_VACCINATED']
    OnePlus_Dose = vaccine.loc[0]['PERSONS_VACCINATED_1PLUS_DOSE']

    valuee = [Full_Dose, OnePlus_Dose - Full_Dose]
    namee = ['People who got 1 dose', 'People fully vaccinated']

    fig = px.pie(values=valuee, names=namee)
    return fig

def Generate_Pie_Chart():
    return dcc.Graph(
        figure=Vaccine_Pie_Chart().update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
        )
    )

'''---------------------------------------------------
          GENERATE CARDS FOR VACCINE INFO
---------------------------------------------------'''
def Card_Vaccine(header, text):
    if header == 'Total Vaccination':
        COLOR = "danger"
    if header == 'Vaccine used':
        COLOR = "success"
    if header == 'Number vaccine types used':
        COLOR = "warning"
    card_head_style = {'textAlign' : 'center', 'fontSize' : '150%'}
    card_body_style = {'textAlign' : 'center', 'fontSize' : '200%'}
    return dbc.Card(
        [
            dbc.CardHeader(header , style=card_head_style),
            dbc.CardBody([
                html.H5(text),
            ], style=card_body_style)
        ],
        color=COLOR,
        inverse=True
    )

'''---------------------------------------------------
          LAYOUT TO SHOW ALL VACCINE DATA
---------------------------------------------------'''
def Vaccine_Info():
    return html.Div([
        dbc.Row(
            [
                dbc.Col(Generate_Pie_Chart(), width={'size': 12})
            ],
            align='center',
            justify='center'
        ),
        dbc.Row(
            [
                dbc.Col(Card_Vaccine(
                    header='Total Vaccination',
                    text= '{:,}'.format(vaccine.loc[0]['TOTAL_VACCINATIONS'])
                )),
                dbc.Col(Card_Vaccine(
                    header='Vaccine used',
                    text=vaccine.loc[0]['VACCINES_USED']
                )),
                dbc.Col(Card_Vaccine(
                    header='Number vaccine types used',
                    text=str(vaccine.loc[0]['NUMBER_VACCINES_TYPES_USED'])
                )),
            ],
            className="g-0",
        )
    ])


'''----------------------------------------------------------
               GENERATE CARD FOR READ/WATCH NEWS
----------------------------------------------------------'''
def New(link, title, text, button, iimage):
    return dbc.Card(
        [
            dbc.CardImg(src = iimage, top = True),
            dbc.CardBody(
                [
                    html.H3(title),
                    html.H5(text),
                    dbc.Button(button, href=link, color='warning')
                ]
            )
        ],
        color='info',
        inverse=True
    )


def News_with_card():
    return dbc.Row(
        [
            dbc.Col(New(
                link='https://www.youtube.com/watch?v=wT2m3kljcSU',
                title='Fake news',
                text='The explosion of coranavirus also leads to the raise of fake new on social medias',
                button='Lets watch',
                iimage='https://image.vietnamlawmagazine.vn/uploadvietnamlaw/2021/7/23/fake_newsjpg172654812.jpg'
            ), width={'size':3}),
            dbc.Col(New(
                link='https://www.youtube.com/watch?v=qQUdy5ZXAqo',
                title='Deadliest pandemics in History (till 2020)',
                text='Plagues and epidemics have ravaged humanity throughout its existence, often changing the course of history',
                button='Lets see',
                iimage='https://i.ytimg.com/vi/qQUdy5ZXAqo/maxresdefault.jpg'
            ), width={'size':3}),
            dbc.Col(New(
                link='https://www.usnews.com/news/health-news/articles/2021-12-10/pandemic-mystery-scientists-focus-on-covids-animal-origins?fbclid=IwAR0dUFwC6fUZsLL4WnJquaR6ysYADavPEMKNcri_oOkyMMHfluQixS7e7nA',
                title='Scientists Focus on COVID Animal Origins',
                text='Most scientists believe it emerged in the wild and jumped from bats to humans, either directly or through another animal. Others theorize it escaped from a Chinese lab.',
                button='Read this',
                iimage='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQyk2DAWarOLrYFlcwYxApLJj09WZZsIc_dQ&usqp=CAU'
            ), width={'size':3}),
            dbc.Col(New(
                link='https://e.vnexpress.net/news/news/vietnam-falls-to-bottom-of-bloomberg-covid-resilience-ranking-4407673.html?fbclid=IwAR1xsPiXIPV-9hnCuW2NUMXPyOH0BjWpZCcikd8XaTRzZZmGc3if0rVTTBM',
                title='Viet Nam',
                text='Vietnam falls to bottom of Bloomberg Covid resilience ranking',
                button='Why',
                iimage='https://file1.dangcongsan.vn/data/0/images/2021/06/14/chamsocytepv/covid-khauhieu.jpg?dpi=150&quality=100&w=680'
            ), width={'size':3}),
        ]
    )



'''---------------------------------------------------
                    FINAL LAYOUT
---------------------------------------------------'''
def generate_layout():
    header = generate_page_header()
    layout = dbc.Container(
        [
            header[0],
            header[1],
            header[2],
            html.Br(),
            Input_email(), html.Hr(),
            Generate_card(), html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('Statistics for the numbers of new cases and new deaths', style={'color': colors['Plum']}), width='auto')
                ],
                align='center',
                justify='center'
            ),
            dbc.Row(
                [
                    dbc.Col(Generate_table())
                ],
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('The fluctuates in the numbers of new cases and new deaths',
                                    style={'color': colors['Plum']}), width='auto')
                ],
                align='center',
                justify='center'
            ),
            dbc.Row(
                [
                    dbc.Col(check_list(), width='auto'),
                    dbc.Col(graph1())
                ],
                align='center'
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('Bar chart to compare between new cases and new deaths', style={'color':colors['Plum']}), width='auto')
                ],
                align='center',
                justify='center'
            ),
            dbc.Row(
                [
                    dbc.Col(bar_chart()),
                ],
                align='center',
                justify='center'
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('Vaccine Information', style={'color': colors['Plum']}), width='auto')
                ],
                align='center',
                justify='center'
            ),
            Vaccine_Info(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(html.H3('Read/Watch more about Covid-19', style={'color': colors['Plum']}))
                ],
            ),
            News_with_card(),
        ],
        fluid=True,
    )

    return layout

'''---------------------------------------------------
               INTERACTIVE FUNCTIONS
---------------------------------------------------'''
@app.callback(
    [Output('my-output', 'children'),
     Output('graph1', 'figure')],
    [Input('my-input', 'value'),
    Input('check_list', 'value')]
)
def update_output_div(input_value1, input_value2):
    your_name = ''
    for i in input_value1:
        if i == '@': break
        your_name += i

    if input_value2 == 'New_cases':
        fig = Cases_Deaths_LineGraph(vac.New_cases)
    else:
        fig = Cases_Deaths_LineGraph(vac.New_deaths)

    return f'WELCOME "{your_name.upper()}" TO OUR WEBSITE', fig



app.layout = generate_layout()

'''---------------------------------------------------
               RUN THE SERVER
---------------------------------------------------'''

if __name__ == "__main__":
    app.run_server(debug = True)