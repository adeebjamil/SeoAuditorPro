# Website SEO Auditor 🚀

A Python/Flask powered tool to instantly audit a website's SEO health by just dropping the URL. This performs a live scrape using `requests` and `BeautifulSoup` to analyze title tags, meta descriptions, heading structure (H1/H2s), image alt tags, along with checking for root `robots.txt` and `sitemap.xml`.

## Setup Instructions

1. **Activate your virtual environment (Optional but Recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```

2. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```powershell
   python app.py
   ```

4. **View the Tool**
   Open your browser to [http://localhost:5000](http://localhost:5000).

## Project Structure
- `app.py` - Flask web server and routing.
- `core/scraper.py` - Logic to visit the given URL, avoid timeouts, and pull out page elements.
- `core/analyzer.py` - Rules engine that scores the data out of 100 and builds suggestions.
- `templates/` - Jinja HTML templates styled via Bootstrap 5.
