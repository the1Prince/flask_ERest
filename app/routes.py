from  flask import render_template,flash, redirect, url_for
from werkzeug.utils import secure_filename

from app import app,db
from flask_login import logout_user,current_user, login_user, login_required
from app.models import staff as Staff,meal as Meal,menu as Menu
from app.forms import LoginForm, StaffRegister, MealForm,MenuForm
from flask import request
from werkzeug.urls import url_parse
import random,json
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import date
import calendar
from PIL import Image



ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
@app.route('/index')
def index():
    title = 'home'
    return render_template('index.html', title=title)


#@app.route('/service-worker.js',methods=['POST','GET'])
#def sw():
#    return app.send_static_file('js/service-worker.js'),200,{'Content-Type': 'text/javascript'}


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/login',methods=['POST','GET'])
def login():
    title='login'

    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        staff = Staff.query.filter_by(username=form.username.data).first()
        if staff is None or not check_password_hash(staff.password_harsh,form.password.data):
           # user= staff.query.filter_by(first_name=form.username.data).
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(staff, remember=form.remember_me.data)
        next_page = request.args.get('dashboard')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html',title=title,form=form)





@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', username=current_user.username))
    form = StaffRegister()
    ran = str(random.randint(100000, 900000))
    #j= json.dumps(ran)
    if form.validate_on_submit():

        #form.emp_no.data=ran
        date1=str(form.dob.data)
        pas = str(generate_password_hash(form.confirm.data))
        staff = Staff(emp_no=ran,dob=date1,name=form.name.data,username=form.username.data,gender=form.gender.data,email=form.email.data,phone=form.telephone.data,adress=form.address.data,position=form.position.data,password_harsh=pas)
        #staff.set_password(form.confirm.data)
        db.session.add(staff)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('staff_register.html', title='E-Restaurant | Register', form=form,ran=ran)





@app.route('/dashboard/<username>',methods=['GET','POST'])
@login_required
def dashboard(username):
    user = Staff.query.filter_by(username=username).first_or_404()
    return redirect(url_for('profile'))
    return render_template('dashboard.html', user=user, title='DC | dashboard')


@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form=StaffRegister
    return render_template('profile.html', title='ERestarant | Profile',form=form)


@app.route('/addmeal',methods=['GET','POST'])
@login_required
def addmeal():
    form=MealForm()
    #if request.method == 'POST':

    if form.validate_on_submit():
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            im = Image.open(file)
            #rgb_im = im.convert('RGB')

            fullname = 'app/static/'+form.name.data+'.png'
            im.save(fullname)
            #file.save(fullname)
        meal=Meal(name=form.name.data,description=form.description.data,price=form.price.data,img=fullname)
        db.session.add(meal)
        db.session.commit()
        return redirect(url_for('result'))




    return render_template('addMeal.html',form=form)


@app.route('/result',methods=['GET','POST'])
@login_required
def result():
    return render_template('result.html')




@app.route('/addmenu',methods=['GET','POST'])
@login_required
def addmenu():
    nam=[]
    form=MenuForm()
    meal=Meal.query.all()
    for m in meal:
        nam.append(m.name)
        print(m.name)
    if request.method == 'POST':
        req = request.form
        mname=req['meal_name']
        type=req['meal_type']
        week=req['weekday']
        menu = Menu(meal_name=mname,description=form.description.data,type=type,week_day=week)
        db.session.add(menu)
        db.session.commit()
        return redirect(url_for('result'))
    return render_template('addMenu.html',form=form,nam=nam)

@app.route('/menu',methods=['GET','POST'])
def menu():
    #list of menu
    menu=Menu.query.all()

    #get day of the week
    my_date = date.today()
    day=calendar.day_name[my_date.weekday()]
    #list of breakfast today
    breakfast=Menu.query.filter_by(week_day=day,type='breakfast').all()
    #list of lunch today
    lunch=Menu.query.filter_by(week_day=day,type='lunch').all()
    #list of dinner today
    dinner=Menu.query.filter_by(week_day=day,type='dinner').all()



    return render_template('menu.html',menu=menu,breakfast=breakfast,lunch=lunch,dinner=dinner)