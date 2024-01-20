--< This web server does not use straight HTML >--

All HTML that is served to a user from the server is preprocessed
with the jinja2 Python based HTML preprocessor. 

Documentation for the preprocessor can be found here: https://jinja.palletsprojects.com/en/3.1.x/

Basic Information:

Jinja2's syntax is built to be relatively close to python

{% ... %} is used for statements and control flow
{{ ... }} is used for expressions that print to template output
{# ... #} is used for comments

Objects can be passed to the template renderer from raw python code by
adding the object to the **kwargs argument of the flask.render_template() function

--< __init__.py >--
@app.route("/)
def index():
    return render_template('index.html', menu_paths = ['path1', 'path2'])

--< index.html >--
< div >
    {{ menu_paths[0] }} // outputs 'path1'
    {{ menu_paths[1] }} // outputs 'path2'
</ div >