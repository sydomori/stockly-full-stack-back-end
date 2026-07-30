from app.extensions import ma
from app.models.Product import Product
from app.models.Category import Category
from app.models.Supplier import Supplier
from app.models.User import User
from app.models.Activity_log import ActivityLog


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

class SupplierSchema(ma.SQLAlchemyAutoSchema):
    model = Supplier
    _load_instance = True

suppliers_schema = SupplierSchema(many=True)
supplier_schema = SupplierSchema()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class ActivityLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ActivityLog
        load_instance = True
        include_fk = True

activity_logs_schema = ActivityLogSchema(many=True)
activity_log_schema = ActivityLogSchema()