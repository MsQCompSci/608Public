import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import json


#get the data
url = ("https://data.cityofnewyork.us/resource/s52a-8aq6.json?$limit=9000")
df1 = pd.read_json(url)

boroughChoices = ['Manhattan', 'Bronx', 'Queens', 'Staten Island', 'Brooklyn', 'ALL']

schools = df1['dbn'].unique() #unique schools only


#style sheet that enables breaking up app in half
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([  #Title
      html.H1("New York City Public School Data"),
      html.H4("By: Layla Quinones")],
      style = {'textAlign': 'center', 'color':'blue'}),
    
    html.Div([ 
        html.H3("Choose a Borough"),
        dcc.Dropdown(
            id="borough",
            options=[{
                'label': i,
                'value': i
                } for i in boroughChoices],
            value = boroughChoices[0]), #uses broughs    
   ],
   style={'width': '60%','display': 'inline-block', 'margin-left': '10%'}),

    
    html.Div([
                
                dcc.Graph(id='bar', figure={}, clickData=None, hoverData=None, # I assigned None for notes, these are None, unless you specify otherwise.
                         )
                ],
                    style={'width': '95%','display': 'inline-block'}),
    
    
    html.Div([
        html.H3("Choose a year"),
        #Dropdown for df1
        dcc.Dropdown(
            id="year",
            options=[{
                'label': i,
                'value': i
            } for i in df1['year'].unique()],
            value=df1['year'].unique()[0]), #uses years   
    ],
        style={'width': '60%','display': 'inline-block', 'margin-left': '10%'}),
    
    
    html.Div([
        html.Div([
            
            dcc.Graph(id='gender', figure={}, clickData=None, hoverData=None, # I assigned None for notes, these are None, unless you specify otherwise.
                     ) #bar graphs are six columns
            ],
                style={'width': '40%','display': 'inline-block'}),
        
        html.Div([
        #Gender
        dcc.Graph(id='ethnicity', figure={}, clickData=None, hoverData=None, # I assigned None for notes, these are None, unless you specify otherwise.
                  ), #bar graphs are six columns
        ],
            style={'width': '50%','display': 'inline-block'}),
    
        # dcc.Store stores the intermediate value
        dcc.Store(id='schoolList', storage_type='session')
       ])
    ])


#callback should fix displays based on Borough & year
@app.callback(
    dash.dependencies.Output('schoolList', 'data'),
    [dash.dependencies.Input('borough', 'value'),
     dash.dependencies.Input('year', 'value')])

def update_table(borough, year):
    schoolList = []
    
    if borough == boroughChoices[0]:#manhattan 
        for i in schools:
          if 'M' in i:
              schoolList.append(i)
    elif borough == boroughChoices[1]: #bronx
        for i in schools:
          if 'X' in i:
              schoolList.append(i)
    elif borough == boroughChoices[2]: #queens
        for i in schools:
          if 'Q' in i:
              schoolList.append(i)
    elif borough == boroughChoices[3]: #staten island
        for i in schools:
          if 'R' in i:
              schoolList.append(i)
    elif borough == boroughChoices[4]: #brooklyn
        for i in schools:
          if 'Q' in i:
              schoolList.append(i)
    elif borough == boroughChoices[5]:
        schoolList = schools
    
    #sort through the dataframe and replace this with list of DFs
    schoolList = df1.loc[df1['dbn'].isin(schoolList)] #school list by borough
    schoolList = schoolList.loc[schoolList['year']==year] #year
    schoolList = schoolList.to_json(orient="index")
    return schoolList

#callback should fix displays based on Borough & year
@app.callback(
    dash.dependencies.Output('gender', 'figure'),
    [dash.dependencies.Input('schoolList', 'data'),
     dash.dependencies.Input('borough', 'value'),
     dash.dependencies.Input('year', 'value')])

