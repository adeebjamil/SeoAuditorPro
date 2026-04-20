from flask import Flask, render_template, request, send_from_directory, abort
from core.scraper import scrape_page
from core.analyzer import analyze_seo
from articles_data import ARTICLES_DB, get_article_by_slug
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/articles', methods=['GET'])
def articles():
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    
    # Filter articles by search query if it exists
    filtered_list = []
    if search_query:
        for article in ARTICLES_DB:
            # Case-insensitive search on title and description
            if (search_query.lower() in article['title'].lower() or 
                search_query.lower() in article['description'].lower() or 
                search_query.lower() in article['content'].lower()):
                filtered_list.append(article)
    else:
        filtered_list = ARTICLES_DB

    # Simple pagination wrapper
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    page_items = filtered_list[start:end]
    total_pages = (len(filtered_list) + per_page - 1) // per_page
    
    return render_template('articles.html', 
                           articles=page_items,
                           page=page, 
                           total_pages=total_pages,
                           search_query=search_query,
                           meta_title="Free SEO Guides & Tutorials (2026) | SEO Auditor Pro",
                           meta_desc="Browse 350+ free technical SEO guides, speed optimization tutorials, and backlink strategies updated for 2026.")

@app.route('/article/<slug>', methods=['GET'])
def article_detail(slug):
    article = get_article_by_slug(slug)
    if not article:
        abort(404)
        
    return render_template('article_detail.html', 
                           article=article,
                           meta_title=f"{article['title']} - SEO Auditor Pro",
                           meta_desc=f"{article['description']}",
                           meta_keys=f"SEO, {article['title']}, 2026 SEO guide")

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy.html', meta_title="Privacy Policy | SEO Auditor Pro")

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms.html', meta_title="Terms of Service | SEO Auditor Pro")

@app.route('/google0b8efa2bb9124e8a.html')
def google_verification():
    return send_from_directory('static', 'google0b8efa2bb9124e8a.html')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    scraped_data = scrape_page(url)
    report = analyze_seo(scraped_data)
    
    return render_template('report.html', report=report, url=url)

if __name__ == '__main__':
    app.run(debug=True)
