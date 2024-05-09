from flask import flash, url_for, request, render_template, redirect, session
from shop import db, app, photos
from shop.products.models import Addproduct

@app.route('/addcart', methods=['POST'])
def AddCart():
    try: 
      product_id = request.form.get('product_id')
      quantity = int(request.form.get('quantity'))
      
      product = Addproduct.query.filter_by(id=product_id).first()
      if product_id and quantity  and request.method =="POST":
          DictItems = {product_id:{'name':product.name,
                                   'price':float(product.price),
                                   'discount':product.discount,
                                   
                                   'quantity':quantity,
                                   'image':product.image_1,
                                    'color':product.colors}}
          if 'Shoppingcart' in session:
              print(session['Shoppingcart'])
              
          else:
              session['Shoppingcart'] = DictItems
              return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)