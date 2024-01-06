from flask import render_template, redirect, url_for, request, Blueprint
from config import app, db
from models import Package, Elf, Holiday
from datetime import datetime

main_bp = Blueprint('main', __name__)


@app.route('/')
def home_page():
    elves = Elf.query.filter_by(active=True).all()
    holidays = Holiday.query.filter_by(deleted=False).all()
    packages = Package.query.filter_by(deleted=False).all()
    return render_template('home.html', packages=packages, elves=elves, holidays=holidays, current_datetime=datetime.now())


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/update_package', methods=['POST'])
def update_package():
    package_to_mark = Package.query.filter_by(id=request.form.get('frm_package_id')).first()
    assigned_elf = Elf.query.filter_by(id=package_to_mark.elf_id).first()
    with app.app_context():
        package_to_mark.delivered = True
        db.session.merge(package_to_mark)
        if assigned_elf.assigned > 0:
            assigned_elf.assigned -= 1
            db.session.merge(assigned_elf)
        db.session.commit()
    return redirect(url_for("home_page"))
