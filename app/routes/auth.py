from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.forms import RegisterForm, LoginForm
from app.models import db, User
from app.data import ui_texts
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

COUNTRY_LANG_MAP = {
    'EG': 'ar', 'SA': 'ar', 'AE': 'ar',
    'FR': 'fr',                        
    'ES': 'es',                        
    'DE': 'de'                         
}

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    lang = request.args.get('lang', session.get('lang', 'en'))
    ui = ui_texts.get(lang, ui_texts.get('en'))
    form = RegisterForm()
    
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(ui.get('err_email', 'Email already registered'), 'danger')
        else:
            hashed_pw = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                country=form.country.data,
                password_hash=hashed_pw,
                role='user'
            )
            db.session.add(new_user)
            db.session.commit()
            
            user_lang = COUNTRY_LANG_MAP.get(form.country.data, 'en')
            session['lang'] = user_lang
            return redirect(url_for('auth.login', lang=user_lang))
            
    return render_template('register.html', ui=ui, lang=lang, dir=ui['dir'], form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    lang = request.args.get('lang', session.get('lang', 'en'))
    ui = ui_texts.get(lang, ui_texts['en'])
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role    
            user_lang = COUNTRY_LANG_MAP.get(user.country, 'en')
            session['lang'] = user_lang
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard', lang=user_lang))
            return redirect(url_for('home.home', lang=user_lang))
        else:
            flash(ui.get('err_match', 'Invalid Credentials'), 'danger')
            
    return render_template('login.html', ui=ui, lang=lang, dir=ui['dir'], form=form)

@auth_bp.route('/logout')
def logout():
    lang = session.get('lang', 'en')
    session.clear()
    session['lang'] = lang
    return redirect(url_for('home.home', lang=lang))