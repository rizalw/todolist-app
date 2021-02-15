from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    judul_tugas = db.Column(db.String(200), nullable = False)
    deskripsi = db.Column(db.String(50), nullable = False)
    deadline = db.Column(db.String(1500), nullable = False)

    def __init__ (self, judul_tugas, deskripsi, deadline):
        self.judul_tugas = judul_tugas
        self.deskripsi = deskripsi
        self.deadline = deadline

@app.route("/")
def index():
    data = Todo.query.order_by(Todo.id).all()
    return render_template("index.html", data = data)

@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == "POST":
        judul_tugas = request.form['judul_tugas']
        deskripsi = request.form['deskripsi']
        deadline = request.form['deadline']
        input_data = Todo(judul_tugas, deskripsi, deadline)
        db.session.add(input_data)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("create.html")

@app.route("/update/<int:id>", methods = ["GET", "POST"])
def update(id):
    data = Todo.query.get_or_404(id)
    if request.method == "POST":
        data.judul_tugas = request.form['judul_tugas']
        data.deskripsi = request.form['deskripsi']
        data.deadline = request.form['deadline']
        db.session.commit()
        return redirect("/")
    else:
        return render_template("update.html", data = data)

@app.route("/delete/<int:id>")
def delete(id):
    data = Todo.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)