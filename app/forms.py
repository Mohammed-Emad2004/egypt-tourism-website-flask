from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, DataRequired, NumberRange, Optional, URL

class ContactForm(FlaskForm):
    FName = StringField('Enter your first name', validators=[DataRequired()])
    LName = StringField('Enter your last name', validators=[DataRequired()])
    email = StringField('Enter your email',validators=[DataRequired(),Email()])
    message = TextAreaField('Message',validators=[DataRequired(),Length(min=10)])
    submit= SubmitField('Send')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = SelectField('Country', choices=[
        ('US', 'United States / USA'),
        ('UK', 'United Kingdom / UK'),
        ('EG', 'Egypt / مصر'),
        ('SA', 'Saudi Arabia / السعودية'),
        ('AE', 'UAE / الإمارات'),
        ('FR', 'France / فرنسا'),
        ('ES', 'Spain / إسبانيا'),
        ('DE', 'Germany / ألمانيا'),
        ('OTHER', 'Other / دولة أخرى')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')
    
class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        ('5', '⭐⭐⭐⭐⭐ (5/5)'),
        ('4', '⭐⭐⭐⭐ (4/5)'),
        ('3', '⭐⭐⭐ (3/5)'),
        ('2', '⭐⭐ (2/5)'),
        ('1', '⭐ (1/5)')
    ], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField('Submit Review')
    
class FlightBookingForm(FlaskForm):
    departure = StringField('Departure City', validators=[DataRequired(), Length(min=2, max=50)])
    travel_date = StringField('Travel Date', validators=[DataRequired()])
    submit = SubmitField('Confirm Booking')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password') 
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Save Changes')
    
class AddPlaceForm(FlaskForm):
    name = StringField('Place Name', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    hook = StringField('Hook', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    transportation = StringField('transportation', validators=[DataRequired()])
    activities = StringField('Activities', validators=[DataRequired()])
    best_time = StringField('Best Time to Visit', validators=[DataRequired()])
    image_file = StringField('Image Filename', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=0, max=5, message='Rating must be between 0 and 5')])
    submit = SubmitField('Add Place')
    booking_url = StringField('Booking URL', validators=[Optional(), URL()])
    location_url = StringField('Location URL', validators=[Optional(), URL()])