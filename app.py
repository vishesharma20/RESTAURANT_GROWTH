import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    width: 260px !important;
}

section[data-testid="stSidebar"] > div {
    width: 260px !important;
}
</style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv("Restaurant_Growth_Final.csv")

# # Load models
# scaler = pickle.load(open("scaler.pkl","rb"))
# pca = pickle.load(open("pca.pkl","rb"))
# kmeans = pickle.load(open("kmeans.pkl","rb"))

st.title("Restaurant Growth Potential Dashboard")

# Dashboard filters
st.sidebar.header("Filters")

subregion = st.sidebar.multiselect(
    "Subregion",
    df["Subregion"].unique(),
    default=df["Subregion"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[
    (df["Subregion"].isin(subregion))
    &
    (df["Segment"].isin(segment))
]

# KPI cards
col1,col2,col3,col4=st.columns(4)

col1.metric(
    "Total Restaurants",
    len(filtered_df)
)

col2.metric(
    "Average GPI",
    round(filtered_df["GPI"].mean(),2)
)

col3.metric(
    "Average Orders",
    round(filtered_df["MonthlyOrders"].mean())
)

col4.metric(
    "Expansion Ready",
    len(filtered_df[
        filtered_df["Recommendation"]=="Expand"
    ])
)

# Charts
st.subheader("Restaurant Cluster Distribution")

fig1=px.histogram(
    filtered_df,
    x="ClusterLabel"
)

st.plotly_chart(fig1)

st.subheader("Growth Potential Distribution")

fig2=px.histogram(
    filtered_df,
    x="GPI"
)

st.plotly_chart(fig2)

# Top restaurants
st.subheader("Top Restaurants")

top=filtered_df.sort_values(
    by="GPI",
    ascending=False
)

st.dataframe(
    top[
        [
            "RestaurantName",
            "CuisineType",
            "ClusterLabel",
            "GPI",
            "Recommendation"
        ]
    ].head(10)
)

# =========================
# Prediction section
# =========================

# ==========================
# Prediction Inputs Sidebar
# ==========================

st.sidebar.markdown("---")
st.sidebar.header("Predict New Restaurant")

growth = st.sidebar.number_input(
    "Growth Factor",
    value=1.03
)

aov = st.sidebar.number_input(
    "Average Order Value",
    value=40.0
)

orders = st.sidebar.number_input(
    "Monthly Orders",
    value=1200
)

instore = st.sidebar.slider(
    "InStore Share",
    0.0,
    1.0,
    0.2
)

ue = st.sidebar.slider(
    "UberEats Share",
    0.0,
    1.0,
    0.5
)

dd = st.sidebar.slider(
    "DoorDash Share",
    0.0,
    1.0,
    0.2
)

sd = st.sidebar.slider(
    "Self Delivery Share",
    0.0,
    1.0,
    0.1
)


# ==========================
# Prediction Results
# ==========================

if st.sidebar.button("Predict Restaurant"):

    score = (
        (growth*20)
        + (aov/2)
        + (orders/100)
        + (sd*50)
        - (ue*20)
    )

    if score > 80:
        cluster = "Scalable Self Delivery Leader"
        recommendation = "Expand"

    elif score > 55:
        cluster = "High Growth Aggregator Driven"
        recommendation = "Optimize"

    else:
        cluster = "Stable Local Performer"
        recommendation = "Stabilize"

    st.success(
        f"Predicted Cluster: {cluster}"
    )

    st.info(
        f"Recommendation: {recommendation}"
    )