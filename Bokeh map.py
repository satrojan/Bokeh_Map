
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import warnings
def ignore_warnings(*args, **kwargs):
    pass
warnings.warn = ignore_warnings


# In[3]:


df_bokeh = pd.read_csv('./data/bokeh_monthly2.csv')


# In[5]:


from bokeh.io import output_notebook, show
output_notebook()
import os
#from ipywidgets import interact
from bokeh.models import GMapOptions
from bokeh.plotting import gmap
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import LinearInterpolator, CategoricalColorMapper,LinearColorMapper
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Slider
from bokeh.palettes import PuBu, Oranges, Plasma
from bokeh.io import curdoc

size_mapper = LinearInterpolator(x=[df_bokeh.wnvpresent.min(),df_bokeh.wnvpresent.max()],
                                y=[5,50])

color_mapper = LinearColorMapper(palette=Plasma[11],
                                 high=df_bokeh.wnvpresent.min(),
                                 low=df_bokeh.wnvpresent.max())

from ipywidgets import interact
from bokeh.io import push_notebook
#data1=ColumnDataSource(df_bokeh)

    #print('?')

#interact(update, m=(0,19,1))

map_options = GMapOptions(lat=41.881832, lng=-87.623177, map_type="roadmap", zoom=10)

# Replace the value below with your personal API key:
api_key = "AIzaSyCtCOtft7HLwShQRkglNePY-dwKAvhgnho"


hover = HoverTool(
        tooltips=[
            ("Trap",'@trap'),
            ("Species",'@species'),
            ("Coordinates", "(@latitude{0.0000}, @longitude{0.0000})"),
        ]
    )

p = gmap(api_key, map_options)

p.toolbar.active_inspect = [hover]

#data1=ColumnDataSource(df_bokeh)

#data = dict(lat=df_bokeh.latitude.unique(),
#            lon=df_bokeh.longitude.unique(),
#            trap=df_bokeh.trap.unique(),
#            species=df_bokeh.species)

#source=df_bokeh[df_bokeh.month_year==0]
source=df_bokeh

r = p.circle(x='longitude', y='latitude',
         size={'field':'wnvpresent','transform':size_mapper},
         fill_color={'field':'wnvpresent','transform':color_mapper},
         fill_alpha=0.6,
         source = df_bokeh[df_bokeh.month_year==5])
#p.circle(x="lon", y="lat", size=10, fill_color="blue", fill_alpha=0.6, source=data)
p.add_tools(hover)
#p.below=show(widgetbox(slider))
#show(widgetbox(slider))

#show(p,notebook_handle=True)

def update(m):
    #data = dict(lat=df_bokeh.loc[month_year].latitude,
    #        lon=df_bokeh.loc[month_year].longitude,
    #        trap=df_bokeh.loc[month_year].trap,
    #        species=df_bokeh.loc[month_year].species)
    #data1.data = data
    r.data_source.data['longitude']=df_bokeh[df_bokeh.month_year==m]['longitude']
    r.data_source.data['latitude']=df_bokeh[df_bokeh.month_year==m]['latitude']
    r.data_source.data['wnvpresent']=df_bokeh[df_bokeh.month_year==m]['wnvpresent']
    r.update
    T1 = str(df_bokeh[df_bokeh.month_year==m].month.unique()).replace('[','').replace(']','')
    T2 = str(df_bokeh[df_bokeh.month_year==m].year.unique()).replace('[','').replace(']','')
    p.title.text="Chicago - West Nile Outbreak - {}/{}".format(T1,T2)
    hover = HoverTool(
        tooltips=[
            ("Trap",'@trap'),
            ("Species",'@species'),
            ("Coordinates", "(@latitude{0.0000}, @longitude{0.0000})"),
        ]
    )
    #p.add_tools(hover)

    #hover.update
    #print(m)
    #p.title.text="Chicago - West Nile Outbreak {}".format
    push_notebook()

interact(update, m=(0,19,1))

#show(p,notebook_handle=True)
curdoc().add_root(p)
