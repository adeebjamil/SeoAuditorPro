from flask import Blueprint, redirect, request, url_for, render_template

bp = Blueprint('out', __name__)

# Mapping for smartlink destinations and their fallback pages
SMARTLINKS = {
    'seo-guides': {
        'url': 'https://www.profitablecpmratenetwork.com/y8vk6ji2k?key=6661e011f23be53400d55fe08d9c2449',
        'fallback': '/articles'
    },
    'tools-vault': {
        'url': 'https://www.profitablecpmratenetwork.com/y8vk6ji2k?key=6661e011f23be53400d55fe08d9c2449',
        'fallback': 'https://tools-vault.app/'
    },
    'temp-mail': {
        'url': 'https://www.profitablecpmratenetwork.com/y8vk6ji2k?key=6661e011f23be53400d55fe08d9c2449',
        'fallback': 'https://www.tempinbox.me/'
    }
}

@bp.route('/out')
def out_redirect():
    target = request.args.get('target')
    info = SMARTLINKS.get(target)
    if not info:
        return redirect(url_for('index'))
    return render_template('out_redirect.html', smart_url=info['url'], fallback_url=info['fallback'])
