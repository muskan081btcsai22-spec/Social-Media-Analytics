import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from pyvis.network import Network
import os


def build_network(posts):
    G = nx.DiGraph()
    for post in posts:
        u = post['username']
        for mention in post.get('mentions', []):
            G.add_edge(u, mention)

    top_nodes = sorted(G.in_degree(), key=lambda x: x[1], reverse=True)[:10]

    communities = []
    if G.number_of_nodes() > 0:
        try:
            communities = list(greedy_modularity_communities(G.to_undirected()))
        except Exception:
            communities = []

    # Save interactive graph
    net = Network(height='500px', width='100%', bgcolor='#1a1a2e', font_color='white', directed=True)
    net.from_nx(G)
    viz_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'network_viz.html')
    net.save_graph(viz_path)

    return {
        'top_nodes': [{'username': n, 'mentions': c} for n, c in top_nodes],
        'num_communities': len(communities),
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
    }
