import json
import streamlit as st
from pathlib import Path
from st_on_hover_tabs import on_hover_tabs

# As for Streamlit Elements, we will need all these objects.
# All available objects and there usage are listed there: https://github.com/okld/streamlit-elements#getting-started

from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# Change page layout to make the dashboard take the whole page.

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], iconName=['dashboard', 'money', 'economy'])

# Initialize default data for code editor and chart.
#
# For this tutorial, we will need data for a Nivo Bump chart.
# You can get random data there, in tab 'data': https://nivo.rocks/bump/
#
# As you will see below, this session state item will be updated when our
# code editor change, and it will be read by Nivo Bump chart to draw the data.

if "data" not in st.session_state:
    st.session_state.data = Path("data.json").read_text()

# Define a default dashboard layout.
# Dashboard grid has 12 columns by default.
#
# For more information on available parameters:
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    # Editor item is positioned in coordinates x=0 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("editor", 0, 0, 6, 3),
    # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("chart", 6, 0, 6, 3),
    # Media item is positioned in coordinates x=0 and y=3, and takes 6/12 columns and has a height of 4.
    dashboard.Item("media", 0 , 3, 6, 3),
    dashboard.Item("data", 6, 3, 6, 3),
]

# Create a frame to display elements.

if tabs =='Dashboard':
    with elements("demo"):
        with dashboard.Grid(layout, draggableHandle=".draggable"):
            with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}):
                padding="5px 15px 5px 15px"
                with mui.Stack(
                    className="draggable",
                    alignItems="center",
                    direction="row",
                    spacing=1,
                    sx={
                        "padding": padding,
                        "borderBottom": 1,
                        "borderColor": "divider",
                    }):
                    mui.icon.PieChart()
                    mui.Typography("Radar chart", sx={"flex": 1})
                    mui.IconButton(mui.icon.DarkMode)
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    editor.Monaco(
                        defaultValue=st.session_state.data,
                        language="json",
                        onChange=lazy(sync("data"))
                    )
                with mui.CardActions:
                    mui.Button("Apply changes", onClick=sync())

           

elif tabs == 'Money':
    st.title("Paper")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Economy':
    st.title("Tom")
    st.write('Name of option is {}'.format(tabs))