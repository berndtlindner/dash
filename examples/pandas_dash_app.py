import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px

### Generate the (pandas) data
# https://medium.com/@harimittapalli/exploratory-data-analysis-iris-dataset-9920ea439a3e
import pandas as pd
from sklearn.datasets import load_iris
dataset=load_iris()
pdf=pd.DataFrame(dataset['data'],columns=['Petal length','Petal Width','Sepal Length','Sepal Width'])
pdf['Species']=dataset['target']
pdf['Species']=pdf['Species'].apply(lambda x: dataset['target_names'][x])

### Some useful functions 

# or rather use dash's more sleeky table UI output
def generate_dash_table(pdf):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pdf.columns],
        data=pdf.to_dict('records'),
        filtering=True,
        sorting=True,
        style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll'
        },
        # page_current=0,
        # page_size=10,
        # page_action='custom'
    )


### This is where the dash app's code starts

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'setosa', 'value': 'setosa'},
            {'label': 'versicolor', 'value': 'versicolor'},
            {'label': 'virginica', 'value': 'virginica'}
            ],
            value=['setosa', 'versicolor', 'virginica'],
            multi=True,
            style={'width': '400px'}
),
    html.Div(id='table-output'),
    dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"})
])

@app.callback(Output(component_id='table-output', component_property='children'),
        [Input(component_id='demo-dropdown', component_property='value')]
)
def update_info_table(input_value):
    pdf_show = pdf[pdf.Species.isin(input_value)]
    return generate_dash_table(pdf_show)

# https://github.com/plotly/dash-px/blob/master/app.py
@app.callback(Output(component_id="graph", component_property="figure"), 
        [Input(component_id='demo-dropdown', component_property='value')]
    )
def make_figure(input_value):
    return px.scatter(
        pdf[pdf.Species.isin(input_value)],
        x="Sepal Length",
        y="Sepal Width",
        color="Species",
        height=700,
    )

### python <app_filename>.py
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051, debug=True)