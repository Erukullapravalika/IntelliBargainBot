from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import re
import mysql.connector
import time
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# ==============================
# LOAD MODELS
# ==============================
kmeans = joblib.load("models/kmeans.pkl")
scaler = joblib.load("models/scaler.pkl")
label_map = joblib.load("models/label_map.pkl")
RFM_FEATURES = joblib.load("models/rfm_features.pkl")

print("Loading intent model...")
intent_pipeline = pipeline(
    "text-classification",
    model="Falconsai/intent_classification",
    top_k=1
)
print("Intent model ready!")

# ==============================
# SESSION MEMORY
# ==============================
sessions = {}
SESSION_TIMEOUT = 600

# ==============================
# RESPONSE TEMPLATES
# ==============================
TEMPLATES = {
    "counter":  "I understand your offer of ₹{user}. Based on your shopping history, I can offer ₹{counter}.",
    "accept":   "Great! Deal confirmed at ₹{price} 🎉",
    "reject":   "No worries! The product is still available at ₹{price}.",
    "final":    "This is my final offer: ₹{price}. I cannot go lower than this.",
    "too_low":  "₹{user} is too low for this product. Best I can offer is ₹{counter}.",
    "closed":   "This negotiation is already closed 😊",
    "clarify":  "Could you please share your offer amount?",
    "error":    "Something went wrong. Please try again.",
    "bulk":     "I understand your offer of ₹{user} for {qty} units. Based on your loyalty, I can offer ₹{counter} per unit (Total: ₹{total})."
}

# ==============================
# ACCEPT GAP 
# ==============================
def get_accept_gap(segment):

    if segment == 2:      # Loyal
        return 50

    elif segment == 1:    # Regular
        return 35

    else:                 # New
        return 20


# ==============================
# ANALYTICAL BEHAVIORAL MODEL
# ==============================
def calculate_negotiation_bounds(customer, product, quantity):

    unit_price = float(product["listed_price"])

    listed_price = unit_price * quantity

    demand_tier = int(product["demand_tier"])

    segment = predict_segment(customer)

    policy = get_negotiation_policy(
        segment,
        demand_tier,
        quantity
    )

    max_discount = policy["discount"]

    floor_ratio = policy["floor"]

    concession_pace = policy["pace"]

    max_rounds = policy["rounds"]

    min_price = listed_price * floor_ratio

    initial_counter = listed_price 


    initial_counter = max(
        initial_counter,
        min_price
    )

    print("\n===== NEGOTIATION POLICY =====")
    print("Segment       :", segment)
    print("Demand Tier   :", demand_tier)
    print("Quantity      :", quantity)
    print("Max Discount  :", round(max_discount * 100, 2), "%")
    print("Floor Price   :", round(min_price))
    print("Rounds        :", max_rounds)
    print("Pace          :", concession_pace)
    print("=============================\n")

    return {

        "segment": segment,

        "unit_price": unit_price,

        "listed_price": listed_price,

        "min_price": min_price,

        "initial_counter": initial_counter,

        "concession_pace": concession_pace,

        "max_rounds": max_rounds
    }

# ==============================
# DB CONNECTION
# ==============================
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="negotiation_db"
    )

# ==============================
# EXTRACT PRICE
# ==============================
def extract_price(message):
    clean = (
        message.lower()
        .replace("₹", "")
        .replace("rs", "")
        .replace("rupees", "")
    )
    nums = re.findall(r"\d+(?:\.\d+)?", clean)
    if nums:
        values = [float(x) for x in nums if float(x) > 10]
        if values:
            return max(values)
    return None

# ==============================
# INTENT DETECTION
# ==============================
def get_intent(message):
    msg = message.lower().strip()

    accept_words = ["yes", "ok", "deal", "accept", "agreed", "sure", "fine", "okay", "done"]
    reject_words = ["no", "reject", "too high", "not interested"]

    if any(w in msg for w in accept_words):
        return "accept"
    if any(w in msg for w in reject_words):
        return "reject"

    try:
        result = intent_pipeline(message)[0][0]
        label  = result["label"].lower()
        score  = result["score"]
        if score > 0.65:
            if any(x in label for x in ["accept", "agree", "positive"]):
                return "accept"
            if any(x in label for x in ["reject", "negative"]):
                return "reject"
    except Exception as e:
        print("Intent error:", e)

    if any(ch.isdigit() for ch in msg):
        return "offer"

    return "other"

# ==============================
# GET CUSTOMER FEATURES
# ==============================
def get_customer(user_id):
    try:
        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT recency_days, total_orders, avg_spend_per_order,
                   customer_lifetime_days, purchase_frequency, total_spend
            FROM customer_features WHERE user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        db.close()
        return result
    except Exception as e:
        print("Customer DB error:", e)
        return None

