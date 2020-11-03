from flask import Flask, render_template, request
from scrapper import get_jobs

app = Flask("SuperScrapper")
db = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<username>")
def contact(username):
    return f"hello my name is {username}"


@app.route("/report")
def report():
    if request.args.get("word"):
        word = request.args.get("word").lower()
        from_db = db.get(word)
        if from_db:
            jobs = from_db
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")

    return render_template(
        "report.html", searchingby=word, resultNums=len(jobs), jobs=jobs
    )


app.run()