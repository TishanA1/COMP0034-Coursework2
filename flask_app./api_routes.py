# python -m flask --app flask_app --debug run
# http://127.0.0.1:5000/property-type?page=1&per-page=10

from flask import (
    render_template,
    current_app as app,
    request,
    make_response,
    jsonify,
)

from flask_app import db
from flask_app.models import LatLong, Price, PropertyType
from flask_app.schemas import LatLongSchema, PriceSchema, PropertyTypeSchema



# -------
# Schemas
# -------

HousePrices_schema = PriceSchema(many=True)
HousePrice_schema = PriceSchema()
HousePricesLatLong_schema = LatLongSchema(many=True)
HousePriceLatLong_schema = LatLongSchema()
HousePricesPropertyType_schema = PropertyTypeSchema(many=True)
HousePricePropertyType_schema = PropertyTypeSchema()


@app.route("/")
def index():
    """Returns the home page"""
    return render_template("index.html")

# Provides a GET route to receive all of LatLong
# paginate is used to put the values on different pages with a result of 100 values per page
@app.get("/lat-long")
def latlong():
    """Returns the details for all events"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 100, type =int)
    result = get_HousePricesLatLong(page,per_page)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    return response

# Provides a GET route to receive specific LatLong
@app.get("/lat-long/<id>")
def latlong_code(id):
    """Returns the details for a given region code."""
    latlong = db.session.execute(
        db.select(LatLong).filter_by(id=id)).scalar_one_or_none()
    if latlong:
        result = HousePriceLatLong_schema.dump(latlong)
        response = make_response(result, 200)
        response.headers["Content-Type"] = "application/json"
    else:
        message = jsonify(
            {
                "status": 404,
                "error": "Not found",
                "message": "Invalid resource URI",
            }
        )
        response = make_response(message, 404)
    return response

# Provides a DELETE route to delete any LatLong values
@app.delete("/lat-long/<id>")
def latlong_delete(id):
    """Removes a NOC record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    latlong = db.session.execute(
        db.select(LatLong).filter_by(id=id)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(latlong)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": latlong.price})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response

# Provides a PATCH route to change any LatLong values
@app.patch("/lat-long/<id>")
def latlong_update(id):
    """Updates changed fields for the NOC record"""
    # Find the current latlong in the database
    existing_region = db.session.execute(
        db.select(LatLong).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    region_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    HousePriceLatLong_schema.load(region_json, instance=existing_region, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(LatLong).filter_by(id=id)
    ).scalar_one_or_none()
    result = HousePriceLatLong_schema.jsonify(updated_region)
    return result

# Provides a POST route to put any new LatLong values
@app.post("/lat-long")
def latlong_add():
    """Adds a new NOC record to the dataset."""
    # Get the values of the JSON sent in the request
    id = request.json.get("id", "")
    latitude = request.json.get("latitude", "")
    longitude = request.json.get("longitude", "")
    price = request.json.get("price", "")
    date_of_transfer = request.json.get("date_of_transfer", "")
    # Create a new LatLong object using the values
    region = LatLong(id=id, latitude=latitude, longitude=longitude, price=price, date_of_transfer=date_of_transfer)
    # Save the new region to the database
    db.session.add(region)
    db.session.commit()
    # Return a reponse to the user with the newly added region in JSON format
    result = HousePriceLatLong_schema.jsonify(region)
    return result

# The same is applied for the ones below

@app.get("/pricing")
def price():
    """Returns the details for all events"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 100, type=int)
    result = get_HousePrices(page,per_page)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.get("/pricing/<id>")
def pricing_code(id):
    """Returns the details for a given region code."""
    price = db.session.execute(
        db.select(Price).filter_by(id=id)).scalar_one_or_none()
    if price:
        result = HousePrice_schema.dump(price)
        response = make_response(result, 200)
        response.headers["Content-Type"] = "application/json"
    else:
        message = jsonify(
            {
                "status": 404,
                "error": "Not found",
                "message": "Invalid resource URI",
            }
        )
        response = make_response(message, 404)
    return response

@app.delete("/pricing/<id>")
def pricing_delete(id):
    """Removes a NOC record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    pricing = db.session.execute(
        db.select(Price).filter_by(id=id)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(pricing)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": pricing.price})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response

@app.patch("/pricing/<id>")
def pricing_update(id):
    """Updates changed fields for the NOC record"""
    # Find the current region in the database
    existing_region = db.session.execute(
        db.select(Price).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    region_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    HousePrice_schema.load(region_json, instance=existing_region, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(Price).filter_by(id=id)
    ).scalar_one_or_none()
    result = HousePrice_schema.jsonify(updated_region)
    return result
#"id": "10",
#"price":"262000",
#"date_of_transfer":"20/06/2022"

@app.post("/pricing")
def pricing_add():
    """Adds a new NOC record to the dataset."""
    # Get the values of the JSON sent in the request
    id = request.json.get("id", "")
    date_of_transfer = request.json.get("date_of_transfer", "")
    price = request.json.get("price", "")
    # Create a new pricing object using the values
    region = Price(id=id, price=price, date_of_transfer=date_of_transfer)
    # Save the new pricing to the database
    db.session.add(region)
    db.session.commit()
    # Return a reponse to the user with the newly added region in JSON format
    result = HousePrice_schema.jsonify(region)
    return result

@app.get("/property-type")
def propertytype():
    """Returns the details for all events"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 100, type=int)
    result = get_HousePricesPropertyType(page,per_page)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    return response

@app.get("/property-type/<id>")
def propertytype_code(id):
    """Returns the details for a given region code."""
    propertytype = db.session.execute(
        db.select(PropertyType).filter_by(id=id)).scalar_one_or_none()
    if propertytype:
        result = HousePricePropertyType_schema.dump(propertytype)
        response = make_response(result, 200)
        response.headers["Content-Type"] = "application/json"
    else:
        message = jsonify(
            {
                "status": 404,
                "error": "Not found",
                "message": "Invalid resource URI",
            }
        )
        response = make_response(message, 404)
    return response

@app.delete("/property-type/<id>")
def propertytype_delete(id):
    """Removes a NOC record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    propertytype = db.session.execute(
        db.select(PropertyType).filter_by(id=id)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(propertytype)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": propertytype.price})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response

@app.patch("/property-type/<id>")
def propertytype_update(id):
    """Updates changed fields for the NOC record"""
    # Find the current property type in the database
    existing_region = db.session.execute(
        db.select(PropertyType).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    region_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    HousePricePropertyType_schema.load(region_json, instance=existing_region, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(PropertyType).filter_by(id=id)
    ).scalar_one_or_none()
    result = HousePricePropertyType_schema.jsonify(updated_region)
    return result

@app.post("/property-type")
def propertytype_add():
    """Adds a new NOC record to the dataset."""
    # Get the values of the JSON sent in the request
    id = request.json.get("id", "")
    date_of_transfer = request.json.get("date_of_transfer", "")
    price = request.json.get("price", "")
    property_type = request.json.get("property_type", "")
    # Create a new property type object using the values
    region = PropertyType(id=id, price=price, date_of_transfer=date_of_transfer, property_type = property_type)
    # Save the new property type to the database
    db.session.add(region)
    db.session.commit()
    # Return a reponse to the user with the newly added region in JSON format
    result = HousePricePropertyType_schema.jsonify(region)
    return result


def get_HousePrices(page,per_page):
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_HousePrices = db.paginate(db.select(Price).order_by(Price.id),page=page,per_page=per_page)
    event_json = HousePrices_schema.dump(all_HousePrices)
    results = {
        "results":event_json,
        "pagination": {
            "count": all_HousePrices.total,
            "page": page,
            "per_page": per_page,
            "pages": all_HousePrices.pages,
        },
    }
    return results

def get_HousePricesLatLong(page,per_page):
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_HousePricesLatLong = db.paginate(db.select(LatLong).order_by(LatLong.id),page=page,per_page=per_page)
    event_json = HousePricesLatLong_schema.dump(all_HousePricesLatLong)
    results = {
        "results":event_json,
        "pagination": {
            "count": all_HousePricesLatLong.total,
            "page": page,
            "per_page": per_page,
            "pages": all_HousePricesLatLong.pages,
        },

    }
    return results

def get_HousePricesPropertyType(page,per_page):
    """Function to get all events from the database as objects and convert to json.

    NB: This was extracted to a separate function as it is used in multiple places
    """
    all_HousePricesPropertyType = db.paginate(db.select(PropertyType).order_by(PropertyType.id),page=page,per_page=per_page)
    event_json = HousePricesPropertyType_schema.dump(all_HousePricesPropertyType)
    results = {
        "results":event_json,
        "pagination": {
            "count": all_HousePricesPropertyType.total,
            "page": page,
            "per_page": per_page,
            "pages": all_HousePricesPropertyType.pages,
        },

    }
    return results