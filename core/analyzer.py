def analyze_seo(data):
    """Analyzes the scraped data, calculates score, and generates specific issues and fix suggestions."""
    if data.get('status') == 'error':
        return {
            'score': 0, 
            'suggestions': [{'issue': f"Failed to scrape URL: {data.get('message')}", 'fix': 'Check the URL spelling and ensure the server allows web scraping.'}], 
            'details': data
        }

    score = 100
    suggestions = []

    # 1. Title & Meta
    title = data.get('title')
    if not title:
        score -= 10; suggestions.append({'issue': 'Missing <title> tag.', 'fix': 'Add a <title> tag.'})
    elif len(title) < 30 or len(title) > 60:
        score -= 5; suggestions.append({'issue': f"Title length ({len(title)} chars) is suboptimal.", 'fix': 'Keep it between 30-60 characters.'})

    meta_desc = data.get('meta_description')
    if not meta_desc:
        score -= 10; suggestions.append({'issue': 'Missing Meta Description.', 'fix': 'Add a meta description tag.'})
    elif len(meta_desc) < 120 or len(meta_desc) > 160:
        score -= 5; suggestions.append({'issue': f"Meta description length ({len(meta_desc)} chars) is off.", 'fix': 'Aim for 120-160 characters.'})

    # 2. Headings
    h1_tags = data.get('h1_tags', [])
    if len(h1_tags) == 0:
        score -= 10; suggestions.append({'issue': 'Missing <h1> tag.', 'fix': 'Add exactly one <h1> tag.'})
    elif len(h1_tags) > 1:
        score -= 5; suggestions.append({'issue': f"Multiple <h1> tags found ({len(h1_tags)}).", 'fix': 'Prefer one main <h1> heading.'})

    if len(data.get('h2_tags', [])) == 0:
        score -= 5; suggestions.append({'issue': 'No <h2> subheadings found.', 'fix': 'Break up content with <h2> tags.'})

    # 3. Content Depth & Links
    word_count = data.get('word_count', 0)
    if word_count < 300:
        score -= 10; suggestions.append({'issue': f"Thin Content ({word_count} words).", 'fix': 'Expand page text to at least 300 words.'})

    if data.get('internal_links', 0) == 0:
        score -= 5; suggestions.append({'issue': 'No internal links.', 'fix': 'Add links pointing to other pages on your website.'})

    # 4. Technical / Security / Performance
    if not data.get('is_https'):
        score -= 10; suggestions.append({'issue': 'Missing HTTPS.', 'fix': 'Install SSL certificate.'})
    if not data.get('has_viewport'):
        score -= 10; suggestions.append({'issue': 'Missing Mobile Viewport.', 'fix': 'Add <meta name="viewport"...>'})
    if not data.get('has_canonical'):
        score -= 5; suggestions.append({'issue': 'Missing Canonical Link.', 'fix': 'Add <link rel="canonical"...>'})
        
    load_time = data.get('load_time', 0)
    if load_time > 3.0:
        score -= 10; suggestions.append({'issue': f"Slow response time ({load_time:.2f}s).", 'fix': 'Optimize your server to respond in under 1.5 seconds.'})
    elif load_time > 1.5:
        score -= 5; suggestions.append({'issue': f"Moderate response time ({load_time:.2f}s).", 'fix': 'Improve server scaling or cache to hit < 1s TTFB.'})

    # 5. Broken Links
    broken_links = data.get('broken_links', [])
    if broken_links:
        score -= 10; suggestions.append({'issue': f"Found {len(broken_links)} broken links (404/dead links).", 'fix': f"Fix dead links. Examples: {', '.join(broken_links[:2])}"})

    # 6. Social & Schema
    if not data.get('has_og'):
        score -= 5; suggestions.append({'issue': 'Incomplete Open Graph Tags.', 'fix': 'Add og:title, og:description, and og:image.'})
    if not data.get('has_schema'):
        score -= 10; suggestions.append({'issue': 'Missing Schema Markup (JSON-LD).', 'fix': 'Add structured data to help search engines understand your entities.'})

    # 7. Images
    images = data.get('images', [])
    missing_alts = [img for img in images if not img.get('alt')]
    if missing_alts:
        deduct = int(10 * (len(missing_alts) / max(len(images), 1)))
        score -= deduct
        suggestions.append({'issue': f"{len(missing_alts)} outside {len(images)} images missing 'alt'.", 'fix': 'Add descriptive alt text to images.'})

    # 8. Roots
    if not data.get('robots_present'):
        score -= 5; suggestions.append({'issue': 'robots.txt not found.', 'fix': 'Create a robots.txt file.'})
    if not data.get('sitemap_present'):
        score -= 5; suggestions.append({'issue': 'sitemap.xml not found.', 'fix': 'Generate a sitemap.xml file.'})

    score = max(0, score)
    if not suggestions:
        suggestions.append({'issue': 'None', 'fix': 'Great job! No major SEO issues found. Everything looks perfect.'})

    return {'score': score, 'suggestions': suggestions, 'details': data}