# ==============================
# GET PRODUCT
# ==============================
def get_product(product_id):
    try:
        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT listed_price, demand_tier
            FROM products WHERE product_id = %s
        """, (product_id,))
        result = cursor.fetchone()
        db.close()
        return result
    except Exception as e:
        print("Product DB error:", e)
        return None

# ==============================
# PREDICT SEGMENT
# ==============================
def predict_segment(customer):
    try:
        df      = pd.DataFrame([{f: customer[f] for f in RFM_FEATURES}])
        scaled  = scaler.transform(df[RFM_FEATURES])
        cluster = kmeans.predict(scaled)[0]
        segment = int(label_map[cluster])
        return segment
    except Exception as e:
        print("Segment prediction error:", e)
        return 0

# ======================================
# Negotiation Policy
#=======================================
def get_negotiation_policy(segment, demand_tier, quantity):

    policies = {

    # NEW
    0: {

        # HIGH DEMAND
        2: {
            "discount": 0.10,
            "floor": 0.90,
            "rounds": 4,
            "pace": 0.40
        },

        # MEDIUM DEMAND
        1: {
            "discount": 0.15,
            "floor": 0.85,
            "rounds": 4,
            "pace": 0.45
        },

        # LOW DEMAND
        0: {
            "discount": 0.20,
            "floor": 0.80,
            "rounds": 4,
            "pace": 0.50
        }
    },

    # REGULAR
    1: {

        2: {
            "discount": 0.15,
            "floor": 0.85,
            "rounds": 5,
            "pace": 0.50
        },

        1: {
            "discount": 0.22,
            "floor": 0.78,
            "rounds": 5,
            "pace": 0.55
        },

        0: {
            "discount": 0.28,
            "floor": 0.72,
            "rounds": 5,
            "pace": 0.60
        }
    },

    # LOYAL
    2: {

        2: {
            "discount": 0.20,
            "floor": 0.80,
            "rounds": 6,
            "pace": 0.60
        },

        1: {
            "discount": 0.28,
            "floor": 0.72,
            "rounds": 6,
            "pace": 0.65
        },

        0: {
            "discount": 0.35,
            "floor": 0.65,
            "rounds": 6,
            "pace": 0.70
        }
    }
}

    policy = policies[segment][demand_tier]

    quantity_bonus = min(
        (quantity - 1) * 0.01,
        0.05
    )

    policy["discount"] = min(
        policy["discount"] + quantity_bonus,
        0.35
    )

    return policy

# ==============================
# CLEANUP SESSIONS
# ==============================
def cleanup_sessions():
    now     = time.time()
    expired = [k for k, v in sessions.items() if now - v["timestamp"] > SESSION_TIMEOUT]
    for k in expired:
        del sessions[k]

# ==============================
# SIGNUP API
# ==============================
@app.route("/signup", methods=["POST"])
def signup():
    data     = request.json
    name     = data.get("name")
    email    = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Please enter all fields"}), 400

    try:
        db     = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            db.close()
            return jsonify({"error": "Email already exists"}), 400

        cursor.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)", (name, email, password))
        db.commit()
        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO customer_features(
                user_id, recency_days, total_orders, avg_spend_per_order,
                customer_lifetime_days, purchase_frequency, total_spend
            ) VALUES(%s,%s,%s,%s,%s,%s,%s)
        """, (user_id, 365, 0, 0, 0, 0, 0))
        db.commit()
        db.close()

        return jsonify({"message": "Signup successful", "user_id": user_id})

    except Exception as e:
        print("Signup error:", e)
        return jsonify({"error": "Signup failed"}), 500