def update_gender(schoolList, borough, year):
    tempDF = json.loads(schoolList)
    tempDF = pd.DataFrame.from_dict(tempDF, orient="index") 
    #gender
    genDF = tempDF[['female_1', 'male_1']]
    genDF = genDF.rename(columns = {'female_1':'female', 'male_1':'male'})
    
    genDF = pd.melt(genDF) #long format
    #Creating the ethnicity pie chart
    genPie = px.pie(genDF, values="value", names='variable', title='Gender Data during {} SY'.format(year))
    genPie.update_layout(title_x=0.5)
    
    #returns graph
    return genPie

#callback should fix displays based on Borough & year
@app.callback(
    dash.dependencies.Output('ethnicity', 'figure'),
    [dash.dependencies.Input('schoolList', 'data'),
     dash.dependencies.Input('borough', 'value'),
     dash.dependencies.Input('year', 'value')])

def update_ethn(schoolList, borough, year):
    tempDF = json.loads(schoolList)
    tempDF = pd.DataFrame.from_dict(tempDF,orient="index")
    #Ethnicity
    ethnDF = tempDF[['asian_1','black_1','hispanic_1','multiple_race_categories_not_represented_1','white_2']]
    ethnDF = ethnDF.rename(columns = {'asian_1':'Asian', 'black_1': 'Black','hispanic_1':'Latinx','multiple_race_categories_not_represented_1': 'Not Represented','white_2':'White'})
    
    ethnDF = pd.melt(ethnDF) #long format
    
    #Creating the ethnicity pie chart
    ethnPie = px.pie(ethnDF, values="value", names='variable', title='Ethnicity Data during {} SY'.format(year))
    ethnPie.update_layout(title_x=0.5)
    
    return ethnPie

#BARGRAPHS
@app.callback(
    dash.dependencies.Output('bar', 'figure'),
     [dash.dependencies.Input('borough', 'value')])

def update_bar(borough):
    schoolList = []
    
    if borough == boroughChoices[0]:#manhattan 
        for i in schools:
          if 'M' in i:
              schoolList.append(i)
    elif borough == boroughChoices[1]: #bronx
        for i in schools:
          if 'X' in i:
              schoolList.append(i)
    elif borough == boroughChoices[2]: #queens
        for i in schools:
          if 'Q' in i:
              schoolList.append(i)
    elif borough == boroughChoices[3]: #staten island
        for i in schools:
          if 'R' in i:
              schoolList.append(i)
    elif borough == boroughChoices[4]: #brooklyn
        for i in schools:
          if 'Q' in i:
              schoolList.append(i)
    elif borough == boroughChoices[5]:
        schoolList = schools
    
    tempDF = df1.loc[df1['dbn'].isin(schoolList)] #school list by borough
    
    Mdisability = tempDF[['year', 'students_with_disabilities_1', 'total_enrollment', 'poverty_1']]
    MdisA = Mdisability.loc[Mdisability['year'] == "2013-14"]
    sumA = list(MdisA.sum()[1:])
    MdisB = Mdisability.loc[Mdisability['year'] == "2014-15"]
    sumB = list(MdisB.sum()[1:])
    MdisC = Mdisability.loc[Mdisability['year'] == "2015-16"]
    sumC = list(MdisC.sum()[1:])
    MdisD = Mdisability.loc[Mdisability['year'] == "2016-17"]
    sumD = list(MdisD.sum()[1:])
    MdisE = Mdisability.loc[Mdisability['year'] == "2017-18"]
    sumE = list(MdisE.sum()[1:])
    
    data = {'year': [2013, 2014,2015,2016,2017],
       'Disabilities': [sumA[0], sumB[0], sumC[0],sumD[0],sumE[0]],
        'Poverty': [sumA[2], sumB[2], sumC[2],sumD[2],sumE[2]],
        'Total': [sumA[1], sumB[1], sumC[1],sumD[1],sumE[1]]}
    sumDF = pd.DataFrame(data)
    sumDF = pd.melt(sumDF, id_vars = 'year')
    barGraph = px.bar(sumDF, x = 'year', color = 'variable', y = 'value', barmode = 'group', title = "Student Enrollment for {}".format(borough))
    
    barGraph.update_layout(title_x=0.5).update_layout(title_x=0.5)
    
    return barGraph

if __name__ == '__main__':
    app.run_server(debug=True)
