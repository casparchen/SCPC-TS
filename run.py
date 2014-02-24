from application import app
from gevent.wsgi import WSGIServer
import sys
print 'server runing...'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


#app.run(host='0.0.0.0', debug=True)


http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
