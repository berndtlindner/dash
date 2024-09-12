from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.widgets import CheckboxButtonGroup, DataTable, TableColumn, Button
from bokeh.transform import factor_cmap, factor_mark
from bokeh.events import ButtonClick

df = flowers.copy()
# This is a bokeh's ColumnDataSource (not pandas dataframe unfortunately)
source = ColumnDataSource(data=df)
labels = df.species.unique() # ['setosa', 'versicolor', 'virginica']
colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers['species']]

plot = figure(tools='tap')
plot.circle(
    x='sepal_length',y='sepal_width',size=20,source=source,
    color=factor_cmap('species', 'Category10_3', labels),
    fill_alpha=0.2
    )
Columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns] 
data_table = DataTable(source=source, columns=Columns, width=400, height=280)

def callback(attr, old, new):
# def callback():
    df_new = df[df.species.isin([labels[i] for i in new])]
    # df_new = df[df.species.isin([labels[i] for i in select.active])]
    # button.disabled=False
    source.data = ColumnDataSource(data=df_new).data

select = CheckboxButtonGroup(labels=['setosa', 'versicolor', 'virginica'], active=[0, 1])
button = Button(label="Run", disabled=True)
select.on_change('active',callback)
# button.on_click(callback)

doc = curdoc()
doc.add_root(column(select, button, plot, data_table))
### bokeh serve --show bokeh_app.py