# ==============================
# LOGIN API
# ==============================
@app.route("/login", methods=["POST"])
def login():
    data     = request.json
    email    = data.get("email")
    password = data.get("password")

    try:
        db     = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, name, email FROM users
            WHERE email=%s AND password=%s
        """, (email, password))
        user = cursor.fetchone()
        db.close()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        return jsonify(user)

    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Login failed"}), 500

# ==============================
# RESET SESSION API
# ==============================
@app.route("/reset_session", methods=["POST"])
def reset_session():
    data       = request.json
    user_id    = data.get("user_id")
    product_id = data.get("product_id")
    key        = f"{user_id}_{product_id}"
    if key in sessions:
        del sessions[key]
    return jsonify({"message": "Session reset"})

# ==============================
# NEGOTIATION API
# ==============================
@app.route("/negotiate", methods=["POST"])
def negotiate():

    cleanup_sessions()

    data       = request.json
    user_id    = data.get("user_id")
    product_id = data.get("product_id")
    quantity   = int(data.get("quantity", 1))
    message    = data.get("message", "").strip()

    if not user_id or not product_id or not message:
        return jsonify({"response": TEMPLATES["error"]})

    key   = f"{user_id}_{product_id}"
    reset = data.get("reset", False)
    if reset and key in sessions:
        del sessions[key]

    intent     = get_intent(message)
    user_offer = extract_price(message)

    # ==============================
    # INIT SESSION
    # ==============================
    if key not in sessions:

        customer = get_customer(user_id)
        if not customer:
            customer = {
                "recency_days": 365, "total_orders": 0,
                "avg_spend_per_order": 0, "customer_lifetime_days": 0,
                "purchase_frequency": 0, "total_spend": 0
            }

        product = get_product(product_id)
        if not product:
            return jsonify({"response": TEMPLATES["error"]})

        bounds = calculate_negotiation_bounds(customer, product, quantity)

        listed_price    = bounds["listed_price"]
        unit_price      = bounds["unit_price"]
        min_price       = bounds["min_price"]
        counter         = bounds["initial_counter"]
        concession_pace = bounds["concession_pace"]
        segment = bounds["segment"]
        max_rounds = bounds["max_rounds"]

        sessions[key] = {
            "round":           0,
            "segment":         segment,
            "unit_price":      unit_price,
            "quantity":        quantity,
            "listed_price":    listed_price,
            "last_counter":    counter,
            "min_price":       min_price,
            "concession_pace": concession_pace,
            "max_rounds":      max_rounds,
            "status":          "negotiating",
            "timestamp":       time.time()
        }

        print("\n========== NEW SESSION ==========")
        print("User ID        :", user_id)
        print("Segment        :", segment)
        print("Quantity       :", quantity)
        print("Listed Price   :", listed_price)
        print("Initial Counter:", round(counter))
        print("Max Rounds     :", max_rounds)
        print("=================================\n")

    session = sessions[key]
    session["timestamp"] = time.time()

    # ==============================
    # CLOSED SESSION
    # Allow accept after final offer
    # ==============================
    if session["status"] == "final":
        if intent == "accept":
            session["status"] = "accepted"
            return jsonify({
                "response": TEMPLATES["accept"].format(
                    price=int(session["last_counter"])
                )
            })
        return jsonify({"response": TEMPLATES["closed"]})

    if session["status"] in ["accepted", "rejected"]:
        return jsonify({"response": TEMPLATES["closed"]})

    listed_price    = session["listed_price"]
    unit_price      = session["unit_price"]
    quantity        = session["quantity"]
    counter         = session["last_counter"]
    min_price       = session["min_price"]
    concession_pace = session["concession_pace"]
    max_rounds      = session["max_rounds"]

    # ==============================
    # ACCEPT
    # ==============================
    if intent == "accept":
        session["status"] = "accepted"
        return jsonify({
            "response": TEMPLATES["accept"].format(price=int(counter))
        })

    # ==============================
    # REJECT
    # ==============================
    if intent == "reject":
        session["status"] = "rejected"
        return jsonify({
            "response": TEMPLATES["reject"].format(price=int(listed_price))
        })

    # ==============================
    # OFFER FLOW
    # ==============================
    if intent == "offer" and user_offer:

        # TOO LOW
        if user_offer < min_price * 0.50:
            return jsonify({
                "response": TEMPLATES["too_low"].format(
                    user=int(user_offer),
                    counter=int(counter)
                )
            })

        # ACCEPT IF CLOSE
        accept_gap = get_accept_gap(
            session["segment"]
            )
        # Never accept below floor price
        if (
            user_offer >= min_price
            and
            abs(user_offer - counter) <= accept_gap
            ):
            
            session["status"] = "accepted"
            return jsonify({ "response": f"Great! Deal confirmed at ₹{int(user_offer)} 🎉"})

        # USER OFFER GREATER THAN COUNTER
        if user_offer > counter:
            session["status"] = "accepted"
            return jsonify({
                "response": TEMPLATES["accept"].format(price=int(user_offer))
            })

        # ==============================
        # TIME-DEPENDENT CONCESSION
        # P(t) = P_floor
        #   + (1-(t/T)^β)
        #   × (P_listed - P_floor)
        # ==============================
        current_round     = session["round"] + 1
        t_ratio           = min(current_round / max_rounds, 1.0)
        concession_factor = 1.0 - (t_ratio ** concession_pace)

        new_counter = min_price + (
            concession_factor * (listed_price - min_price)
        )
        new_counter = max(new_counter, min_price)
        
        offer_ratio = user_offer / listed_price
        
        # max adjustment ₹50
        adjustment = min(75, offer_ratio * 75)
        new_counter = max(
            min_price,
            new_counter - adjustment
            )
        session["last_counter"] = new_counter
        session["round"]        = current_round

        # FINAL ROUND
        if current_round >= max_rounds:
            session["status"] = "final"
            return jsonify({
                "response": TEMPLATES["final"].format(price=int(new_counter))
            })

        # ==============================
        # BULK QUANTITY RESPONSE
        # Show per unit + total if qty > 1
        # ==============================
        if quantity > 1:
            per_unit = new_counter / quantity
            return jsonify({
                "response": TEMPLATES["bulk"].format(
                    user=int(user_offer),
                    qty=quantity,
                    counter=int(per_unit),
                    total=int(new_counter)
                )
            })

        return jsonify({
            "response": TEMPLATES["counter"].format(
                user=int(user_offer),
                counter=int(new_counter)
            )
        })

    return jsonify({"response": TEMPLATES["clarify"]})

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)