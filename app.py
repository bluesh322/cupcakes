from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'somemoregoodfun'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
sess = db.session


@app.route('/')
def index():
    #cupcakes = Cupcake.query.all()
    form = AddCupcakeForm()
    return render_template('index.html', form = form)
"""
@app.route('/', methods=["POST"])
def add_cupcake():
    form = AddCupcakeForm()
    if form.validate_on_submit():
        new_cupcake = Cupcake()
        new_cupcake.flavor = form.flavor.data
        new_cupcake.size = form.size.data
        new_cupcake.rating = form.rating.data
        new_cupcake.image = form.image.data or None
        sess.add(new_cupcake)
        sess.commit()
        return redirect("/")
    else: 
        return render_template('index.html', form=form)
"""
############################## API ROUTES ########################################

@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes/<int:id>')
def show_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          size=request.json["size"],
                          rating=request.json["rating"],
                          image=request.json["image"] or None)
    sess.add(new_cupcake)
    sess.commit()
    res = jsonify(cupcake=new_cupcake.serialize())
    return (res, 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def patch_cupcake(id):
    req = request.json
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = req.get("flavor", cupcake.flavor)
    cupcake.size = req.get("size", cupcake.size)
    cupcake.rating = req.get("rating", cupcake.rating)
    cupcake.image = req.get("image", cupcake.image)

    sess.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    sess.delete(cupcake)
    sess.commit()

    return jsonify(message="Deleted")
