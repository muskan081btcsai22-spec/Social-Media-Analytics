import networkx as nx

def detect_influencers(posts, top_n=10):
    G = nx.DiGraph()

    # Build graph
    for post in posts:
        user = post.get('username')
        mentions = post.get('mentions', [])

        for m in mentions:
            G.add_edge(user, m)

    # If graph is empty, return empty
    if G.number_of_nodes() == 0:
        return []

    # Try eigenvector centrality (better influence measure)
    try:
        centrality = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        # fallback if it fails
        centrality = nx.degree_centrality(G)

    # Sort users by influence
    ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Format output
    return [
        {
            'rank': i + 1,
            'username': user,
            'score': round(score, 4)
        }
        for i, (user, score) in enumerate(ranked)
    ]