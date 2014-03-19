from . import app, auth_methods

from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, login_required
from flask.ext.wtf import Form
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired

class SelectValueField(SelectField):
    def _value(self):
        return self.default if self.default is not None else ''

class LoginForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    auth_method = SelectValueField('Authentication Source', default=0,
            choices=[(i, m.method_name) for i, m in enumerate(auth_methods)],
            coerce=int)


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if len(auth_methods) < 2:
        form.auth_method.widget = HiddenInput()
    if form.validate_on_submit():
        print('Form validated')
        method = auth_methods[form.auth_method.data]
        user = method.authenticate_user(form.username.data, form.password.data)
        if user is not None:
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))


    return render_template('login.html', form=form)