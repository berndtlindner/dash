import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

### Generate the (pandas) data
test_list = ['a', 'b', 'c', 'd']
pdf = pd.DataFrame(test_list, columns=['letters'])

### Some useful functions 

# Generate a more basic html table UI output
# https://dash.plot.ly/getting-started
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# or rather use dash's more sleeky table UI output
def generate_dash_table(pdf):
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in pdf.columns],
        data=pdf.to_dict('records'),
        filtering=True,
        sorting=True
    )


### This is where the dash app's code starts

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Limit the number of rows to return'),
    dcc.Input(id='rows-limit', value=1, type='numeric'),
    html.Div(id='table-output'),
])

@app.callback(Output(component_id='table-output', component_property='children'),
        [Input(component_id='rows-limit', component_property='value')]
)
def update_info_table(input_value):
    if input_value == '':
        pdf_show = pdf
    else:
        rows=int(input_value)
        pdf_show = pdf.head(rows)
    return generate_dash_table(pdf_show)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051, debug=True)