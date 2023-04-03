import dash as dbc
from dash_extensions.enrich import html, dcc, Output, Input, DashProxy
import dash_mantine_components as dmc
from dash_extensions import WebSocket

# Client-side function (for performance) that updates the graph.
def update_graph_js(axis):
    ret = """function(msg) {
    if(!msg){return {};}  // no data, just return
    const data = JSON.parse(msg.data);  // read the data
    return {data: [{y: data[%s], type: "scatter"}]}};  // plot the data
    """% (axis)
    return ret

# Create small example app.
app = DashProxy(__name__)


app.layout = html.Div([
    WebSocket(id="ws", url="ws://localhost:5000/objects"),
    WebSocket(id="ws-camera", url="ws://localhost:5000/camera"),
    dmc.Grid(children=[
        dmc.Col(dcc.Graph(id="graph-x"),span=6),
        dmc.Col(dcc.Graph(id="graph-y"),span=6),
        dmc.Col(html.Img(id="video-stream", style={"background-color": "red",'width': '100%'}), span=4)
    ]),
])

# app.clientside_callback(update_position, Output("testing", "children"), Input("ws", "message"))
app.clientside_callback(update_graph_js(1), Output("graph-x", "figure"), Input("ws", "message"))
app.clientside_callback(update_graph_js(0), Output("graph-y", "figure"), Input("ws", "message"))

app.clientside_callback("function(m){return m? m.data : '';}", Output("video-stream", "src"), Input("ws-camera", "message"))

def start_dashboard():
    app.run_server()

if __name__ == "__main__":
    start_dashboard()
