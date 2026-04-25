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
        user_input = request.form["question"]

        # تحويل السؤال
        user_vec = vectorizer.transform([user_input])

        # حساب التشابه
        similarities = cosine_similarity(user_vec, X)
        best_match = similarities.argmax()

        # شرط: إذا التشابه ضعيف
        if similarities[0][best_match] < 0.2:
            result = "❌ Je n'ai pas compris votre question."
        else:
            result = answers[best_match]

    return render_template("index.html", result=result)

if name == "__main__":
    app.run(debug=True)
