from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .product import Product

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')

    def add_product(self, session, product_name, product_price, product_quantity, product_description):
        if self.role != 'seller':
            raise PermissionError("Only sellers can add products.")
        new_product = Product(
            product_name=product_name,
            product_price=product_price,
            product_quantity=product_quantity,
            product_description=product_description,
            seller_id=self.id
        )
        session.add(new_product)
        session.commit()
        print(f'Product {product_name} added successfully.')
        return True

    def remove_product(self, session, product_id):
        if self.role != 'seller':
            raise PermissionError("Only sellers can remove products.")
        product = session.query(Product).filter_by(id=product_id, seller_id=self.id).first()
        if product:
            session.delete(product)
            session.commit()
            print(f'Product with ID {product_id} removed successfully.')
            return True
        else:
            print(f'Product with ID {product_id} not found or not owned by the seller.')
            return False

    def view_order_summary(self, session):
        if self.role != 'seller':
            raise PermissionError("Only sellers can view order summaries.")
        orders = session.query(Product).filter_by(seller_id=self.id).all()
        if not orders:
            print("No orders found for this seller.")
            return []
        order_summary = []
        for order in orders:
            order_summary.append({
                'product_name': order.product_name,
                'product_price': order.product_price,
                'product_quantity': order.product_quantity,
                'product_description': order.product_description
            })
        print('Order summary viewed successfully.')
        return order_summary