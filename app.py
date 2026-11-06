from flask import Flask, request, jsonify
import requests
import os

API_KEY = os.environ.get("INIT_API_KEY")
API_URL = "https://api.init.computer/v2/8jbwlidc8p"
from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# CONFIGURATION
API_KEY = os.environ.get("INIT_API_KEY")
API_URL = "https://api.init.computer/v2/8jbwlidc8p"

TAUX_YUAN = 650
WHATSAPP = "261388046403"

# INTERFACE COMPLETE
HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>MadaShop</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial;
    background: #f4f5f9;
}

header {
    background: #111827;
    color: white;
    padding: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    color: #facc15;
    font-size: 24px;
    font-weight: bold;
}

button {
    cursor: pointer;
    border: none;
    border-radius: 7px;
    padding: 11px;
}

.cart {
    background: #facc15;
    font-weight: bold;
}

.hero {
    background: linear-gradient(120deg,#111827,#2563eb);
    color: white;
    text-align: center;
    padding: 45px 15px;
}

.hero h1 {
    font-size: 29px;
}

.search {
    display: flex;
    max-width: 600px;
    margin: 25px auto 0;
    gap: 8px;
}

.search input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border: none;
    border-radius: 7px;
}

.search button {
    background: #facc15;
    font-weight: bold;
}

.container {
    padding: 20px;
    max-width: 1200px;
    margin: auto;
}

.products {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 13px;
}

.product {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px #0001;
}

.product img {
    width: 100%;
    height: 170px;
    object-fit: contain;
}

.info {
    padding: 12px;
}

.title {
    font-size: 14px;
    height: 35px;
    overflow: hidden;
}

.price {
    color: #e11d48;
    font-weight: bold;
    margin: 10px 0;
}

.add {
    width: 100%;
    background: #111827;
    color: white;
}

.panel {
    display: none;
    position: fixed;
    inset: 0;
    background: white;
    padding: 20px;
    overflow: auto;
    z-index: 10;
}

.panel.show {
    display: block;
}

.item {
    border-bottom: 1px solid #ddd;
    padding: 12px 0;
}

.checkout {
    background: #16a34a;
    color: white;
    width: 100%;
    margin-top: 20px;
}

footer {
    background: #111827;
    color: white;
    text-align: center;
    padding: 25px;
    margin-top: 30px;
}

@media(min-width:700px) {
    .products {
        grid-template-columns: repeat(4,1fr);
    }
}
</style>
</head>

<body>

<header>
    <div class="logo">MadaShop</div>

    <button class="cart" onclick="openCart()">
        🛒 Panier (<span id="count">0</span>)
    </button>
</header>

<section class="hero">
    <h1>Bienvenue sur MadaShop</h1>
    <p>Découvrez les produits de Pinduoduo</p>

    <div class="search">
        <input id="query" placeholder="Rechercher un produit...">
        <button onclick="search()">Chercher</button>
    </div>
</section>

<main class="container">

    <h2>Nos produits</h2>

    <p id="message">Recherchez votre premier produit.</p>

    <div class="products" id="products"></div>

</main>

<div class="panel" id="panel">

    <button onclick="closeCart()">← Retour</button>

    <h2>Mon panier</h2>

    <div id="cartItems"></div>

    <h3 id="total">Total : 0 Ar</h3>

    <button class="checkout" onclick="checkout()">
        Commander sur WhatsApp
    </button>

</div>

<footer>
    MadaShop © 2026
</footer>

<script>

const RATE = 650;
const WHATSAPP = "261388046403";

let cart = [];

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, c => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[c]);
}

function safeImage(url) {
    try {
        const u = new URL(url);
        if (u.protocol === "https:" || u.protocol === "http:") {
            return u.href;
        }
    } catch(e) {}
    return "https://placehold.co/300x200?text=MadaShop";
}

async function search() {

    let q = document.getElementById("query").value.trim();

    if (!q) {
        alert("Entrez un produit à rechercher.");
        return;
    }

    document.getElementById("message").innerText =
        "Recherche en cours...";

    document.getElementById("products").innerHTML = "";

    try {

        const response = await fetch(
            "/api/search?q=" + encodeURIComponent(q)
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur API");
        }

        displayProducts(data.items || []);

    } catch(e) {

        document.getElementById("message").innerText =
            "Erreur : " + e.message;

    }
}

