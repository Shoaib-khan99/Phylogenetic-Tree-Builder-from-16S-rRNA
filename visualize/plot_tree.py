#!/usr/bin/env python
import plotly.graph_objects as go
from ete3 import Tree
import pandas as pd
import re

# Load trees
NJ_TREE = "../results/tree_nj.newick"
ML_TREE = "../results/ml_tree/silva_ml.treefile"

def parse_ete_tree(tree_file):
    t = Tree(tree_file)
    # Extract taxonomy from SILVA labels: e.g., Bacteria;Proteobacteria;Gammaproteobacteria;...
    for leaf in t:
        label = leaf.name
        parts = label.split(";")
        if len(parts) >= 7:
            leaf.name = parts[6].strip()  # Genus
            leaf.add_feature("phylum", parts[1].strip())
            leaf.add_feature("class", parts[2].strip())
        else:
            leaf.name = label.split()[0]
            leaf.add_feature("phylum", "Unknown")
            leaf.add_feature("class", "Unknown")
    return t

def tree_to_plotly(t, title):
    def get_xy(node, x=0, y=0, dx=1):
        if node.is_leaf():
            return [(x, y, node.name, getattr(node, "phylum", "Unknown"))], x + dx
        else:
            children = node.children
            xs, ys, labels, colors = [], [], [], []
            child_x = x
            for child in children:
                child_data, child_x = get_xy(child, child_x, y - 1, dx / len(children))
                xs.extend([d[0] for d in child_data])
                ys.extend([d[1] for d in child_data])
                labels.extend([d[2] for d in child_data])
                colors.extend([d[3] for d in child_data])
            return [(x, y, "", "")] + list(zip(xs, ys, labels, colors)), child_x

    data, _ = get_xy(t)
    df = pd.DataFrame(data, columns=["x", "y", "label", "phylum"])
    df = df[df["label"] != ""]  # remove internal nodes

    fig = go.Figure()

    # Edges
    for node in t.traverse():
        if not node.is_root():
            parent = node.up
            fig.add_trace(go.Scatter(
                x=[get_x(parent), get_x(node)],
                y=[get_y(parent), get_y(node)],
                mode="lines",
                line=dict(color="gray", width=1),
                hoverinfo="none"
            ))

    # Leaves
    phyla = df["phylum"].unique()
    colors = {p: f"rgb({i*50 % 255}, {i*80 % 255}, {i*120 % 255})" for i, p in enumerate(phyla)}

    for phylum in phyla:
        sub = df[df["phylum"] == phylum]
        fig.add_trace(go.Scatter(
            x=sub["x"], y=sub["y"],
            mode="markers+text",
            name=phylum,
            text=sub["label"],
            textposition="middle right",
            marker=dict(size=8, color=colors[phylum]),
            hovertemplate=f"<b>%{{text}}</b><br>Phylum: {phylum}<extra></extra>"
        ))

    fig.update_layout(
        title=title,
        showlegend=True,
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=800,
        template="simple_white"
    )
    return fig

def get_x(node):
    return sum(1 for _ in node.iter_descendants()) if node.children else 0

def get_y(node):
    return -list(node.get_leaves()).index(node) if node.is_leaf() else 0

# Build trees
t_nj = parse_ete_tree(NJ_TREE)
t_ml = parse_ete_tree(ML_TREE)

fig_nj = tree_to_plotly(t_nj, "16S rRNA Neighbor-Joining Tree (BioPython)")
fig_ml = tree_to_plotly(t_ml, "16S rRNA Maximum Likelihood Tree (IQ-TREE)")

# Save
os.makedirs("../results", exist_ok=True)
fig_nj.write_html("../results/tree_nj_interactive.html")
fig_ml.write_html("../results/tree_ml_interactive.html")
fig_nj.write_image("../results/tree_nj.png")
fig_ml.write_image("../results/tree_ml.png")

print("Interactive trees saved to results/")
