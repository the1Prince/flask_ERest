from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, BooleanField, PasswordField, RadioField, SubmitField, TextAreaField, SelectField,DecimalField,FileField
from wtforms.fields.html5 import EmailField,DateField
from wtforms.validators import DataRequired,ValidationError,EqualTo
from app.models import staff as Staff


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log me In')


class StaffRegister(FlaskForm):
    #emp_no = StringField('emp_no',validators=[DataRequired()])
    name = StringField('Fullname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    telephone = StringField('Telephone')
    dob = DateField('Date of birth')
    gender = RadioField(choices=[('male','male'),('female','female')], validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    position = StringField('Position',validators=[DataRequired()])
    password =  PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Staff.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Staff.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class MenuForm(FlaskForm):
    meal_name = StringField('Meal', validators=[DataRequired()])
    description = TextAreaField('Description')
    type = SelectField('Type of meal', choices=[('breakfast','breakfast'),('lunch','lunch'),('dinner','dinner')])
    week_day = SelectField('Day of the week', choices=[('sunday','sunday'),('monday','monday'),('tuesday','tuesday'),('wednesday','wednesday'),('thursday','thursday'),('friday','friday'),('saturday','saturday')])
    submit = SubmitField('Submit')

class MealForm(FlaskForm):
    name= StringField('Meal', validators=[DataRequired()])
    description= TextAreaField('Description')
    price= DecimalField('Price',places=2, validators=[DataRequired()])
    img= FileField()
    submit = SubmitField('Submit')
