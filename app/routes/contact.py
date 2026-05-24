from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.data import ui_texts
from app.forms import ContactForm
from app.models import db, ContactMessage

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    lang = request.args.get('lang', session.get('lang', 'en'))
    session['lang'] = lang
    ui = ui_texts.get(lang, ui_texts.get('en'))
    form = ContactForm()
    
    if form.validate_on_submit():
        new_msg = ContactMessage(
            first_name=form.FName.data,
            last_name=form.LName.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_msg)
        db.session.commit()
        
        flash(ui.get('msg_contact_success', 'Your message has been sent successfully!'), 'success')
        return redirect(url_for('contact.contact', lang=lang))
    return render_template('contact.html', ui=ui, lang=lang, dir=ui['dir'], form=form)