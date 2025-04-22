from flask import Flask, jsonify, send_from_directory
import requests
from textblob import TextBlob
from datetime import datetime, timedelta

# === Configuration ===
application = Flask(__name__, static_folder='../static', static_url_path='')

CLÉ_API_NEWS = 'b741529903424b0ca280b6e9d8f7c32d'  # Remplace par ta vraie clé
ENTREPRISES = ['Google', 'Apple', 'Facebook', 'Amazon', 'Microsoft', 'Tesla']


# === Analyse de sentiment ===
def analyser_sentiment(texte):
    blob = TextBlob(texte)
    polarité = blob.sentiment.polarity
    if polarité >= 0.3:
        return 'très positif'
    elif 0.1 <= polarité < 0.3:
        return 'légèrement positif'
    elif -0.3 <= polarité < -0.1:
        return 'légèrement négatif'
    elif polarité <= -0.3:
        return 'très négatif'
    else:
        return 'neutre'


def calculer_variation_depuis_actualites(articles):
    variation = 0
    for article in articles:
        texte = f"{article.get('title', '')} {article.get('description', '')}"
        sentiment = analyser_sentiment(texte)
        if sentiment == 'très positif':
            variation += 3
        elif sentiment == 'légèrement positif':
            variation += 1
        elif sentiment == 'légèrement négatif':
            variation -= 1
        elif sentiment == 'très négatif':
            variation -= 3
    return max(-5, min(5, variation))


# === Route d’accueil : sert index.html ===
@application.route('/')
def accueil():
    return send_from_directory(application.static_folder, 'index.html')


# === API : actualités + sentiment + variation ===
@application.route('/api/actualites-entreprises')
def actualites_entreprises():
    actualites = {}
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for entreprise in ENTREPRISES:
        url = (
            f'https://newsapi.org/v2/everything?'
            f'q={entreprise}&language=fr&from={yesterday}&to={yesterday}&sortBy=publishedAt&apiKey={CLÉ_API_NEWS}'
        )
        réponse = requests.get(url)
        données = réponse.json()
        articles = données.get('articles', [])[:5]

        # Analyse des sentiments et calcul variation
        for article in articles:
            texte = f"{article.get('title', '')} {article.get('description', '')}"
            article['sentiment'] = analyser_sentiment(texte)

        variation = calculer_variation_depuis_actualites(articles)

        actualites[entreprise] = {
            'articles': articles,
            'variation': variation
        }

    return jsonify(actualites)


# === Lancer l'application ===
if __name__ == '__main__':
    print(">>> Serveur Flask en cours de démarrage...")
    application.run(debug=True)
