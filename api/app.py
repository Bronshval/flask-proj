from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'base.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable = False)
    day = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Article {self.id}"



@app.route("/")
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.day.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    articles_alone = Article.query.get_or_404(id)
    try:
        db.session.delete(articles_alone)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error"

@app.route('/posts/<int:id>')
def posts_detail(id):
    articles_alone = Article.query.get(id)
    return render_template('post_detail.html', articles_alone=articles_alone)


@app.route('/posts/<int:id>/update', methods = ['POST', 'GET'])
def post_update(id):
    articles_alone = Article.query.get(id)
    if request.method == 'POST':
        articles_alone.title = request.form['title']
        articles_alone.intro = request.form['intro']
        articles_alone.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except Exception as ex:
            return ex
    else:
        return render_template('post_update.html', articles_alone=articles_alone)


@app.route('/create-article', methods = ['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text = text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except Exception as ex:
            return ex
    else:
        return render_template('create-article.html')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
