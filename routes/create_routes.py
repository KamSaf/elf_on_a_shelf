from flask import redirect, url_for, request, flash, Blueprint
from config import app, db
from models import Package, Elf, Holiday
from datetime import datetime


create_bp = Blueprint('create', __name__)


@app.route('/new_elf', methods=["POST"])
def new_elf():
    new_elf = Elf(name=request.form.get('frm_name'), surname=request.form.get('frm_surname'), assigned=0, hire_date=datetime.now(), active=True)
    with app.app_context():
        db.session.add(new_elf)
        db.session.commit()
    return redirect(url_for("home_page"))


@app.route('/new_package', methods=["POST"])
def new_package():
    new_package = Package(elf_id=request.form.get('frm_elf'),
                          title=request.form.get('frm_title'),
                          receiver=request.form.get('frm_receiver'),
                          delivery_date=datetime.strptime(request.form.get("frm_delivery_date"), "%Y-%m-%d"),
                          delivered=False,
                          deleted=False,
                          create_date=datetime.now())

    with app.app_context():
        db.session.add(new_package)
        elf = Elf.query.filter_by(id=request.form.get('frm_elf')).first()
        elf.assigned += 1
        db.session.commit()
    return redirect(url_for("home_page"))


@app.route('/new_holiday', methods=["POST"])
def new_holiday():
    if datetime.strptime(request.form.get("frm_start_date"), "%Y-%m-%d") > datetime.strptime(request.form.get("frm_end_date"), "%Y-%m-%d"):
        flash('End date cannot occur before start date!', 'error')
        return redirect(url_for('home_page'))
    new_holiday = Holiday(elf_id=request.form.get('frm_elf'),
                          type=request.form.get('frm_type'),
                          start_date=datetime.strptime(request.form.get("frm_start_date"), "%Y-%m-%d"),
                          end_date=datetime.strptime(request.form.get("frm_end_date"), "%Y-%m-%d"),
                          deleted=False,
                          create_date=datetime.now())
    with app.app_context():
        db.session.add(new_holiday)
        db.session.commit()
    return redirect(url_for("home_page"))
