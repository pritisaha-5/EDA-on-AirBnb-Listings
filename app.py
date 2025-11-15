import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Airbnb Listings EDA Dashboard")

# ---------------------------------------------------------
#         LOAD DATASET FROM GITHUB AUTOMATICALLY
# ---------------------------------------------------------

github_url = "https://raw.githubusercontent.com/pritisaha-5/EDA-on-AirBnb-Listings/refs/heads/main/Sample_data.csv"

st.write("### Loading Dataset from GitHub...")
try:
    df = pd.read_csv(github_url)
    st.success("Dataset Loaded Successfully from GitHub!")
except:
    st.error("❌ Failed to load dataset. Check GitHub link.")
    st.stop()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# ---------------------------------------------------------
#                CHECK MISSING VALUES
# ---------------------------------------------------------
st.subheader("Missing Values")
st.write(df.isnull().sum())

# ---------------------------------------------------------
#                DATA CLEANING
# ---------------------------------------------------------
st.subheader("Data Cleaning")

df['last review'] = pd.to_datetime(df['last review'], errors='coerce')
df.fillna({'reviews per month': 0, 'last review': df['last review'].min()}, inplace=True)
df.dropna(subset=['NAME', 'host name'], inplace=True)

df = df.drop(columns=["license", "house_rules"], errors='ignore')

# price formatting
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
df['service fee'] = df['service fee'].replace('[\$,]', '', regex=True).astype(float)

df.drop_duplicates(inplace=True)

st.success("Data Cleaning Completed!")
st.dataframe(df.head())

# ---------------------------------------------------------
#                DESCRIPTIVE STATISTICS
# ---------------------------------------------------------
st.subheader("Statistical Summary")
st.write(df.describe())

# ---------------------------------------------------------
#                VISUALIZATIONS
# ---------------------------------------------------------
st.header("Visualizations")

# Price Distribution
st.subheader("Distribution of Listing Prices")
fig1 = plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=50, kde=True)
st.pyplot(fig1)

# Room Type Countplot
st.subheader("Room Type Distribution")
fig2 = plt.figure(figsize=(8, 5))
sns.countplot(x='room type', data=df)
st.pyplot(fig2)

# Neighbourhood Group
st.subheader("Number of Listings by Neighbourhood Group")
fig3 = plt.figure(figsize=(12, 8))
sns.countplot(
    y='neighbourhood group',
    data=df,
    order=df['neighbourhood group'].value_counts().index
)
st.pyplot(fig3)

# Box Plot: Price vs Room Type
st.subheader("Price vs Room Type")
fig4 = plt.figure(figsize=(10, 6))
sns.boxplot(x='room type', y='price', data=df)
st.pyplot(fig4)

# Reviews Over Time
st.subheader("Number of Reviews Over Time")
df['last review'] = pd.to_datetime(df['last review'])
reviews_over_time = df.groupby(df['last review'].dt.to_period('M')).size()

fig5 = plt.figure(figsize=(12, 6))
reviews_over_time.plot(kind='line')
st.pyplot(fig5)
