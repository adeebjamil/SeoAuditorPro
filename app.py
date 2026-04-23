from flask import Flask, render_template, request, send_from_directory, abort, make_response
from core.scraper import scrape_page
from core.analyzer import analyze_seo
from articles_data import ARTICLES_DB, get_article_by_slug
from core.out_redirect import bp as out_redirect_bp
from core.tools import tools_bp
import os


app = Flask(__name__)
app.register_blueprint(out_redirect_bp)
app.register_blueprint(tools_bp)

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

# Health Check Endpoint for UptimeRobot (Keeps Render Free Tier awake)
@app.route('/ping')
def ping():
    return "OK", 200

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

@app.route('/robots.txt')
def robots_txt():
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.url_root.rstrip('/')}/sitemap.xml"
    ]
    return make_response("\n".join(lines), 200, {'Content-Type': 'text/plain'})

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    base_url = request.url_root.rstrip('/')
    
    # Define pages with priority and changefreq
    static_pages = [
        {'route': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'route': '/articles', 'priority': '0.9', 'changefreq': 'daily'},
        {'route': '/tools/', 'priority': '0.8', 'changefreq': 'weekly'},
        {'route': '/tools/meta-generator', 'priority': '0.8', 'changefreq': 'weekly'},
        {'route': '/tools/schema-generator', 'priority': '0.8', 'changefreq': 'weekly'},
        {'route': '/privacy-policy', 'priority': '0.3', 'changefreq': 'monthly'},
        {'route': '/terms-of-service', 'priority': '0.3', 'changefreq': 'monthly'}
    ]
    
    pages = []
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')

    for p in static_pages:
        pages.append({
            'loc': f"{base_url}{p['route']}",
            'lastmod': today,
            'priority': p['priority'],
            'changefreq': p['changefreq']
        })
        
    for article in ARTICLES_DB:
        pages.append({
            'loc': f"{base_url}/article/{article['slug']}",
            'lastmod': today, # In a real app, this would be the article's updated date
            'priority': '0.7',
            'changefreq': 'weekly'
        })
        
    xml_sitemap = render_template('sitemap.xml', pages=pages)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    approach = request.form.get('approach', 'static')
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    scraped_data = scrape_page(url, approach)
    report = analyze_seo(scraped_data)
    
    return render_template('report.html', report=report, url=url, approach=approach)

if __name__ == '__main__':
    app.run(debug=True)
