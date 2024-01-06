from flask import render_template, redirect, url_for, request
from config import app, db
from models import Package, Elf, Holiday
from datetime import datetime


@app.route('/')
def home_page():
    elves = Elf.query.filter_by(active=True).all()
    holidays = Holiday.query.filter_by(deleted=False).all()
    packages = Package.query.filter_by(deleted=False).all()
    return render_template('home.html', packages=packages, elves=elves, holidays=holidays, current_datetime=datetime.now())


@app.route('/about')
def about_page():
    return render_template('about.html')


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
def edit_holiday_form(holiday_id):
    if request.method == 'GET':
        old_holiday = Holiday.query.filter_by(id=holiday_id).first()
        assigned_elf = Elf.query.filter_by(id=holiday_id).first()
        return render_template('edit_holiday.html', old_holiday=old_holiday, assigned_elf=assigned_elf)
    elif request.method == 'POST':
        edited_holiday = Holiday.query.filter_by(id=holiday_id).first()
        edited_holiday.elf_id = request.form.get('frm_elf')
        edited_holiday.type = request.form.get('frm_type')
        edited_holiday.start_date = datetime.strptime(request.form.get("frm_start_date"), "%Y-%m-%d")
        edited_holiday.end_date = datetime.strptime(request.form.get("frm_end_date"), "%Y-%m-%d")
        with app.app_context():
            db.session.merge(edited_holiday)
            db.session.commit()
        return redirect(url_for("home_page"))







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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.jinja_env.globals.update(to_datetime=datetime.strptime)
    app.run(debug=True)
