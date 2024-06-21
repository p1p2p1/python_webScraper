from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from web_scraper import web_scraper

#URL 설정
url = {
    "berlin" : "https://berlinstartupjobs.com",
    "wwr" : "https://weworkremotely.com",
    "web3" : "https://web3.career",
}
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

#임시 DB 
db = {}

app = Flask("JobScrapper")

#Search Site Mapping(Route)
@app.route("/")
def home():
    return render_template("home.html", name="yoo")


#Search Result Site Mapping
@app.route("/search")
def search():
    berlin_jobs = []
    wwr_jobs = []
    web3_jobs = []
    keyword = request.args.get("keyword") 
    
    scraper = web_scraper(headers)
    scraper.berlin_web_scrape(url['berlin'], keyword, berlin_jobs)

    scraper.wwr_web_scrape(url['wwr'], keyword, wwr_jobs)

    scraper.web3_web_scrape(url['web3'], keyword, web3_jobs)

    return render_template("search.html", keyword=keyword, berlin_jobs= berlin_jobs, wwr_jobs = wwr_jobs, web3_jobs = web3_jobs)


app.run("0.0.0.0")

