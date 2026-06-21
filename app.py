from pyvis.network import Network
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="GeneRank",
    page_icon="🧬",
    layout="wide"
)

# -----------------------------------
# HEADER
# -----------------------------------

st.title("🧬 GeneRank")
st.subheader("AI-Powered Cancer Biomarker Prioritization Platform")

# -----------------------------------
# LOAD DATA
# -----------------------------------

biomarkers_df = pd.read_csv("biomarkers.csv")
gene_scores_df = pd.read_csv("gene_scores.csv")
interactions_df = pd.read_csv("interactions.csv")
drugs_df = pd.read_csv("datasets_drugs.csv")

biomarkers_df.columns = biomarkers_df.columns.str.strip()
gene_scores_df.columns = gene_scores_df.columns.str.strip()
interactions_df.columns = interactions_df.columns.str.strip()
drugs_df.columns = drugs_df.columns.str.strip()

# -----------------------------------
# INPUTS
# -----------------------------------

st.header("Input Parameters")

disease = st.selectbox(
    "Select Cancer Type",
    biomarkers_df["Disease"].unique()
)

gene_input = st.text_input(
    "Enter Gene Symbol (Optional)",
    ""
)

# -----------------------------------
# DASHBOARD
# -----------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Biomarkers", len(biomarkers_df))

with c2:
    st.metric("Drug Records", len(drugs_df))

with c3:
    st.metric("Gene Interactions", len(interactions_df))

# -----------------------------------
# ANALYSIS
# -----------------------------------

if st.button("🚀 Analyze"):

    # Biomarkers

    disease_biomarkers = biomarkers_df[
        biomarkers_df["Disease"] == disease
    ]

    st.header("🧬 Biomarkers Found")

    st.dataframe(
        disease_biomarkers,
        use_container_width=True
    )

    # Scores

    disease_scores = gene_scores_df[
    gene_scores_df["Disease"] == disease
]
    st.header("📊 Biomarker Relevance Scores")

    st.dataframe(
        disease_scores,
        use_container_width=True
    )

    # Score Chart

    st.subheader("Biomarker Score Visualization")

    chart_data = disease_scores.set_index("Gene")["Score"]

    st.bar_chart(chart_data)

    # Ranking

    ranked = disease_scores.sort_values(
        by="Score",
        ascending=False
    )

    st.header("🏆 Biomarker Ranking")

    st.dataframe(
        ranked,
        use_container_width=True
    )

    # -----------------------------------
    # NETWORK
    # -----------------------------------

    disease_genes = disease_biomarkers["Gene"].tolist()

    network = interaction_df[
        interaction_df["Gene1"].isin(disease_genes)
        |
        interaction_df["Gene2"].isin(disease_genes)
    ]

    st.header("🧬 Gene Interaction Network")

    net = Network(
        height="700px",
        width="100%",
        bgcolor="#222222",
        font_color="white"
    )

    for _, row in network.iterrows():

        net.add_node(
            row["Gene1"],
            label=row["Gene1"]
        )

        net.add_node(
            row["Gene2"],
            label=row["Gene2"]
        )

        net.add_edge(
            row["Gene1"],
            row["Gene2"]
        )

    net.save_graph("network.html")

    with open("network.html", "r", encoding="utf-8") as f:
        html = f.read()

    components.html(html, height=750)

    # -----------------------------------
    # HUB GENE
    # -----------------------------------

    gene_counts = {}

    for _, row in network.iterrows():

        gene_counts[row["Gene1"]] = (
            gene_counts.get(row["Gene1"], 0) + 1
        )

        gene_counts[row["Gene2"]] = (
            gene_counts.get(row["Gene2"], 0) + 1
        )

    if len(gene_counts) > 0:

        hub_gene = max(
            gene_counts,
            key=gene_counts.get
        )

        st.header("⭐ Hub Gene Detection")

        st.success(
            f"Hub Gene: {hub_gene}"
        )

        # Gene Importance

        importance_df = pd.DataFrame(
            gene_counts.items(),
            columns=[
                "Gene",
                "Importance"
            ]
        )

        importance_df = importance_df.sort_values(
            by="Importance",
            ascending=False
        )

        st.header("🌐 Gene Importance Ranking")

        st.dataframe(
            importance_df,
            use_container_width=True
        )

    # -----------------------------------
    # DRUGS
    # -----------------------------------

    drug_result = drugs_df[
        drugs_df["Gene"].isin(disease_genes)
    ]

    st.header("💊 Drug Recommendations")

    st.dataframe(
        drug_result,
        use_container_width=True
    )
