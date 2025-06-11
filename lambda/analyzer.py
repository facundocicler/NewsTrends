import spacy

nlp = spacy.load("es_core_news_sm")

# Palabras clave categorizadas
KEYWORDS = [
    # Política
    "Elecciones", "Presidente", "Congreso", "Senado", "Diputados", "Gobierno", "Ministros", "Coalición",
    "Oposición", "Partidos políticos", "Cristina Fernández de Kirchner", "Alberto Fernández",
    "Mauricio Macri", "Javier Milei", "Milei", "Kirchnerismo", "Macrismo", "Peronismo",

    # Economía
    "Inflación", "Dólar", "Dólar blue", "Peso", "Deuda", "Presupuesto", "Impuestos", "Salarios",
    "Desempleo", "PIB", "Exportaciones", "Importaciones", "Paridad", "Retenciones", "Subsidios",
    "Jubilaciones", "Precios", "AFIP", "ANSES", "INDEC", "Supermercados", "YPF", "Enarsa",

    # Seguridad
    "Seguridad", "Delincuencia", "Policía", "Fuerzas armadas", "Narcotráfico", "Fronteras", "Inseguridad",

    # Sociales
    "Pobreza", "Desigualdad", "Vivienda", "Trabajo"
]

def extract_keywords(text: str) -> list:
    if not isinstance(text, str):
        return []
    doc = nlp(text)
    return list({ent.text for ent in doc.ents if len(ent.text.strip()) > 3})

def count_keyword_matches(text: str, keywords=KEYWORDS) -> int:
    if not isinstance(text, str):
        return 0
    return sum(1 for k in keywords if k.lower() in text.lower())

def detect_alert(text: str, min_score: int = 2) -> bool:
    score = count_keyword_matches(text)
    return score >= min_score

def analyze_dataframe(df):
    df["keywords"] = df["title_clean"].apply(extract_keywords)
    df["alert_score"] = df["title_clean"].apply(count_keyword_matches)
    df["alert"] = df["alert_score"] >= 2  # valor ajustable
    return df