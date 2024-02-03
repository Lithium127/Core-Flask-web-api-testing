from flask_assets import Environment, Bundle


assets = Environment()

# any other scripts
js = Bundle(
    'site.js'
)

css = Bundle(
    'style.css'
)

assets.register('css_all', css)
assets.register('js_all', js)