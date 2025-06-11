from cleaner import clean_articles
from analyzer import analyze_dataframe
from pymongo import MongoClient
from notifier import send_alerts
import requests
import json

def lambda_handler(event, context):
    with open("config.json") as f:
        config = json.load(f)

    url = f"https://gnews.io/api/v4/top-headlines?country={config['country']}&lang={config['lang']}&max=100&apikey={config['api_key']}"
    articles = requests.get(url).json().get("articles", [])

    if not articles:
        return {"message": "No se encontraron artículos."}
    
    df = clean_articles(articles)
    df = analyze_dataframe(df)

    client = MongoClient(config["mongo_uri"])
    collection = client["news_db"]["news_articles"]
    collection.create_index("url", unique=True)

    inserted_count = 0
    for article in df.to_dict(orient="records"):
        result = collection.update_one(
            {"url": article["url"]},
            {"$setOnInsert": article},
            upsert=True
        )
        if result.upserted_id:
            inserted_count += 1

    alert_df = df[df["alert"] == True]
    if not alert_df.empty:
        topic_arn = config.get('sns_topic_arn')
        if topic_arn:
            send_alerts(alert_df, topic_arn)
        else:
            print("No se encontró el ARN del topic SNS en config.json.")
    else:
        print("No se detectaron alertas relevantes.")

    return {"message": f"Insertados {inserted_count} nuevos artículos"}