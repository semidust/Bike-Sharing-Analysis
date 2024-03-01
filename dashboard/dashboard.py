import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="dark")

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.resample(rule="M", on="dateday").agg({
        "count": "sum"
    }).reset_index()

    return monthly_rentals_df

def create_weekly_rentals_df(df):
    # mengurutkan hari
    day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    df["weekday"] = pd.Categorical(df["weekday"], categories=day_order, ordered=True)

    weekly_rentals_df = df.groupby(by="weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    }).reset_index()

    return weekly_rentals_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").agg({
        "count": "sum"
    }).reset_index()

    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weather").agg({
        "count": "sum"
    }).reset_index()

    return byweather_df

# load data
df = pd.read_csv("https://raw.githubusercontent.com/semidust/bike-sharing-analysis/main/dashboard/cleaned_day.csv")
df.reset_index(inplace=True)

df["dateday"] = pd.to_datetime(df["dateday"])

# komponen filter
min_date = df["dateday"].min()
max_date = df["dateday"].max()

with st.sidebar:
    st.image("https://github.com/semidust/bike-sharing-analysis/blob/main/dashboard/logo.png?raw=true")

    start_date, end_date = st.date_input(
        label="Time Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dateday"] >= str(start_date)) &
             (df["dateday"] <= str(end_date))]

monthly_rentals_df = create_monthly_rentals_df(main_df)
weekly_rentals_df = create_weekly_rentals_df(main_df)
byseason_df = create_byseason_df(main_df)
byweather_df = create_byweather_df(main_df)

st.title("Bike Sharing Dashboard :star:")
st.divider()

# total counts
col1, col2, col3 = st.columns(3)

with col1:
    registered_counts = weekly_rentals_df["registered"].sum()
    st.metric("Registered Users", value="{:,}".format(registered_counts))

with col2:
    casual_counts = weekly_rentals_df["casual"].sum()
    st.metric("Casual Users", value="{:,}".format(casual_counts))

with col3:
    total_counts = weekly_rentals_df["count"].sum()
    st.metric("Total Users", value="{:,}".format(total_counts))

st.divider()

# monthly rentals
st.header(":blue[Monthly Rentals]")

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(
    data=monthly_rentals_df,
    x="dateday",
    y="count",
    marker="o",
    linewidth=2,
    color="#72BCD4",
    ax=ax
)
plt.xlabel(None)
plt.ylabel(None)

st.pyplot(fig)

# weekly rentals
st.header(":blue[Weekly Rentals]")
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    x=weekly_rentals_df["weekday"],
    y=weekly_rentals_df["registered"],
    label="registered",
    linewidth=0,
    errorbar=None,
    color="#72BCD4",
    ax=ax
)

sns.barplot(
    x=weekly_rentals_df["weekday"],
    y=weekly_rentals_df["casual"],
    label="casual",
    linewidth=0,
    errorbar=None,
    color="#D3D3D3",
    ax=ax
)

plt.xlabel(None)
plt.ylabel(None)
plt.legend()
st.pyplot(fig)

# by weather and season
st.header(":blue[Rental Counts by Weather and Season]")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        data=byseason_df,
        x="season",
        y="count",
        palette=colors,
        errorbar=None,
        linewidth=0,
        ax=ax
    )
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.title("Number of Rentals by Season", loc="center", fontsize=30)
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        data=byweather_df,
        x="weather",
        y="count",
        palette=colors,
        errorbar=None,
        linewidth=0,
        ax=ax
    )
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.title("Number of Rentals by Weather", loc="center", fontsize=30)
    plt.xlabel(None)
    plt.ylabel(None)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    st.pyplot(fig)

st.caption("Copyright © 2024 [Sammytha](https://github.com/semidust)")
