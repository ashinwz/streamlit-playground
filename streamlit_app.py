# First, we will need the following imports for our application.

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
    tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'], 
                         iconName=['dashboard', 'money', 'economy'], default_choice=0)

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

    # Create a new dashboard with the layout specified above.
    #
    # draggableHandle is a CSS query selector to define the draggable part of each dashboard item.
    # Here, elements with a 'draggable' class name will be draggable.
    #
    # For more information on available parameters for dashboard grid:
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

        with dashboard.Grid(layout, draggableHandle=".draggable"):

        # First card, the code editor.
        #
        # We use the 'key' parameter to identify the correct dashboard item.
        #
        # To make card's content automatically fill the height available, we will use CSS flexbox.
        # sx is a parameter available with every Material UI widget to define CSS attributes.
        #
        # For more information regarding Card, flexbox and sx:
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/

            with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}):

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
                    mui.icon.PieChart()
                    mui.Typography("Radar chart", sx={"flex": 1})
                    mui.IconButton(mui.icon.DarkMode)

                # We want to make card's content take all the height available by setting flex CSS value to 1.
                # We also want card's content to shrink when the card is shrinked by setting minHeight to 0.

                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                    # Here is our Monaco code editor.
                    #
                    # First, we set the default value to st.session_state.data that we initialized above.
                    # Second, we define the language to use, JSON here.
                    #
                    # Then, we want to retrieve changes made to editor's content.
                    # By checking Monaco documentation, there is an onChange property that takes a function.
                    # This function is called everytime a change is made, and the updated content value is passed in
                    # the first parameter (cf. onChange: https://github.com/suren-atoyan/monaco-react#props)
                    #
                    # Streamlit Elements provide a special sync() function. This function creates a callback that will
                    # automatically forward its parameters to Streamlit's session state items.
                    #
                    # Examples
                    # --------
                    # Create a callback that forwards its first parameter to a session state item called "data":
                    # >>> editor.Monaco(onChange=sync("data"))
                    # >>> print(st.session_state.data)
                    #
                    # Create a callback that forwards its second parameter to a session state item called "ev":
                    # >>> editor.Monaco(onChange=sync(None, "ev"))
                    # >>> print(st.session_state.ev)
                    #
                    # Create a callback that forwards both of its parameters to session state:
                    # >>> editor.Monaco(onChange=sync("data", "ev"))
                    # >>> print(st.session_state.data)
                    # >>> print(st.session_state.ev)
                    #
                    # Now, there is an issue: onChange is called everytime a change is made, which means everytime
                    # you type a single character, your entire Streamlit app will rerun.
                    #
                    # To avoid this issue, you can tell Streamlit Elements to wait for another event to occur
                    # (like a button click) to send the updated data, by wrapping your callback with lazy().
                    #
                    # For more information on available parameters for Monaco:
                    # https://github.com/suren-atoyan/monaco-react
                    # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

                    editor.Monaco(
                        defaultValue=st.session_state.data,
                        language="json",
                        onChange=lazy(sync("data"))
                    )

                with mui.CardActions:

                    # Monaco editor has a lazy callback bound to onChange, which means that even if you change
                    # Monaco's content, Streamlit won't be notified directly, thus won't reload everytime.
                    # So we need another non-lazy event to trigger an update.
                    #
                    # The solution is to create a button that fires a callback on click.
                    # Our callback doesn't need to do anything in particular. You can either create an empty
                    # Python function, or use sync() with no argument.
                    #
                    # Now, everytime you will click that button, onClick callback will be fired, but every other
                    # lazy callbacks that changed in the meantime will also be called.

                    mui.Button("Apply changes", onClick=sync())

            # Second card, the Nivo Bump chart.
            # We will use the same flexbox configuration as the first card to auto adjust the content height.

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

            # Third element of the dashboard, the Media player.

            with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}):

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
                    mui.Typography("Media", sx={"flex": 1})
                    mui.IconButton(mui.icon.DarkMode)
                    # This element is powered by ReactPlayer, it supports many more players other
                    # than YouTube. You can check it out there: https://github.com/cookpete/react-player#props
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    media.Player(url=media_url, width="100%", height="100%", controls=True)

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