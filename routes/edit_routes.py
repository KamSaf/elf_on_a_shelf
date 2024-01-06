from flask import render_template, redirect, url_for, request, flash, Blueprint
from config import app, db
from models import Package, Elf, Holiday
from datetime import datetime


edit_bp = Blueprint('edit', __name__)


@app.route('/edit_package/<int:package_id>', methods=['POST', 'GET'])
def edit_package(package_id):
    if request.method == 'GET':
        elves = Elf.query.filter_by(active=True).all()
        old_package = Package.query.filter_by(id=package_id).first()
        if old_package.elf_id:
            old_elf = Elf.query.filter_by(id=old_package.elf_id).first()
        else:
            old_elf = None
        return render_template('edit_package.html', old_package=old_package, elves=elves, old_elf=old_elf)
    elif request.method == 'POST':
        edited_package = Package.query.filter_by(id=package_id).first()
        if edited_package.elf_id != request.form.get('frm_elf'):
            old_elf = Elf.query.filter_by(id=edited_package.elf_id).first()
            old_elf.assigned -= 1

            new_elf = Elf.query.filter_by(id=request.form.get('frm_elf')).first()
            new_elf.assigned += 1
            db.session.merge(old_elf)
            db.session.merge(new_elf)
            db.session.commit()

        edited_package.elf_id = request.form.get('frm_elf')
        edited_package.title = request.form.get('frm_title')
        edited_package.delivery_date = datetime.strptime(request.form.get("frm_delivery_date"), "%Y-%m-%d")
        edited_package.receiver = request.form.get('frm_receiver')

        with app.app_context():
            db.session.merge(edited_package)
            db.session.commit()
        return redirect(url_for("home_page"))


@app.route('/edit_elf/<int:elf_id>', methods=['POST', 'GET'])
def edit_elf(elf_id):
    if request.method == 'GET':
        old_elf = Elf.query.filter_by(id=elf_id).first()
        return render_template('edit_elf.html', old_elf=old_elf)
    elif request.method == 'POST':
        edited_elf = Elf.query.filter_by(id=elf_id).first()
        edited_elf.name = request.form.get('frm_name')
        edited_elf.surname = request.form.get('frm_surname')
        with app.app_context():
            db.session.merge(edited_elf)
            db.session.commit()
        return redirect(url_for("home_page"))


@app.route('/edit_holiday/<int:holiday_id>', methods=['POST', 'GET'])
def edit_holiday(holiday_id):
    if request.method == 'GET':
        old_holiday = Holiday.query.filter_by(id=holiday_id).first()
        assigned_elf = Elf.query.filter_by(id=holiday_id).first()
        return render_template('edit_holiday.html', old_holiday=old_holiday, assigned_elf=assigned_elf)
    elif request.method == 'POST':
        if datetime.strptime(request.form.get("frm_start_date"), "%Y-%m-%d") > datetime.strptime(request.form.get("frm_end_date"), "%Y-%m-%d"):
            flash('End date cannot occur before start date!', 'error')
            return redirect(url_for('edit_holiday', holiday_id=holiday_id))
        edited_holiday = Holiday.query.filter_by(id=holiday_id).first()
        edited_holiday.elf_id = request.form.get('frm_elf')
        edited_holiday.type = request.form.get('frm_type')
        edited_holiday.start_date = datetime.strptime(request.form.get("frm_start_date"), "%Y-%m-%d")
        edited_holiday.end_date = datetime.strptime(request.form.get("frm_end_date"), "%Y-%m-%d")
        with app.app_context():
            db.session.merge(edited_holiday)
            db.session.commit()
        return redirect(url_for("home_page"))
