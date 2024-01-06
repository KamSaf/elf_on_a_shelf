from flask import redirect, url_for, request, Blueprint
from config import app, db
from models import Package, Elf, Holiday


delete_bp = Blueprint('delete', __name__)


@app.route('/delete_elf', methods=["POST"])
def delete_elf():
    elf_id = request.form.get('frm_item_id')
    elf_to_delete = Elf.query.filter_by(id=elf_id).first()
    holidays_to_delete = Holiday.query.filter_by(elf_id=elf_id).all()
    packages_to_unassign = Package.query.filter_by(elf_id=elf_id).all()
    with app.app_context():
        for holiday in holidays_to_delete:
            holiday.deleted = True
            db.session.merge(holiday)
        for package in packages_to_unassign:
            package.elf_id = None
            db.session.merge(package)
        elf_to_delete.active = False
        db.session.merge(elf_to_delete)
        db.session.commit()
    return redirect(url_for("home_page"))


@app.route('/delete_package', methods=["POST"])
def delete_package():
    package_to_delete = Package.query.filter_by(id=request.form.get('frm_item_id')).first()
    if package_to_delete.elf_id:
        assigned_elf = Elf.query.filter_by(id=package_to_delete.elf_id).first()
    else:
        assigned_elf = None
    with app.app_context():
        package_to_delete.deleted = True
        db.session.merge(package_to_delete)
        if assigned_elf and assigned_elf.assigned > 0:
            assigned_elf.assigned -= 1
            db.session.merge(assigned_elf)
        db.session.commit()
    return redirect(url_for("home_page"))


@app.route('/delete_holiday', methods=["POST"])
def delete_holiday():
    holiday_to_delete = Holiday.query.filter_by(id=request.form.get('frm_item_id')).first()
    with app.app_context():
        holiday_to_delete.deleted = True
        db.session.merge(holiday_to_delete)
        db.session.commit()
    return redirect(url_for("home_page"))
