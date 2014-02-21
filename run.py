from application import app


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app.run(host='0.0.0.0', debug=True)