import streamlit as st
import pandas as pd
from pymongo import MongoClient
from collections import Counter
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tendencias en Noticias", layout="wide")
st.title("📰 Noticias en Política, Economía, Seguridad y Sociales")

@st.cache_resource
def get_data():
    mongo_uri = st.secrets["mongo_uri"]
    client = MongoClient(mongo_uri)
    collection = client["news_db"]["news_articles"]
    data = list(collection.find())
    return pd.DataFrame(data)

df = get_data()

st.sidebar.header("⚙️ Filtros")
solo_alertas = st.sidebar.checkbox("🔔 Solo noticias con alerta")
cantidad = st.sidebar.slider("Cantidad de noticias a mostrar", 5, 50, 20)

if solo_alertas and "alert" in df.columns:
    df = df[df["alert"] == True]

st.subheader("Últimas Noticias")
st.dataframe(df[["publishedAt", "title", "keywords"]].sort_values("publishedAt", ascending=False).head(cantidad), use_container_width=True)

st.subheader("📊 Palabras clave más mencionadas")
keywords = df["keywords"].explode().dropna()
top_keywords = Counter(keywords).most_common(10)

if top_keywords:
    labels, values = zip(*top_keywords)
    fig, ax = plt.subplots()
    ax.barh(labels, values, color="skyblue")
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("No hay palabras clave detectadas.")