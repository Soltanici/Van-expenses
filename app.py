import pandas as pd
import datetime as dt
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Vans expenses",
                   page_icon=":bar_chart:",
                   layout="wide"
)

df = pd.read_excel(
    io="Van expenses.xlsx",
    engine="openpyxl",
    sheet_name="Total",
    skiprows=3,
    usecols="B:H",
    nrows=1000,
)
df



st.sidebar.header("Please filter here: ")

month = st.sidebar.multiselect(
    "Select the month: ",
    options=df["month"].unique(),
    default=df["month"].unique()
)

reg_number = st.sidebar.multiselect(
    "Select the Registration Nr : ",
    options=df["reg_number"].unique(),
    default=df["reg_number"].unique()
)

df_selection = df.query(
    "month == @month & reg_number == @reg_number"
)

st.title(":bar_chart: Van Expenses")
st.markdown("##")

total_expenses = round(df_selection["price"].sum(),2)
average_expenses = round(df_selection["price"].mean(),2)

left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.subheader("Total price: ")
    st.subheader(f"£ {total_expenses}")



with right_column:
    st.subheader("Average expenses: ")
    st.subheader(f"£ {average_expenses}")

st.markdown("---")

price_by_vans = (
    df_selection.groupby(by = ["reg_number"]).sum()[["price"]].sort_values(by=["price"])
)
fig_van_price = px.bar(
    price_by_vans,
    x=price_by_vans.index,
    y="price",
    title="<b>Van Expenses</b>",
    color_discrete_sequence=["#0083B8"] * len(price_by_vans),
    template="plotly_white"
)
fig_van_price.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)

price_by_month = (
    df_selection.groupby(by = ["month"]).sum()[["price"]].sort_values(by=["price"])
)
fig_month_price = px.bar(
    price_by_month,
    x=price_by_month.index,
    y="price",
    title="<b>Total expense by month</b>",
    color_discrete_sequence=["#0083B8"] * len(price_by_month),
    template="plotly_white"
)
fig_month_price.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)


left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_van_price,use_container_width=True)
right_column.plotly_chart(fig_month_price,use_container_width=True)


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
"""

st.markdown(hide_st_style,unsafe_allow_html=True)



