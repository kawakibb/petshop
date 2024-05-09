from flask import flash, url_for, request, render_template, redirect, session
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import AddproductForm
import secrets, os


@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('products/updatebrand.html', title="update brand", updatebrand=updatebrand)

@app.route('/addcategory', methods=['GET','POST'])
def addcategory():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'The Category {getcategory} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcategory'))

    return render_template('products/addbrand.html')


@app.route('/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecategory.name = category
        flash(f'The category {updatecategory.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('category'))
    category = updatecategory.name
    return render_template('products/updatebrand.html', title="update category", updatecategory=updatecategory)



@app.route('/addproduct',methods=['POST','GET'])
def addproduct():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddproductForm(request.form)
    if request.method =="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        description = form.description.data
        color = form.color.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        addpro = Addproduct(name=name, price=price, discount=discount, stock=stock, color=color, description=description, brand_id=brand, category_id=category,image_3=image_3,image_2=image_2,image_1=image_1)
        db.session.add(addpro)
        flash(f'The product {name} had been added','success')
        db.session.commit()
        return redirect(url_for('admin'))
    
    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>',methods=['POST','GET'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    
    form = AddproductForm(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.color = form.color.data
        product.description = form.description.data
        product.brand_id = brand
        product.category_id = category

        #delet images

        db.session.commit()
        flash(f'your product has been updated','success')
        return redirect(url_for('admin'))
    
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.color.data = product.color
    form.description.data = product.description
    return render_template('products/updateproduct.html', form=form,brands=brands,categories=categories,product=product)

@app.route('/deleteproduct/<int:id>',methods=['POST','GET'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(product)
        db.session.commit()
        flash(f'the product {product.name} was deleted','success')
        return redirect(url_for('admin'))
    flash(f'cant delete the product','danger')

    return redirect(url_for('admin'))
