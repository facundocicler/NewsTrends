import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_alerts(df_alert, topic_arn=None):
    if df_alert.empty:
        print("No hay alertas que enviar.")
        return

    if not topic_arn:
        print("Debes proporcionar un ARN de SNS válido.")
        return

    try:
        sns = boto3.client("sns", region_name="us-east-2")

        top_alerts = df_alert.sort_values(by="alert_score", ascending=False).head(5)

        titles = []
        for _, row in top_alerts.iterrows():
            title = row.get("title", "Sin título")
            score = row.get("alert_score", 0)
            url = row.get("url", "URL no disponible")
            titles.append(f"• {title} (score: {score})\n{url}")

        message = "🔔 ALERTA DE NOTICIAS PRIORITARIAS 🔔\n\n" + "\n\n".join(titles)

        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="🚨 Alertas Prioritarias | Política, Economía, Seguridad y Temas Sociales"
        )
        print("✅ Alerta enviada correctamente a SNS.")

    except (BotoCoreError, ClientError) as e:
        print(f"❌ Error al enviar alerta por SNS: {e}")