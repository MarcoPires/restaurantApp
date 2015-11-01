from runserver import app
# default app bootstrap, init the flask server
app.secret_key = 'super_secret_key'
app.run( host = '0.0.0.0', port = 5000 )