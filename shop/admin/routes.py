from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
from flask_login import logout_user
import os


@app.route('/')
def landing():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/landing.html', brands=brands, categories=categories)

@app.route('/home')
def home():
     products = Addproduct.query.filter(Addproduct.stock > 0)
     brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
     categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
     return render_template('products/index.html', products=products, brands=brands, categories=categories)

@app.route('/aboutus')
def aboutus():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/aboutus.html', brands=brands, categories=categories)

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/single_page.html',product=product,brands=brands,categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand=brand,brands=brands,categories=categories)

@app.route('/category/<int:id>')
def get_cat(id):
    category = Addproduct.query.filter_by(category_id=id)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html', category=category,categories=categories,brands=brands)


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html',title='admin page', products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html',title="Brand page", brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html',title="category page", categories=categories)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data,email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thanks for registering','success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title="Registeration")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method =="POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email']= form.email.data
            flash(f'Welcome {form.email.data} you are loged in', 'success' )
            return redirect(request.args.get('next') or url_for('admin'))
            
        else:
            flash('wrong password please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('admin/login.html', form=form, title="login page")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing'))
