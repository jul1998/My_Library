from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)
app.app_context().push()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)


    def __repr__(self):
        return '<title %r>' % self.title


    def serialize(self):
        return({
            "title": self.title,
            "author": self.author,
            "rating": self.rating
        })


db.create_all()



@app.route('/')
def home():
    books = db.session.query(Books).all()

    return render_template("index.html", all_books=books)


@app.route("/add", methods=['POST', "GET"])
def add():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        rating = request.form.get("rating")

        new_entry = Books(title=title, author=author, rating=rating)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template("add.html")

@app.route("/edit/<int:book_id>", methods=['POST', "GET"])
def edit_rating(book_id):
    book_id = Books.query.filter_by(id=book_id).first()
    if request.method == "POST":
        new_rating = request.form.get("rating")
        book_id.rating = new_rating
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", book=book_id)

@app.route("/delete")
def delete_book():
    book_id = request.args.get("id")
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

