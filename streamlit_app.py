import streamlit as st
import pandas as pd
import plotly.express as px
APP_TITLE = "News NLP Text Analysis"

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown('''
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1180px;}
[data-testid="stMetricValue"] {font-size: 1.65rem;}
.small-note {color: #5f6368; font-size: 0.92rem;}
</style>
''', unsafe_allow_html=True)


df = pd.read_csv("data/news_metrics_sample.csv")
st.title(APP_TITLE)
st.caption("Sentiment, readability, and editorial quality metrics for scraped article text.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Articles", len(df))
c2.metric("Avg polarity", f"{df.polarity.mean():.2f}")
c3.metric("Avg fog index", f"{df.fog_index.mean():.1f}")
c4.metric("Words analyzed", f"{int(df.word_count.sum()):,}")

left, right = st.columns([1, 1])
with left:
    st.subheader("Sentiment spread")
    fig = px.scatter(df, x="subjectivity", y="polarity", size="word_count", color="fog_index", hover_name="title", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Readability distribution")
    st.plotly_chart(px.histogram(df, x="fog_index", nbins=18), use_container_width=True)

st.subheader("Articles needing editorial review")
review = df.assign(review_priority=(df.fog_index > 14) | (df.polarity < -0.2)).sort_values(["review_priority", "fog_index"], ascending=[False, False])
st.dataframe(review, use_container_width=True, hide_index=True)
