from app.extensions import ma
from app.models.Product import Product
from app.models.Category import Category


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True

products_schema = ProductSchema(many=True)
product_schema = ProductSchema()

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model: Category
        load_instance = True
    