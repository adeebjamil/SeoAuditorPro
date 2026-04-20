def get_all_articles():
    seo_terms = [
        "On-Page SEO", "Technical SEO", "Backlink Building", "Keyword Research", 
        "Local SEO", "Core Web Vitals", "Schema Markup", "Content Strategy", 
        "Mobile Optimization", "Site Speed", "Voice Search SEO", "E-commerce SEO",
        "International SEO", "Link Equity", "Header Tags", "Meta Descriptions"
    ]
    
    actions = [
        "The Ultimate Guide to", "10 Secret Strategies for", "How to Dominate", 
        "A Beginner's Tutorial on", "Advanced Techniques for", "Common Mistakes in", 
        "Maximizing ROI with", "The Future of", "Step-by-Step:", "Unlock the Power of"
    ]
    
    articles = []
    for i in range(1, 351):
        term = seo_terms[i % len(seo_terms)]
        action = actions[i % len(actions)]
        year = 2026
        
        title = f"{action} {term} in {year}"
        slug = f"seo-article-{i}-{action.lower().replace(' ', '-')}-{term.lower().replace(' ', '-')}"
        desc = f"Looking to improve your website's search rankings? Read our comprehensive article #{i} about {term}, covering the best methods and latest algorithms."
        
        content = f"""
        <p class="lead">Welcome to SEO Guide #{i}. In this article, we dive deep into <strong>{term}</strong> and why it matters for your website's organic visibility.</p>
        
        <h3 class="mt-4">Why {term} is Crucial</h3>
        <p>Google and other search engines continuously update their algorithms to provide the best possible results. Focusing on {term} ensures that your site meets both user expectations and crawler requirements.</p>
        
        <h3 class="mt-4">Best Practices</h3>
        <ul>
            <li>Conduct thorough research before making structural changes.</li>
            <li>Maintain a clean, logical hierarchy for your content.</li>
            <li>Monitor your metrics via Google Search Console and Analytics.</li>
        </ul>
        
        <div class="alert alert-info mt-4">
            <strong>Pro Tip:</strong> Combine {term} with a solid overall content strategy to see compounded growth over time.
        </div>
        """
        
        articles.append({
            "id": i,
            "title": title,
            "slug": slug,
            "description": desc,
            "content": content,
            "image_seed": i % 100
        })
        
    return articles

ARTICLES_DB = get_all_articles()

def get_article_by_slug(slug):
    for article in ARTICLES_DB:
        if article['slug'] == slug:
            return article
    return None
