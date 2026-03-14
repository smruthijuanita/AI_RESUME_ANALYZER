import networkx as nx
import plotly.graph_objects as go


def build_skill_graph(role, skills, missing):

    G = nx.Graph()

    for s in skills:
        G.add_edge(role, s)

    for m in missing:
        G.add_edge(role, m)

    pos = nx.spring_layout(G)

    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)

        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines'
    )

    node_x = []
    node_y = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=list(G.nodes())
    )

    fig = go.Figure(data=[edge_trace, node_trace])

    return fig