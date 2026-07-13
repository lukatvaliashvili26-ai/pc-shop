from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, Account, Component, UserCart
from forms import SignUpForm, SignInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neon-cyber-secret-2026'
# app.py-ის თავში, სადაც კონფიგურაციაა
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_mgr = LoginManager(app)
login_mgr.login_view = 'signin'
login_mgr.login_message_category = 'warning'


@login_mgr.user_loader
def load_account(uid):
    return Account.query.get(int(uid))


def init_components():
    if not Component.query.first():
        items = [
            Component(
                title="AMD Ryzen 7 7800X3D",
                tech_type="CPU",
                cost=400,
                info="საუკეთესო გეიმერული პროცესორი.",
                img_link="images/cpu.jpg"  # აუცილებლად დაუმატეთ images/ თავში
            ),
            Component(
                title="ASUS ROG Strix RTX 4070 Ti",
                tech_type="GPU",
                cost=950,
                info="მძლავრი ვიდეობარათი.",
                img_link="images/gpu.jpg"
            ),
            Component(
                title="Kingston FURY 16GB DDR5",
                tech_type="RAM",
                cost=85,
                info="სტაბილური და სწრაფი მეხსიერება.",
                img_link="images/ram.jpg"
            ),
            Component(
                title="Crucial P3 Plus 1TB",
                tech_type="SSD",
                cost=75,
                info="სწრაფი მაღალი ხარისხის NVMe SSD.",
                img_link="images/ssd.jpg"
            )
        ]
        db.session.add_all(items)
        db.session.commit()

@app.route('/')
@app.route('/catalog')
def catalog():
    search = request.args.get('find', '')
    t_filter = request.args.get('type', '')

    q = Component.query
    if search:
        q = q.filter(Component.title.contains(search))
    if t_filter:
        q = q.filter_by(tech_type=t_filter)

    hardware = q.all()
    return render_template('catalog.html', hardware=hardware)


@app.route('/item/<int:item_id>')
def item_view(item_id):
    obj = Component.query.get_or_404(item_id)
    return render_template('item_detail.html', obj=obj)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('catalog'))
    f = SignUpForm()
    if f.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(f.secure_password.data).decode('utf-8')
        acc = Account(nickname=f.nickname.data, email_address=f.email_address.data, secure_password=pw_hash)
        db.session.add(acc)
        try:
            db.session.commit()
            flash('ექაუნთი შეიქმნა! გაიარეთ ავტორიზაცია.', 'success')
            return redirect(url_for('signin'))
        except:
            db.session.rollback()
            flash('მონაცემები უკვე დაკავებულია.', 'danger')
    return render_template('signup.html', form=f)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('catalog'))
    f = SignInForm()
    if f.validate_on_submit():
        acc = Account.query.filter_by(email_address=f.email_address.data).first()
       if acc and bcrypt.check_password_hash(acc.secure_password, f.secure_password.data):
            login_user(acc)
            return redirect(url_for('catalog'))
        else:
            flash('არასწორი ფოსტა ან პაროლი.', 'danger')
    return render_template('signin.html', form=f)


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('catalog'))


@app.route('/mycart')
@login_required
def mycart():
    elements = UserCart.query.filter_by(account_id=current_user.id).all()
    total = sum(el.item.cost for el in elements)
    return render_template('mycart.html', elements=elements, total=total)


@app.route('/push_to_cart/<int:el_id>')
@login_required
def push_to_cart(el_id):
    new_item = UserCart(account_id=current_user.id, component_id=el_id)
    db.session.add(new_item)
    db.session.commit()
    flash('კომპონენტი დაემატა!', 'success')
    return redirect(url_for('catalog'))


@app.route('/drop_from_cart/<int:c_id>')
@login_required
def drop_from_cart(c_id):
    target = UserCart.query.get_or_404(c_id)
    if target.account_id == current_user.id:
        db.session.delete(target)
        db.session.commit()
        flash('წაიშალა კალათიდან.', 'info')
    return redirect(url_for('mycart'))


@app.route('/order_finish')
@login_required
def order_finish():
    UserCart.query.filter_by(account_id=current_user.id).delete()
    db.session.commit()
    flash('შეკვეთა რეგისტრირებულია!', 'success')
    return redirect(url_for('catalog'))


with app.app_context():
    db.create_all()
    init_components()

if __name__ == '__main__':
    app.run(debug=True)