function displayProducts(items) {

    const container = document.getElementById("products");

    container.innerHTML = "";

    if (!items.length) {
        document.getElementById("message").innerText =
            "Aucun produit trouvé.";
        return;
    }

    document.getElementById("message").innerText =
        items.length + " produits trouvés.";

    items.forEach((p, index) => {

        const price = Number(p.price) || 0;

        const priceAr = Math.round(price * RATE);

        const div = document.createElement("div");

        div.className = "product";

        div.innerHTML = `
            <img src="${escapeHTML(safeImage(p.pic_url))}"
                 alt="${escapeHTML(p.title)}">

            <div class="info">
                <div class="title">
                    ${escapeHTML(p.title)}
                </div>

                <div class="price">
                    ${priceAr.toLocaleString("fr-FR")} Ar
                </div>

                <button class="add">
                    Ajouter au panier
                </button>
            </div>
        `;

        div.querySelector("button").onclick = () => {
            addCart(p);
        };

        container.appendChild(div);

    });
}

function addCart(p) {

    cart.push({
        title: p.title,
        price: Number(p.price) || 0
    });

    updateCart();

}

function updateCart() {

    document.getElementById("count").innerText =
        cart.length;

    const container = document.getElementById("cartItems");

    container.innerHTML = "";

    let total = 0;

    cart.forEach((p, i) => {

        total += p.price * RATE;

        const div = document.createElement("div");

        div.className = "item";

        div.innerHTML = `
            ${escapeHTML(p.title)}
            <br>
            ${Math.round(p.price * RATE).toLocaleString("fr-FR")} Ar
            <button>Supprimer</button>
        `;

        div.querySelector("button").onclick = () => {
            cart.splice(i, 1);
            updateCart();
        };

        container.appendChild(div);

    });

    document.getElementById("total").innerText =
        "Total : " + Math.round(total).toLocaleString("fr-FR") + " Ar";

}

function openCart() {
    document.getElementById("panel").classList.add("show");
}

function closeCart() {
    document.getElementById("panel").classList.remove("show");
}

function checkout() {

    if (!cart.length) {
        alert("Votre panier est vide.");
        return;
    }

    let text = "Bonjour MadaShop, je souhaite commander :%0A%0A";

    let total = 0;

    cart.forEach((p, i) => {

        let price = Math.round(p.price * RATE);

        total += price;

        text += (i + 1) + ". " + p.title +
            " - " + price + " Ar%0A";

    });

    text += "%0ATotal : " + total + " Ar";

    window.open(
        "https://wa.me/" + WHATSAPP + "?text=" + text,
        "_blank"
    );

}

document.getElementById("query").addEventListener(
    "keydown",
    e => {
        if (e.key === "Enter") search();
    }
);

</script>

</body>
</html>
"""

# PAGE PRINCIPALE
@app.route("/")
def home():
    return render_template_string(HTML)


# VERIFICATION
@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "site": "MadaShop",
        "platform": "Pinduoduo"
    })


# RECHERCHE PIN DUODUO
@app.route("/api/search")
def search_products():

    keyword = request.args.get("q", "").strip()

    if not keyword:
        return jsonify({"items": []})

    if not API_KEY:
        return jsonify({
            "error": "Clé API manquante"
        }), 401

    try:

        response = requests.post(
            API_URL,
            headers={
                "Authorization": "Bearer " + API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "keyword": keyword
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        items = []

        for p in results:

            items.append({
                "title": p.get("title", "Produit"),
                "price": p.get("price", 0),
                "pic_url": p.get(
                    "image",
                    p.get("imageUrl", p.get("pic_url", ""))
                ),
                "detail_url": p.get(
                    "productUrl",
                    p.get("link", "")
                )
            })

        return jsonify({
            "items": items,
            "total": len(items)
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({
            "error": "Erreur API",
            "details": response.text[:300]
        }), 502

    except requests.exceptions.RequestException:
        return jsonify({
            "error": "Connexion API impossible"
        }), 502

    except ValueError:
        return jsonify({
            "error": "Réponse JSON invalide"
        }), 502


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

@app.route("/")
def home():
    return "MadaShop fonctionne !"


@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "site": "MadaShop",
        "platform": "Pinduoduo"
    })


@app.route("/api/search")
def search():

    keyword = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    if not keyword:
        return jsonify({"items": []})

    if not API_KEY:
        return jsonify({
            "error": "Clé API manquante"
        }), 401

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "keyword": keyword,
                "category": category
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])

        items = []

        for p in results:
            items.append({
                "title": p.get("title", "Produit"),
                "price": p.get("price", 0),
                "pic_url": p.get("image", ""),
                "detail_url": p.get("productUrl", ""),
                "discount": p.get("discount", "")
            })

        return jsonify({
            "items": items,
            "total": len(items)
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Erreur de connexion API",
            "details": str(e)
        }), 502

    except ValueError:
        return jsonify({
            "error": "Réponse JSON invalide"
        }), 502


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
