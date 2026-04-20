import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import time
import concurrent.futures

def scrape_page(url):
    """Fetches the HTML of the page, parses SEO elements, schema, and checks broken links."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        # Measure Performance (TTFB / Load Time)
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15)
        load_time = time.time() - start_time
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # 1. Basic SEO
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else None
        
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag['content'].strip() if meta_desc_tag and meta_desc_tag.has_attr('content') else None
        
        h1_tags = [h1.text.strip() for h1 in soup.find_all('h1')]
        h2_tags = [h2.text.strip() for h2 in soup.find_all('h2')]
        
        images = soup.find_all('img')
        images_data = [{'src': img.get('src'), 'alt': img.get('alt', '').strip()} for img in images]
        
        # 2. Technical / Mobility / Security
        is_https = parsed_url.scheme == 'https'
        has_viewport = bool(soup.find('meta', attrs={'name': 'viewport'}))
        has_canonical = bool(soup.find('link', rel='canonical'))
        
        # 3. Social Tags & Schema
        og_title = bool(soup.find('meta', property='og:title'))
        og_desc = bool(soup.find('meta', property='og:description'))
        og_image = bool(soup.find('meta', property='og:image'))
        has_og = og_title and og_desc and og_image
        
        has_schema = len(soup.find_all('script', type='application/ld+json')) > 0
        
        # 4. Content Depth & Links
        for script in soup(['script', 'style']):
            script.extract()
        body_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ''
        word_count = len(re.findall(r'\w+', body_text))
        
        links = soup.find_all('a', href=True)
        internal_links = 0
        external_links = 0
        absolute_links = []
        
        for link in links:
            href = link.get('href', '')
            if href.startswith('http'):
                absolute_links.append(href)
                if urlparse(href).netloc == parsed_url.netloc:
                    internal_links += 1
                else:
                    external_links += 1
            elif href.startswith('mailto:') or href.startswith('tel:') or href.startswith('#'):
                continue
            else:
                internal_links += 1
                absolute_links.append(urljoin(base_url, href))
                
        # 5. Broken Links Checker (Sample up to 15 unique links)
        absolute_links = list(set(absolute_links))[:15]
        broken_links = []
        
        def check_link(l):
            try:
                r = requests.head(l, headers=headers, timeout=5, allow_redirects=True)
                if r.status_code >= 400 and r.status_code not in [403, 405]:
                    return l
            except:
                return l
            return None
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for r in executor.map(check_link, absolute_links):
                if r: broken_links.append(r)
                
        # 6. Root Files
        robots_present = requests.get(urljoin(base_url, '/robots.txt'), headers=headers, timeout=5).status_code == 200
        sitemap_present = requests.get(urljoin(base_url, '/sitemap.xml'), headers=headers, timeout=5).status_code == 200
        
        return {
            'url': url, 'title': title, 'meta_description': meta_desc,
            'h1_tags': h1_tags, 'h2_tags': h2_tags, 'images': images_data,
            'is_https': is_https, 'has_viewport': has_viewport, 'has_canonical': has_canonical,
            'has_og': has_og, 'has_schema': has_schema,
            'word_count': word_count, 'internal_links': internal_links, 'external_links': external_links,
            'load_time': load_time, 'broken_links': broken_links,
            'robots_present': robots_present, 'sitemap_present': sitemap_present,
            'status': 'success'
        }
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
