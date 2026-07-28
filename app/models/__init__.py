#register model so Flask-Migrate can detect it
from app.models.User import User
from app.models.Category import Category
from app.models.Supplier import Supplier
from app.models.Product import Product
from app.models.Product_suplier import ProductSupplier