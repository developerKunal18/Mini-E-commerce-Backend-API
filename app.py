from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Product Model ----------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# ---------- Get All Products ----------
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in products
    ])

# ---------- Add Product ----------
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    product = Product(
        name=data["name"],
        price=data["price"],
        stock=data["stock"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product added"
    })

# ---------- Update Product ----------
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json()

    product = Product.query.get(product_id)

    if product:
        product.name = data["name"]
        product.price = data["price"]
        product.stock = data["stock"]

        db.session.commit()

        return jsonify({
            "message": "Product updated"
        })

    return jsonify({
        "message": "Product not found"
    }), 404

# ---------- Delete Product ----------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Product deleted"
        })

    return jsonify({
        "message": "Product not found"
    }), 404

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
