import pandas as pd
import spacy

nlp = spacy.load("es_core_news_sm")

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

def clean_articles(articles: list) -> pd.DataFrame:
    df = pd.DataFrame(articles)
    
    df.drop_duplicates(subset="url", inplace=True)

    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    df["title_clean"] = df["title"].apply(preprocess_text)
    df["description_clean"] = df["description"].apply(preprocess_text)

    return df    