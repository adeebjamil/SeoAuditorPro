from flask import Blueprint, render_template, request

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

@tools_bp.route('/', methods=['GET'])
def tools_index():
    return render_template('tools/index.html', 
                           meta_title="Free SEO Tools & Generators | SEO Auditor Pro", 
                           meta_desc="Access our suite of free SEO tools including Meta Tag Generator, Schema Markup Generator, and more.",
                           meta_keys="SEO tools, meta tag generator, schema generator, free SEO tools, JSON-LD generator")

@tools_bp.route('/meta-generator', methods=['GET', 'POST'])
def meta_generator():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        brand = request.form.get('brand', '').strip()
        location = request.form.get('location', '').strip()
        
        # Generate some smart templates based on input
        # We will return this back to the template
        return render_template('tools/meta_generator.html', 
                               meta_title="Meta Tag & Title Generator | SEO Auditor Pro",
                               keyword=keyword, brand=brand, location=location)

    return render_template('tools/meta_generator.html', meta_title="Meta Tag & Title Generator | SEO Auditor Pro", meta_desc="Generate perfectly optimized meta titles, descriptions, and keywords dynamically based on SEO best practices.")

@tools_bp.route('/schema-generator', methods=['GET'])
def schema_generator():
    return render_template('tools/schema_generator.html', meta_title="JSON-LD Schema Markup Generator | SEO Auditor Pro", meta_desc="Generate accurate JSON-LD structured data for Articles, Local Businesses, FAQs, and Products.")
