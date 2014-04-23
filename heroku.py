#!/usr/bin/env python
from evesrp import create_app
from evesrp.killmail import CRESTMail, ShipURLMixin
from evesrp.auth.testauth import TestAuth
from os import environ as env
from binascii import unhexlify


skel_url = 'https://wiki.eveonline.com/en/wiki/{name}'

class EOWikiCREST(CRESTMail, ShipURLMixin(skel_url)): pass


app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = env['DATABASE_URL']
app.config['SECRET_KEY'] = unhexlify(env['SECRET_KEY'])
app.config['USER_AGENT_EMAIL'] = 'paxswill@paxswill.com'
app.config['AUTH_METHODS'] = [TestAuth()]
app.config['CORE_AUTH_PRIVATE_KEY'] = env.get('CORE_PRIVATE_KEY')
app.config['CORE_AUTH_PUBLIC_KEY'] = env.get('CORE_PUBLIC_KEY')
app.config['CORE_AUTH_IDENTIFIER'] = env.get('CORE_IDENTIFIER')
app.config['KILLMAIL_SOURCES'] = [EOWikiCREST]
if env.get('DEBUG') is not None:
    app.debug = True


if __name__ == '__main__':
    # So we get the database tables for these
    from evesrp.auth.testauth import TestUser, TestGroup
    print("Creating databases...")
    app.extensions['sqlalchemy'].db.create_all(app=app)