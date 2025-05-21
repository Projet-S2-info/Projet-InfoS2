from flask import Flask, jsonify, send_from_directory
import requests
from textblob import TextBlob
from datetime import datetime, timedelta

# === Configuration ===
application = Flask(__name__, static_folder='../static', static_url_path='')

#CLÉ_API_NEWS = 'b741529903424b0ca280b6e9d8f7c32d'  
CLÉ_API_NEWS = '30e339ad3f2b4a3799305f9cdeb8ae54'
ENTREPRISES = ['Google', 'Apple', 'Facebook', 'Amazon', 'Microsoft', 'Tesla']

# === Analyse de sentiment (score numérique seulement) ===
def score_sentiment(texte):
    blob = TextBlob(texte)
    return blob.sentiment.polarity

# === Calcul du score total depuis 5 articles ===
def calculer_score_global(articles):
    score_total = sum(score_sentiment(article['title'] + " " + article['description']) for article in articles)
    return round(score_total, 2)

# === Calcul dynamique des cotes ===
def calculer_cotes(score):
    # Transforme le score en probabilités comprises entre 0.1 et 0.9
    proba_hausse = 0.5 + (score / 10)
    proba_hausse = min(max(proba_hausse, 0.1), 0.9)
    
    cote_hausse = round(1 / proba_hausse, 2)
    cote_baisse = round(1 / (1 - proba_hausse), 2)
    
    return cote_hausse, cote_baisse

# === Routes ===
@application.route('/')
def accueil():
    return send_from_directory(application.static_folder, 'index.html')

@application.route('/api/actualites-entreprises')
def actualites_entreprises():
    resultats = {}
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for entreprise in ENTREPRISES:
        url = (
            f'https://newsapi.org/v2/everything?q={entreprise}'
            f'&language=en&from={yesterday}&sortBy=publishedAt&apiKey={CLÉ_API_NEWS}'
        )
        réponse = requests.get(url)
        print(f"NewsAPI response for {entreprise}: {réponse.status_code}, {réponse.json()}")
        données = réponse.json()
        articles = données.get('articles', [])[:5]

        # Score global sentiment sur les 5 articles
        score_global = calculer_score_global(articles)

        # Cotes dynamiques
        cote_hausse, cote_baisse = calculer_cotes(score_global)

        resultats[entreprise] = {
            'articles': articles,
            'score_sentiment': score_global,
            'cotes': {
                'hausse': cote_hausse,
                'baisse': cote_baisse
            }
        }

    return jsonify(resultats)

if __name__ == '__main__':
    #Temporarily disable Flask’s debug mode to avoid the reloader conflict
    #application.run(debug=True)
    application.run(debug=False)
