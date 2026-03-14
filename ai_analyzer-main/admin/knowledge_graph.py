"""Knowledge graph: User -> Resume, User -> Chat, Resume -> VectorDB, Chat -> LLM."""

import networkx as nx
import plotly.graph_objects as go

from db.database import get_all_users, get_all_resumes, get_all_chats


def build_knowledge_graph():
    G = nx.DiGraph()

    # Add LLM and VectorDB as global nodes
    G.add_node("LLM", node_type="system")
    G.add_node("VectorDB", node_type="system")

    users = get_all_users()
    resumes = get_all_resumes()
    chats = get_all_chats()

    user_ids = {r[0]: r[2] for r in users}  # id -> email
    for uid, email in user_ids.items():
        G.add_node(f"User:{email}", node_type="user")

    def user_node(uid):
        email = user_ids.get(uid, f"user_{uid}")
        node = f"User:{email}"
        if node not in G:
            G.add_node(node, node_type="user")
        return node

    for r in resumes:
        rid, uid, file_path, embedding_id, _ = r
        resume_node = f"Resume:{rid}"
        G.add_node(resume_node, node_type="resume")
        G.add_edge(user_node(uid), resume_node)
        G.add_edge(resume_node, "VectorDB")

    for c in chats:
        cid, uid, msg, resp, ts = c
        chat_node = f"Chat:{cid}"
        G.add_node(chat_node, node_type="chat")
        G.add_edge(user_node(uid), chat_node)
        G.add_edge(chat_node, "LLM")

    return G


def render_knowledge_graph():
    G = build_knowledge_graph()
    if G.number_of_nodes() == 0:
        return None

    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    node_x = [pos[n][0] for n in G.nodes()]
    node_y = [pos[n][1] for n in G.nodes()]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=[str(n).replace("User:", "").replace("Resume:", "R").replace("Chat:", "C")[:20] for n in G.nodes()],
        textposition="top center",
        marker=dict(size=12, line=dict(width=2)),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Knowledge Graph: Users, Resumes, Chats, VectorDB, LLM",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )
    return fig
