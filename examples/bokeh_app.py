from bokeh.sampledata.iris import flowers
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.models.widgets import CheckboxButtonGroup, TextInput, DataTable, DateFormatter, TableColumn
from bokeh.transform import factor_cmap, factor_mark

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
    # print(select.active)
    df_new = df[df.species.isin([labels[i] for i in new])]
    source.data = ColumnDataSource(data=df_new).data
    #source.data.update(source)

select = CheckboxButtonGroup(labels=['setosa', 'versicolor', 'virginica'], active=[0, 1])
select.on_change('active',callback)

doc = curdoc()
doc.add_root(column(select, plot, data_table))
### bokeh serve --show bokeh_app.py