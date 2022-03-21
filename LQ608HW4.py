
"""
Question Two: Are stewards (steward activity measured by the ‘steward’ 
variable) having an impact on the health of trees?
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


######DF1########

#create an empty Data Frame
df1 = pd.DataFrame()

#Create a list of boroighs
boroughs = ["Queens", "Brooklyn", "Manhattan", "Staten Island", "Bronx"]

#use a for loop to iterate through the boroughs list 
for i in boroughs:
    #replace the space in staten island with %20 for url
    if i == "Staten Island":
        boroname = str(i.replace(' ', '%20'))
    else:
        boroname = i
    
    #concatinate the string with the brooname
    soql_url = (
            "https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$select=steward,spc_common,health,count(spc_common)"
            + "&$where=boroname='"
            + boroname + "'&$group=steward,spc_common,health")
    
 #temperary dataframe
    dftemp = pd.read_json(soql_url)

    dftemp['Borough'] = i
    
    #append to empty data frame
    df1 = df1.append(dftemp, ignore_index=True)
    



#Rename columns
df1.columns = ['Steward', 'Species', 'Health', 'Count',  'Borough']


#drop NA values
df1.dropna(axis=0, inplace=True)

borough_choices = df1["Borough"].unique()


#############DASH APP#########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#style sheet that enables breaking up app in half
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    #Title
    html.H2("New York City Tree Health"),
    html.H5("Data 608 Winter 2021"),
    html.H5("By: Layla Quinones"),
    html.H5("Homework 4"),

    
    #dropdown menue
    html.Div(
        [
            #Dropdown for df1
            dcc.Dropdown(
                id="Borough",
                options=[{
                    'label': i,
                    'value': i
                } for i in borough_choices],
                value='Manhattan'),
        ],
        
        style={'width': '25%',
               'display': 'inline-block'}),
        
    
    html.Div([
        #Both are the same type of graph
        #Graph One
        dcc.Graph(id='graph1', figure={}, clickData=None, hoverData=None, # I assigned None for notes, these are None, unless you specify otherwise.
                  className='six columns'), #bar graphs are six columns
        
       #Graph Two
       dcc.Graph(id='graph2', figure={}, clickData=None, hoverData=None, # I assigned None for notes, these are None, unless you specify otherwise.
                 className='six columns'), #bar graphs are six columns
       
       ])

    
    ])
    
    
#Graph one
#callback populates charts in figure={} area - App triggered by Borough Value
@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('Borough', 'value')])

#borough value passed into callback
def update_graph1(borough):
    
    #First Graph Borough, Type and Health
    df_plot1 = df1[df1['Borough'] == borough]
    
    # Proportion for normalizing of data for speices
    df_plot1['Count'] = round(df_plot1['Count'] / df_plot1.groupby('Species')['Count'].transform('sum') * 100, 2)
    
    #create a pivot table for first graph
    pv1 = pd.pivot_table(
        df_plot1,
        index=['Species'],
        columns=['Health'],
        values=['Count'],
        aggfunc=sum,
        fill_value=0)
    
    #Three graphs to present Good, Fair and Poor depending on health variable
    trace1 = go.Bar(x=pv1.index, y=pv1[('Count', 'Good')], name='Good', marker_color=px.colors.qualitative.Dark24[2])
    trace2 = go.Bar(x=pv1.index, y=pv1[('Count', 'Fair')], name='Fair', marker_color=px.colors.qualitative.Dark24[0])
    trace3 = go.Bar(x=pv1.index, y=pv1[('Count', 'Poor')], name='Poor', marker_color=px.colors.qualitative.Dark24[1])
    
    #returns graph
    return {
        'data': [trace1, trace2, trace3],
        'layout':
            go.Layout(
                title='Health Proportion for Trees by Speices in {}'.format(borough),
                barmode='stack'
            )
    } 
#GRAPh Two - callback populates chart in figure={} area - App triggered by Borough Value
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('Borough', 'value')])

#borough value passed into callback
def update_graph2(borough):

    #Then Graph Borough, Steward and Health
    df_plot2 = df1[df1['Borough'] == borough]
    
    # Proportion for normalizing of data for steward
    df_plot2['Count'] = round(df_plot2['Count'] / df_plot2.groupby('Steward')['Count'].transform('sum') * 100, 2)
 
    #create a pivot table
    pv2 = pd.pivot_table(
           df_plot2,
           index=['Steward'],
           columns=['Health'],
           values=['Count'],
           aggfunc=sum,
           fill_value=0)
       
    #Three graphs to present Good, Fair and Poor depending on health variable
    trace4 = go.Bar(x=pv2.index, y=pv2[('Count', 'Good')], name='Good', marker_color=px.colors.qualitative.Dark24[2])
    trace5 = go.Bar(x=pv2.index, y=pv2[('Count', 'Fair')], name='Fair', marker_color=px.colors.qualitative.Dark24[0])
    trace6 = go.Bar(x=pv2.index, y=pv2[('Count', 'Poor')], name='Poor', marker_color=px.colors.qualitative.Dark24[1])

    #returns graph
    return {
        'data': [trace4, trace5, trace6],
        'layout':
            go.Layout(
                title='Health Proportion for Trees by Steward in {}'.format(borough),
                barmode='stack'
            )
    } 

if __name__ == '__main__':
    app.run_server(debug=True)

'''
Question 1:
    In the app we see a visualization that 
    stacks the proportions of various types of trees that are 
    in good poor and fair condition. Poor tree proporition is stacked on top, 
    fair is stacked in the middle and Good at the bottom. The user can choose 
    on the dropdown the borough in which these proportions exist. These trees
    are grouped by speices.
    
    Question 2:
        In the app we see a visualization that 
        stacks the various types of trees that are 
        in good poor and fair condition. The user can choose the borough
        They want to view for each.
        Poor tree proporition is stacked on top, 
        fair is stacked in the middle and Good at the bottom. The user can choose 
        on the dropdown the borough in which these proportions exist. These are
        grouped based on steward status. We generally see that steward variable
        with the value of NONE has less trees that are in "Good" health compared
        to the others.
    
'''