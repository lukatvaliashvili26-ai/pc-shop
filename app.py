from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import db, Account, Component, UserCart
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neon-cyber-secret-2026'
# app.py-ის თავში, სადაც კონფიგურაციაა
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyber_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_mgr = LoginManager(app)
login_mgr.login_view = 'signin'
login_mgr.login_message_category = 'warning'


@login_mgr.user_loader
def load_account(uid):
    return db.session.get(Account, int(uid))


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
            ),
            Component(
                title="Intel Core i9-14900K",
                tech_type="CPU",
                cost=550,
                info="უძლიერესი პროცესორი სამუშაოდ და გეიმინგისთვის.",
                img_link="images/cpu2.jpg"
            ),
            Component(
                title="NVIDIA RTX 4090",
                tech_type="GPU",
                cost=1700,
                info="ყველაზე მძლავრი ვიდეოკარტა გეიმინგისთვის.",
                img_link="images/gpu2.jpg"
            ),
            Component(
                title="Samsung 990 Pro 2TB",
                tech_type="SSD",
                cost=190,
                info="ულტრა სწრაფი NVMe SSD.",
                img_link="images/ssd2.jpg"
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


@app.route('/reg', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = Account.query.filter_by(
            nickname=form.username.data
        ).first()

        if existing_user:
            flash("მომხმარებელი უკვე არსებობს", "danger")
            return render_template(
                "signup.html",
                form=form
            )


        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')


        new_user = Account(
            nickname=form.username.data,
            email_address=form.username.data + "@mail.com",
            secure_password=hashed_password
        )


        db.session.add(new_user)
        db.session.commit()


        flash(
            "რეგისტრაცია წარმატებულია",
            "success"
        )


        return redirect(
            url_for('signin')
        )


    return render_template(
        "signup.html",
        form=form)

@app.route('/log', methods=['GET','POST'])
def signin():

    form = LoginForm()


    if form.validate_on_submit():

        user = Account.query.filter_by(
            nickname=form.username.data
        ).first()


        if user and bcrypt.check_password_hash(
            user.secure_password,
            form.password.data
        ):

            login_user(user)

            return redirect(
                url_for('catalog')
            )


        flash(
            "არასწორი მომხმარებელი ან პაროლი",
            "danger"
        )


    return render_template(
        "signin.html",
        form=form
    )



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
