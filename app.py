import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

# ---------------------------------------------------------
#                TITLE & FILE UPLOAD
# ---------------------------------------------------------
st.title("Airbnb Listings EDA Dashboard")

uploaded_file = st.file_uploader("Upload your Airbnb Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

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
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True)
    st.pyplot()

    # Room Type Countplot
    st.subheader("Room Type Distribution")
    plt.figure(figsize=(8, 5))
    sns.countplot(x='room type', data=df)
    st.pyplot()

    # Neighbourhood Group
    st.subheader("Number of Listings by Neighbourhood Group")
    plt.figure(figsize=(12, 8))
    sns.countplot(y='neighbourhood group',
                  data=df,
                  order=df['neighbourhood group'].value_counts().index)
    st.pyplot()

    # Box Plot: Price vs Room Type
    st.subheader("Price vs Room Type")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='room type', y='price', data=df)
    st.pyplot()

    # Reviews Over Time
    st.subheader("Number of Reviews Over Time")
    df['last review'] = pd.to_datetime(df['last review'])
    reviews_over_time = df.groupby(df['last review'].dt.to_period('M')).size()
    plt.figure(figsize=(12, 6))
    reviews_over_time.plot(kind='line')
    st.pyplot()

else:
    st.info("Please upload a CSV file to start the EDA.")
