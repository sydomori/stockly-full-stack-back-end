from app.extensions import ma
from app.models.Product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True

products_schema = ProductSchema(many=True)
product_schema = ProductSchema()
    