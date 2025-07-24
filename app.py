from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import EmployeeForm
from models import db, Employee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def index():
    department = request.args.get('department')
    if department:
        employees = Employee.query.filter_by(department=department).all()
    else:
        employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_emp = Employee(
            name=form.name.data,
            position=form.position.data,
            department=form.department.data,
            salary=form.salary.data
        )
        db.session.add(new_emp)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    emp = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=emp)
    if form.validate_on_submit():
        form.populate_obj(emp)
        db.session.commit()
        flash('Employee updated successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    emp = Employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
