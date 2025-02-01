# Libs
import pandas as pd
from module.tfidf import TFIDF
from flask import Flask, render_template, request

from wordcloud import WordCloud, STOPWORDS
import base64
from io import BytesIO
from PIL import Image

# App
app = Flask(__name__)

# TF-IDF
tfidf = TFIDF('./data')
tfidf.load()

# Documents
df = pd.read_csv('./files/documents.csv')
df = df.dropna().reset_index(drop=True).sample(frac=0.6, random_state=42).reset_index(drop=True)

# Index route
@app.route("/", methods=["GET", "POST"])
def index():
  results = []
  terms = ""
  
  # Search config
  top = 10
  all = True
  
  # Image
  img_str = ''

  #
  if request.method == "POST":
    terms = request.form.get("terms").lower()
    terms = [term.strip() for term in terms.split(';')]

    if len(terms) > 0:
      top = int(request.form.get("top"))
      all = request.form.get("all")
      documents = []

      for term in terms:
        search = tfidf.tfidf(term, all=all)
        scores = search[:top]
      
        # For each search feedback
        for score, document_id in scores:
          results.append({
            "document_id": document_id,
            "document_text": df.iloc[document_id].text,
            "score": score,
            "term": term
          })
        
          documents.append(df.iloc[document_id].text)
      
      # Resorting
      results = sorted(results, key=lambda item: item['score'], reverse=True)

      # Wordcloud
      wc = WordCloud(
        max_words=200, stopwords=set(STOPWORDS),
        width=1296, height=550,
        min_font_size=4, max_font_size=150,
        mode='RGBA', background_color=None
      )
      
      #
      wc.generate(' '.join(documents))
      wc.to_file("images/nuvem.png")
      
      #
      img = Image.open("images/nuvem.png")
      
      # Converting to base64
      buffered = BytesIO()
      img.save(buffered, format="PNG") # Escolha o formato adequado
      img_str = base64.b64encode(buffered.getvalue()).decode()

  return render_template("index.html", results=results, terms='; '.join(terms), top=top, all=all, img_str=img_str)

# Main
if __name__ == "__main__":
    app.run(debug=True)