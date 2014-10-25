from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, template_folder='views')
db = SQLAlchemy(app)


@app.route('/')
def page_index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(
        debug=True,
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000))
    )
