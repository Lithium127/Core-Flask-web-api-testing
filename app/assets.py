from flask_assets import Environment, Bundle


assets = Environment()

js = Bundle(
    'https://code.jquery.com/jquery-3.5.1.min.js',
    'js/site.js'
)

css = Bundle(
    'css/style.scss'
)

assets.register('css_all', css)
assets.register('js_all', js)