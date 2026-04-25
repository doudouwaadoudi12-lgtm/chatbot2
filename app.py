from flask import Flask, render_template, request
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# تحميل البيانات
with open("faq.json", "r", encoding="utf-8") as f:
    data = json.load(f)

questions = list(data.keys())
answers = list(data.values())

# TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    
    if request.method == "POST":
        user_input = request.form.get("question", "")

        if user_input.strip() != "":
            user_vec = vectorizer.transform([user_input])
            similarities = cosine_similarity(user_vec, X)
            best_match = similarities.argmax()

            if similarities[0][best_match] < 0.2:
                result = "❌ Je n'ai pas compris votre question."
            else:
                result = answers[best_match]

    return render_template("index.html", result=result)


# مهم جداً ✔️
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)