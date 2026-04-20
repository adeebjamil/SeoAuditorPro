import json
from core.scraper import scrape_page
from core.analyzer import analyze_seo

data = scrape_page('https://www.tempinbox.me/')
report = analyze_seo(data)

print(json.dumps(report, indent=2))
