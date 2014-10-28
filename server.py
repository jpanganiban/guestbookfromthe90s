from flask import Flask, render_template, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@mysql/guestbook'
db = SQLAlchemy(app)


class Guestlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, index=True)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    content = db.Column(db.Text)

    @property
    def website(self):
        return Website.query.filter_by(website_id=self.website_id).first()


class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    @properties
    def guestlogs(self):
        return Guestlog.query.filter_by(website_id=self.id).all()

    def __repr__(self):
        return "??Guestlog %s %s %s??" % (self.name, self.email, self.content)


@app.route('/')
def page_index():
    logs = Guestlog.query.all()  # []
    return render_template('index.html', logs=logs)


@app.route('/guestbook', methods=['POST'])
def api_guestbook():
    log = Guestlog(name=request.form['author'],
             email=request.form['email'],
             content=request.form['content'])
    db.session.add(log)
    db.session.commit()
    return redirect('/')


@app.route('/guestlogs/<int:id>', methods=['GET'])
def api_guestlog(id):
    log = Guestlog.query.filter_by(id=id).first()  # ()
    db.session.delete(log)
    db.session.commit()
    return redirect('/')


@app.route('/db/rebuild')
def db_rebuild():
    """A supersecret destructive api that
    rebuilds the database."""
    db.drop_all()
    db.create_all()
    return "Ok"


if __name__ == '__main__':
    app.run(
        debug=os.environ.get('DEBUG', 'true').lower() == 'true',
        host=os.environ.get('HOST', '0.0.0.0'),
        port=int(os.environ.get('PORT', 5000))
    )
