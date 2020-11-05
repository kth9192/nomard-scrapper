from flask import Flask, render_template, request, send_file
from scrapper import get_jobs
from exporter import save_to_file

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
        existingJob = db.get(word)

        if existingJob:
            jobs = existingJob
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")

    return render_template(
        "report.html", searchingby=word, resultNums=len(jobs), jobs=jobs
    )


@app.route("/export")
def export():
    try:
        word = request.args.get("word").lower()
        if not word:
            raise Exception()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file("jobs.csv")

    except:
        return redirect("/")


app.run()