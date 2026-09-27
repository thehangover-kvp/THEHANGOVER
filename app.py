from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# =========================================================
# DATABASE
# =========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hangover.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# FOOD MODEL
# =========================================================

class Food(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    available = db.Column(
        db.Boolean,
        default=True
    )


# =========================================================
# OFFER MODEL
# =========================================================

class Offer(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    text = db.Column(
        db.String(300),
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )


# =========================================================
# SHOP STATUS MODEL
# =========================================================

class ShopStatus(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    is_open = db.Column(
        db.Boolean,
        default=True
    )


# =========================================================
# SHOP STATUS FUNCTION
# =========================================================

def get_shop_status():

    shop = ShopStatus.query.first()

    if shop is None:

        shop = ShopStatus(
            is_open=True
        )

        db.session.add(shop)

        db.session.commit()

    return shop


# =========================================================
# CUSTOMER HOME
# =========================================================

@app.route("/")
def home():

    foods = Food.query.all()

    offers = Offer.query.filter_by(
        active=True
    ).all()

    shop = get_shop_status()

    return render_template(
        "index.html",
        foods=foods,
        offers=offers,
        shop=shop
    )


# =========================================================
# SERVICE WORKER
# =========================================================

@app.route("/service-worker.js")
def service_worker():

    return send_from_directory(
        app.static_folder,
        "service-worker.js"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]


        if (
            username == "admin"
            and
            password == "1234"
        ):

            return redirect(
                url_for("dashboard")
            )


        return "Wrong Username or Password ❌"


    return render_template(
        "admin.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def dashboard():

    foods = Food.query.all()

    shop = get_shop_status()

    return render_template(
        "dashboard.html",
        foods=foods,
        shop=shop
    )


# =========================================================
# TOGGLE SHOP
# =========================================================

@app.route("/admin/toggle-shop")
def toggle_shop():

    shop = get_shop_status()

    shop.is_open = not shop.is_open

    db.session.commit()

    return redirect(
        url_for("dashboard")
    )


# =========================================================
# ADD FOOD
# =========================================================

@app.route(
    "/admin/add-food",
    methods=["GET", "POST"]
)
def add_food():

    if request.method == "POST":

        name = request.form["name"]

        category = request.form["category"]

        price = float(
            request.form["price"]
        )

        available = (
            request.form["available"]
            == "1"
        )


        new_food = Food(

            name=name,

            category=category,

            price=price,

            available=available

        )


        db.session.add(
            new_food
        )

        db.session.commit()


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "add_food.html"
    )


# =========================================================
# EDIT FOOD
# =========================================================

@app.route(
    "/admin/edit-food/<int:food_id>",
    methods=["GET", "POST"]
)
def edit_food(food_id):

    food = Food.query.get_or_404(
        food_id
    )


    if request.method == "POST":

        food.name = request.form["name"]

        food.category = request.form["category"]

        food.price = float(
            request.form["price"]
        )

        food.available = (
            request.form["available"]
            == "1"
        )


        db.session.commit()


        return redirect(
            url_for("dashboard")
        )


    return render_template(
        "edit_food.html",
        food=food
    )


# =========================================================
# DELETE FOOD
# =========================================================

@app.route(
    "/admin/delete-food/<int:food_id>"
)
def delete_food(food_id):

    food = Food.query.get_or_404(
        food_id
    )


    db.session.delete(
        food
    )

    db.session.commit()


    return redirect(
        url_for("dashboard")
    )


# =========================================================
# ADD OFFER
# =========================================================

@app.route(
    "/admin/add-offer",
    methods=["GET", "POST"]
)
def add_offer():

    if request.method == "POST":

        text = request.form["text"]


        new_offer = Offer(

            text=text,

            active=True

        )


        db.session.add(
            new_offer
        )

        db.session.commit()


        return redirect(
            url_for("offers")
        )


    return render_template(
        "add_offer.html"
    )


# =========================================================
# MANAGE OFFERS
# =========================================================

@app.route("/admin/offers")
def offers():

    offers = Offer.query.all()


    return render_template(
        "add_offer.html",
        offers=offers
    )


# =========================================================
# EDIT OFFER
# =========================================================

@app.route(
    "/admin/edit-offer/<int:offer_id>",
    methods=["GET", "POST"]
)
def edit_offer(offer_id):

    offer = Offer.query.get_or_404(
        offer_id
    )


    if request.method == "POST":

        offer.text = request.form["text"]

        db.session.commit()


        return redirect(
            url_for("offers")
        )


    return render_template(
        "edit_offer.html",
        offer=offer
    )


# =========================================================
# DELETE OFFER
# =========================================================

@app.route(
    "/admin/delete-offer/<int:offer_id>"
)
def delete_offer(offer_id):

    offer = Offer.query.get_or_404(
        offer_id
    )


    db.session.delete(
        offer
    )

    db.session.commit()


    return redirect(
        url_for("offers")
    )


# =========================================================
# TOGGLE OFFER
# =========================================================

@app.route(
    "/admin/toggle-offer/<int:offer_id>"
)
def toggle_offer(offer_id):

    offer = Offer.query.get_or_404(
        offer_id
    )


    offer.active = not offer.active

    db.session.commit()


    return redirect(
        url_for("offers")
    )


# =========================================================
# RUN APP
# =========================================================
with app.app_context():
    db.create_all()
    get_shop_status()


if __name__ == "__main__":
    app.run(
        debug=True
    )
