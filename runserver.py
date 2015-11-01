from restaurantApp import app

# on dev mod, use this file to bootstrap
# this will init the flask server, with debug
if __name__ == '__main__':
    
    host = '0.0.0.0'
    port = 5000

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run( host = host, port = port )