from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .product import Product
from .cart import Cart

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')

    def change_role(self, session, new_role):   
        self.role = new_role
        session.commit()
        print(f'User {self.username} role changed to {new_role}.')
        return True

    def add_product(self, session, product_name, product_price, product_quantity, product_description, product_image):
        if self.role != 'seller':
            raise PermissionError("Only sellers can add products.")
        new_product = Product(
            product_name=product_name,
            product_price=product_price,
            product_quantity=product_quantity,
            product_description=product_description,
            product_image=product_image,
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
        
    def view_seller_summary(self, session, page, per_page):
        if self.role != 'seller':
            raise PermissionError("Only sellers can view seller summary.")
        
        total_orders = session.query(Product).filter_by(seller_id=self.id).count()
        orders = session.query(Product).filter_by(seller_id=self.id).offset((page - 1) * per_page).limit(per_page).all()
        if not orders:
            return {
                'orders': [],
                'page': page,
                'per_page': per_page,
                'total_pages': 0,
                'total_orders': 0,
                'next_page': None,
                'prev_page': None
            }
        order_summary = []
        for order in orders:
            order_summary.append({
                'product_id': order.id,
                'product_name': order.product_name,
                'product_price': order.product_price,
                'product_quantity': order.product_quantity,
                'product_description': order.product_description,
                'product_image': order.product_image
            })
        total_pages = (total_orders + per_page - 1) // per_page
        return {
            'orders': order_summary,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_orders': total_orders,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None
        }

    def view_order_summary(self, session, page, per_page):  
        total_products = session.query(Product).count()
        products = session.query(Product).offset((page - 1) * per_page).limit(per_page).all()
        product_summary = []
        for product in products:
            product_summary.append({
                'product_id': product.id,
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': product.product_quantity,
                'product_description': product.product_description,
                'product_image': product.product_image
            })
        total_pages = (total_products + per_page - 1) // per_page
        return {
            'products': product_summary,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_products': total_products,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None
        }
    
    def add_to_cart(self, session, product_id, quantity):
        cart_item = session.query(Cart).filter_by(user_id=self.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=self.id, product_id=product_id, quantity=quantity)
            session.add(cart_item)
        session.commit()
        print(f'Added {quantity} of product ID {product_id} to cart.')
        return True
    
    def view_cart(self, session, page, per_page):
        total_cart_items = session.query(Cart).filter_by(user_id=self.id).count()
        cart_items = session.query(Cart).filter_by(user_id=self.id).offset((page - 1) * per_page).limit(per_page).all()
        cart_summary = []
        for item in cart_items:
            product = session.query(Product).filter_by(id=item.product_id).first()
            cart_summary.append({
                'product_name': product.product_name,
                'product_price': product.product_price,
                'product_quantity': item.quantity,
                'product_description': product.product_description,
                'product_image': product.product_image
            })
        total_pages = (total_cart_items + per_page - 1) // per_page
        return {
            'cart_items': cart_summary,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_cart_items': total_cart_items,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None
        }
    
    def checkout(self, session):
        cart_items = session.query(Cart).filter_by(user_id=self.id).all()
        if not cart_items:
            print("No items in cart to checkout.")
            return False
        for item in cart_items:
            session.delete(item)
        session.commit()
        print("Checked out successfully. All items removed from cart.")
        return True   