#!/usr/bin/env python
from evesrp import app

import config

app.config.from_object(config.Development)
app.config['USER_AGENT_EMAIL'] = 'paxswill@paxswill.com'
app.run()
