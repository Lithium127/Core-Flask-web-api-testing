from flask_assets import Environment, Bundle


assets = Environment()


css = Bundle(
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css',
    'style.css'
)

assets.register('css_all', css)