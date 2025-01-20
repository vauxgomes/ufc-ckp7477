# Libs
import pandas as pd
from flask import Flask, render_template, request
from module.tfidf import TFIDF

# App
app = Flask(__name__)

# TF-IDF
tfidf = TFIDF('./data')
tfidf.load()

# Documents
df = pd.read_csv('./files/documents.csv')
df = df.dropna().reset_index(drop=True)

# Index route
@app.route("/", methods=["GET", "POST"])
def index():
  results = []
  term = ""
  
  # Search config
  top = 10
  all = True

  #
  if request.method == "POST":
    term = request.form.get("term").lower()
    
    if term:
      top = int(request.form.get("top"))
      all = request.form.get("all")
              
      scores = tfidf.tfidf(term, all=all)[:top]
      
      for score, document_id in scores:
        results.append({
          "document_id": document_id,
          "document_text": df.iloc[document_id].text,
          "score": score
        })

  return render_template("index.html", results=results, term=term, top=top, all=all)

# Main
if __name__ == "__main__":
    app.run(debug=True)