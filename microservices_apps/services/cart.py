from flask import Blueprint, session, redirect, url_for, render_template

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def cart():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

@cart_bp.route('/add-to-cart/<item_type>/<int:item_id>', methods=['POST'])
def add_to_cart(item_type, item_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cart_items = session.get('cart', [])
    cart_items.append({'item_type': item_type, 'item_id': item_id})
    session['cart'] = cart_items
    
    return redirect(url_for('cart'))
