import os
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@db:5432/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Kontak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    telepon = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    alamat = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    kontak_list = Kontak.query.all()
    return render_template("index.html", kontak=kontak_list)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_kontak = Kontak(
            nama=request.form["nama"],
            telepon=request.form["telepon"],
            email=request.form.get("email"),
            alamat=request.form.get("alamat")
        )
        db.session.add(new_kontak)
        db.session.commit()
        return redirect("/")
    return render_template("form.html", judul="Tambah Kontak", kontak=None)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    kontak = Kontak.query.get_or_404(id)
    if request.method == "POST":
        kontak.nama = request.form["nama"]
        kontak.telepon = request.form["telepon"]
        kontak.email = request.form.get("email")
        kontak.alamat = request.form.get("alamat")
        db.session.commit()
        return redirect("/")
    return render_template("form.html", judul="Edit Kontak", kontak=kontak)

@app.route("/delete/<int:id>")
def delete(id):
    kontak = Kontak.query.get_or_404(id)
    db.session.delete(kontak)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")