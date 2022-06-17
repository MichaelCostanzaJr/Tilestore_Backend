import json
from flask import Flask, abort, request
from about_me import me
from mock_data import catalog
from config import db
from bson import ObjectId

app = Flask('tilestore')

@app.route("/", methods=['GET'])
def home():
    return "This is the Home Page"

@app.route("/about")
def about():
    return me["first"] + " " + me["middle"] + " " + me["last"] + " " + me["suffix"] + " " + str(me["age"])
    
@app.route("/myaddress")
def address():
    return f' {me["address"]["street"]} {me["address"]["city"]} {me["address"]["state"]} {me["address"]["zip"]}'

#########################################################################################################################
#################################################### API ENDPOINTS ######################################################
#########################################################################################################################

@app.route("/api/catalog", methods=['GET'])
def get_catalog():
    results = []
    cursor = db.products.find({})

    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)

    return json.dumps(results)



@app.route("/api/catalog", methods=['POST'])
def save_product():
    try:
        product = request.get_json()
        errors = ""

        if not "title" in product or len(product["title"]) < 5:
            errors += ", Title is required and should have at least 5 chars"

        if not "image" in product:
            errors += ", Image is required"

        if not "price" in product or product["price"] < 10:
            errors += ", Price is required and should be >= 10"

        if errors:
            return abort(400, errors)
    
    
        db.products.insert_one(product)
        product["_id"] = str(product["_id"])

        return json.dumps(product)

    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")



@app.route("/api/catalog/count", methods=['GET'])
def get_count():
    cursor = db.products.find({})
    num_items = 0
    for prod in cursor:
        num_items += 1

    return json.dumps(num_items)



@app.route("/api/product/<id>", methods=['GET'])
def get_product(id):
    try:

        if not ObjectId.is_valid(id):
            return abort(400, "Invalid id")

        product = db.products.find_one({"_id": ObjectId(id)})

        if not product:
           return abort(404, "Product not found")

        product["_id"] = str(product["_id"])
        return json.dumps(product)

    except:
        return abort(500, "Unexpected error")
    #return an error code
    #return abort(404, "Sorry, Id does not match any product")



@app.get("/api/catalog/total") 
def get_total():
    total = 0
    cursor = db.products.find({})
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)



@app.get("/api/products/<category>")
def products_by_category(category):
    results = []
    cursor = db.products.find({"category": category})
    category = category.lower()
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        results.append(prod)
        
    
    return json.dumps(results)



@app.get("/api/categories")
def get_unique_categories():
    cursor = db.products.find({})
    results = []
    for prod in cursor:
        cat = prod["category"]

        if not cat in results:
            results.append(cat)

    return json.dumps(results)



@app.get("/api/product/cheapest")
def get_cheapest_product():
    cursor = db.products.find({})
    solution = cursor[0]
    for prod in cursor:

        if prod["price"] < solution["price"]:
            solution = prod

    solution["_id"] = str(solution["_id"])

    return json.dumps(solution) 

####################################################################
##########################COUPON CODES##############################
####################################################################

# GET ALL
@app.route("/api/coupons", methods=['GET'])
def get_all_coupons():
    results = []
    cursor = db.coupons.find({})

    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)
    return json.dumps(results)

# SAVE COUPON CODE
@app.route("/api/coupons", methods=['POST'])
def save_coupon():
    try:
        coupon = request.get_json()
        errors = ""
        #validations
        if not "title" in coupon or len(coupon["title"]) < 7:
            errors += ", Title is required and should have at least 7 chars"

        if errors:
            return abort(400, errors)

        db.coupons.insert_one(coupon)

        coupon["_id"] = str(coupon["_id"])
        return json.dumps(coupon)

    except Exception as ex:
        return abort(500, F"Unexpected error: {ex}")
# GET CC BY CODE

@app.get("/api/coupons/<coupon>")
def coupons_by_code(coupon):
    results = []
    cursor = db.coupons.find({"coupon": coupon})
    coupon = coupon.lower()
    for cc in cursor:
        cc["_id"] = str(cc["_id"])
        results.append(cc)
        
    
    return json.dumps(results)

app.run(debug=True)

