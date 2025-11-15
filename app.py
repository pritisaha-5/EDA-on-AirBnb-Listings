# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 


# %%
df=pd.read_csv("Sample_data.csv")

# %%
df

# %%
df.columns

# %% [markdown]
# # Check for Missing Values

# %%
print(df.isnull().sum())

# %%
df.info()

# %% [markdown]
# # Handling Missing Values

# %%
df['last review']=pd.to_datetime(df['last review'],errors='coerce')
df.info()

# %%
df.fillna({'reviews per month':0,'last review':df['last review'].min()},inplace =True)

# %%
df.dropna(subset=['NAME','host name'],inplace=True)
print(df.isnull().sum())

# %%
df=df.drop(columns=["license","house_rules"],errors='ignore')

# %%
df.head()

# %%
df['price']=df['price'].replace('[\$,]','',regex=True).astype(float)
df['service fee']=df['service fee'].replace('[\$,]','',regex=True).astype(float)

# %%
df.head()

# %% [markdown]
# # Remove Duplicates

# %%
df.drop_duplicates(inplace=True)

# %%
df.info()

# %% [markdown]
# # Statistics

# %%
df.describe()

# %%
import matplotlib .pyplot as plt
import seaborn as sns
plt.figure(figsize=(10,6))
sns.histplot(df['price'],bins=50,kde=True,color='blue')
plt.title('Distribution of Listing Prices')
plt.xlabel('Price($)')
plt.ylabel('Frequency')
plt.show()

# %%
plt.figure(figsize=(8,5))
sns.countplot(x='room type',data=df,color='red')
plt.title('Room Type Distribution')
plt.xlabel('Room Type')
plt.ylabel('Count')
plt.show()

# %%
plt.figure(figsize=(12,8))
sns.countplot(y='neighbourhood group',data=df,color='lightgreen',order=df['neighbourhood group'].value_counts().index)
plt.title('Number of Listings by Neighbourhood Group')
plt.xlabel('Count')
plt.ylabel('Neighbourhood Group')
plt.show()

# %%
plt.figure(figsize=(10,6))
sns.boxplot(x='room type',y='price',hue='room type',data=df,palette='Set1')
plt.title('Price vs. Room Type')
plt.xlabel('Room Type')
plt.ylabel('Price ($)')
plt.legend(title='Room Type')
plt.show()

# %%
df.head()

# %%
df['last review']=pd.to_datetime(df['last review'])
reviews_over_time=df.groupby(df['last review'].dt.to_period('M')).size()
plt.figure(figsize=(12,6))
reviews_over_time.plot(kind='line',color='red')
plt.title('Number of Reviews Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Reviews')
plt.show()

# %%



