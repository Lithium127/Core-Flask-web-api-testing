from flask_assets import Environment, Bundle


assets = Environment()

js = Bundle(
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js',
    'site.js'
)

css = Bundle(
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
    'style.css'
)

assets.register('css_all', css)
assets.register('js_all', js)