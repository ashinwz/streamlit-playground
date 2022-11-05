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
    tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], iconName=['dashboard', 'money', 'economy'], default_choice=0)

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
    dashboard.Item("data", 0, 3, 12, 3),
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

            with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}):

                # To make this header draggable, we just need to set its classname to 'draggable',
                # as defined above in dashboard.Grid's draggableHandle.
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
                    mui.icon.Radar()
                    mui.Typography("Radar chart", sx={"flex": 1})
                    mui.IconButton(mui.icon.DarkMode)
                # mui.icon.ViewCompact()
                # mui.Typography("Data grid")


                # Like above, we want to make our content grow and shrink as the user resizes the card,
                # by setting flex to 1 and minHeight to 0.

                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This is where we will draw our Bump chart.
                #
                # For this exercise, we can just adapt Nivo's example and make it work with Streamlit Elements.
                # Nivo's example is available in the 'code' tab there: https://nivo.rocks/bump/
                #
                # Data takes a dictionary as parameter, so we need to convert our JSON data from a string to
                # a Python dictionary first, with `json.loads()`.
                #
                # For more information regarding other available Nivo charts:
                # https://nivo.rocks/

                    nivo.Bump(
                        data=json.loads(st.session_state.data),
                        colors={ "scheme": "spectral" },
                        lineWidth=3,
                        activeLineWidth=6,
                        inactiveLineWidth=3,
                        inactiveOpacity=0.15,
                        pointSize=10,
                        activePointSize=16,
                        inactivePointSize=0,
                        pointColor={ "theme": "background" },
                        pointBorderWidth=3,
                        activePointBorderWidth=3,
                        pointBorderColor={ "from": "serie.color" },
                        axisTop={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "",
                            "legendPosition": "middle",
                            "legendOffset": -36
                        },
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "",
                            "legendPosition": "middle",
                            "legendOffset": 32
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "ranking",
                            "legendPosition": "middle",
                            "legendOffset": -40
                        },
                        margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                        axisRight=None,
                    )

            with mui.Card(key="data", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}):
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
                    mui.icon.Radar()
                    mui.Typography("data", sx={"flex": 1})
                    mui.IconButton(mui.icon.DarkMode)

                    DEFAULT_COLUMNS = [
                        { "field": 'id', "headerName": 'ID', "width": 90 },
                        { "field": 'firstName', "headerName": 'First name', "width": 150, "editable": True, },
                        { "field": 'lastName', "headerName": 'Last name', "width": 150, "editable": True, },
                        { "field": 'age', "headerName": 'Age', "type": 'number', "width": 110, "editable": True, },
                    ]

                    DEFAULT_ROWS = [
                        { "id": 1, "lastName": 'Snow', "firstName": 'Jon', "age": 35 },
                        { "id": 2, "lastName": 'Lannister', "firstName": 'Cersei', "age": 42 },
                        { "id": 3, "lastName": 'Lannister', "firstName": 'Jaime', "age": 45 },
                        { "id": 4, "lastName": 'Stark', "firstName": 'Arya', "age": 16 },
                        { "id": 5, "lastName": 'Targaryen', "firstName": 'Daenerys', "age": None },
                        { "id": 6, "lastName": 'Melisandre', "firstName": None, "age": 150 },
                        { "id": 7, "lastName": 'Clifford', "firstName": 'Ferrara', "age": 44 },
                        { "id": 8, "lastName": 'Frances', "firstName": 'Rossini', "age": 36 },
                        { "id": 9, "lastName": 'Roxie', "firstName": 'Harvey', "age": 65 },
                    ]

                    # with mui.Box(sx={"flex": 1, "minHeight": 0}):
                with mui.Box(sx={"flex": 1, "minHeight": 0}):
                    mui.DataGrid(
                        columns=DEFAULT_COLUMNS,
                        rows=DEFAULT_ROWS,
                        pageSize=5,
                        rowsPerPageOptions=[5],
                        checkboxSelection=True,
                        disableSelectionOnClick=True,
                        onCellEditCommit=True,
                    )

elif tabs == 'Money':
    st.title("Paper")
    st.write('Name of option is {}'.format(tabs))

elif tabs == 'Economy':
    st.title("Tom")
    st.write('Name of option is {}'.format(tabs))