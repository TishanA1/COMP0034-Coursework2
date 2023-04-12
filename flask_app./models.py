from flask_app import db

# Lists all the columns used for each class
class Price(db.Model):
    """Prices"""

    __tablename__ = "price"
    id = db.Column(db.Integer, primary_key = True)
    date_of_transfer= db.Column(db.String(50), nullable=False)
    price= db.Column(db.Integer, nullable = False)

    def __repr__(self):
        """
        Returns the attributes of the event as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.price},{self.date_of_transfer}>"

class LatLong(db.Model):
    """Latitude and Longitude"""
    __tablename__ = "latlong"
    id = db.Column(db.Integer, primary_key = True)
    latitude= db.Column(db.String(50),nullable=False)
    longitude= db.Column(db.String(50), nullable=False)
    price= db.Column(db.Integer, nullable = False)
    date_of_transfer= db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """
        Returns the attributes of the event as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}: {self.latitude}, {self.longitude}, {self.price}, {self.date_of_transfer}>"

class PropertyType(db.Model):
    """Latitude and Longitude"""
    __tablename__ = "propertytype"
    id = db.Column(db.Integer, primary_key = True)
    price= db.Column(db.Integer, nullable = False)
    date_of_transfer= db.Column(db.String(50), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """
        Returns the attributes of the event as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"<{clsname}:{self.price}, {self.date_of_transfer}, {self.date_of_transfer}, {self.property_type}>"



