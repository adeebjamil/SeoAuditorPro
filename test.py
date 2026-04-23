import json
import time
from core.scraper import scrape_page
from core.analyzer import analyze_seo

url = 'https://www.tempinbox.me/'

print(f"==================================================")
print(f"  TESTING URL: {url}")
print(f"==================================================\n")

# 1. Fast Scan
print(f"⚡ RUNNING FAST SCAN (Static HTML)...")
start_static = time.time()
data_static = scrape_page(url, approach='static')
report_static = analyze_seo(data_static)
time_static = time.time() - start_static

print(f"   -> Score: {report_static['score']}/100")
print(f"   -> H1 Tags Found: {len(data_static.get('h1_tags', []))} {data_static.get('h1_tags', [])}")
print(f"   -> Word Count: {data_static.get('word_count')}")
print(f"   -> Execution Time: {time_static:.2f} seconds\n")

# 2. Deep Scan
print(f"🤖 RUNNING DEEP SCAN (Headless JS)...")
start_headless = time.time()
data_headless = scrape_page(url, approach='headless')
report_headless = analyze_seo(data_headless)
time_headless = time.time() - start_headless

print(f"   -> Score: {report_headless['score']}/100")
print(f"   -> H1 Tags Found: {len(data_headless.get('h1_tags', []))} {data_headless.get('h1_tags', [])}")
print(f"   -> Word Count: {data_headless.get('word_count')}")
print(f"   -> Execution Time: {time_headless:.2f} seconds\n")

print(f"==================================================")
print(f"  TESTS COMPLETE")
print(f"==================================================")
