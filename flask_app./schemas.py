from flask_app.models import LatLong, Price, PropertyType
from flask_app import db, ma

class LatLongSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Event class."""

    class Meta:
        model = LatLong
        load_instance = True
        sqla_session = db.session
        include_fk = True
        include_relationships = True

class PriceSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Event class."""

    class Meta:
        model = Price
        load_instance = True
        include_fk = True
        sqla_session = db.session
        include_relationships = True

class PropertyTypeSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all the attributes from the Event class."""

    class Meta:
        model = PropertyType
        load_instance = True
        include_fk = True
        sqla_session = db.session
        include_relationships = True