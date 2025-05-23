
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("https://storage.googleapis.com/youtube-analytics_pandas/youtube_dataset.csv")
    df.dropna(inplace=True)
    df['Published_date'] = pd.to_datetime(df['Published_date'])
    df['Engagement'] = df['Like_count'] + df['Comment_Count']
    return df

df = load_data()

st.title("📊 YouTube Channel Analytics Tool")

# --- Line Plot: Views Over Time ---
st.subheader("Views Over Time")
views_over_time = df.groupby(df['Published_date'].dt.to_period('M'))['Views'].sum()
st.line_chart(views_over_time)

# --- Bar Plot: Likes per Video ---
st.subheader("Top 20 Videos by Likes")
likes_per_video = df[['Title', 'Like_count']].sort_values(by='Like_count', ascending=False).head(20)

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(data=likes_per_video, x='Like_count', y='Title', palette='coolwarm', ax=ax1)
ax1.set_title('Top 20 Videos by Likes')
st.pyplot(fig1)

# --- Scatter Plot: Views vs Likes ---
st.subheader("Views vs Likes")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x='Views', y='Like_count', ax=ax2)
ax2.set_title("Views vs Likes")
st.pyplot(fig2)

# --- Optional: Top Channels ---
st.subheader("Top Channels by Total Views")
top_channels = df.groupby('Channel_Name')['Views'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_channels)

# Show raw data if needed
if st.checkbox("Show raw data"):
    st.write(df)
