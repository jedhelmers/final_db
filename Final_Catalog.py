from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Item, User, Basketz
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']


engine = create_engine('sqlite:///productcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(User=[user.serialize for user in users])


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 80%; height: 80%;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html')

    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/catalog/TV/<string:size_id>/<string:brand_id>')
def showCatalogAll(brand_id, size_id):

    check = login_session.get('username')
    checkName = session.query(User).filter_by(name = check).first()

    if checkName:
        checkName = "nome"

    if check != None and checkName != 'nome':
        newUser = User(name = login_session['username'])
        session.add(newUser)
        session.commit()

    if (brand_id == 'all' and size_id =='all'):
        items = session.query(Item).all()
    elif (brand_id != 'all' and size_id == 'all'):
        items = session.query(Item).filter_by(brand = brand_id)
    elif (brand_id == 'all' and size_id != 'all'):
        items = session.query(Item).filter_by(size = size_id)
    else:
        items = session.query(Item).filter_by(brand = brand_id, size = size_id)

    brands = session.query(Item).distinct(Item.brand).group_by(Item.brand).all()
    sizes = session.query(Item).distinct(Item.size).group_by(Item.size).all()
    return render_template('catalog.html', check = check, items = items, brands = brands, sizes = sizes, login_session = login_session)

@app.route('/catalog/TV/<string:size_id>/<string:brand_id>/JSON')
def showCatalogJSON(brand_id, size_id):

    if (brand_id == 'all' and size_id =='all'):
        items = session.query(Item).all()
    elif (brand_id != 'all' and size_id == 'all'):
        items = session.query(Item).filter_by(brand = brand_id)
    elif (brand_id == 'all' and size_id != 'all'):
        items = session.query(Item).filter_by(size = size_id)
    else:
        items = session.query(Item).filter_by(brand = brand_id, size = size_id)
    return jsonify(Item=[item.serialize for item in items])


@app.route('/catalog/basket/JSON')
def showBasketJSON():
    user = session.query(User).filter_by(name = login_session['username']).first()
    items = session.query(Basketz).filter_by(userid = user.userid)
    return jsonify(Basketz=[item.serialize for item in items])

#Item details page with qty adjustment
@app.route('/catalog/<int:id>/', methods = ['GET', 'POST'])
def editItem(id):

    user = session.query(User).filter_by(name = login_session['username']).first()

    item = session.query(Item).filter_by(id = id).one()

    brands = session.query(Item).distinct(Item.brand).group_by(Item.brand).all()
    sizes = session.query(Item).distinct(Item.size).group_by(Item.size).all()

    basketItem = session.query(Basketz).filter_by(userid = user.userid, itemid = id).first()
    if request.method == 'POST':
        if basketItem:
            basketItem.qty = int(request.form['qty'])
        else:
            basketItem = Basketz(itemid = id, userid = user.userid, qty = request.form['qty'])
        session.add(item)
        session.commit()
        return redirect(url_for('showCatalogAll', brand_id = 'all', size_id = 'all'))
    else:
        return  render_template('editCart.html', login_session = login_session, item = item, brands = brands, sizes = sizes, basket = basketItem)



#Item details page with qty adjustment
@app.route('/catalog/<int:id>/additem', methods = ['GET', 'POST'])
def addItem(id):
    check = login_session.get('username')
    if check != None:
        newItem = session.query(Basketz).filter_by(itemid = id).first()
        user = session.query(User).filter_by(name = login_session['username']).first()

        if request.method == 'POST':
            if newItem:
                newItem.qty = int(request.form['qty'])
            else:
                newItem = Basketz(itemid = id, userid = user.userid, qty = request.form['qty'])

            session.add(newItem)
            session.commit()
            return redirect(url_for('showCatalogAll', brand_id = 'all', size_id = 'all'))
        else:
            return render_template('addItem.html', id = id)
    else:
        return redirect('showCatalogAll')
#Shows basket contents
@app.route('/basket')
def showBasket():
    baskets = session.query(Basketz).all()
    output = ""
    for basket in baskets:
        if basket.itemid != 0:
            item = session.query(Item).filter_by(id = basket.itemid).one()
            output += "Item ID: " + str(basket.itemid) + "</br>"
            output += "Item description: " + str(item.description) + "</br>"
            output += "Basket ID: " + str(basket.basketid) + "</br>"
            output += "Qty: " + str(basket.qty) + "</br>"
            output += "User ID: " + str(basket.userid) + "</br></br>"
    if output != "":
        return output
    else:
        return "Empty basket!"

#Shows all items
@app.route('/all')
def showItems():
    baskets = session.query(Item).all()
    output = ""
    for basket in baskets:
        #item = session.query(Item).filter_by(id = basket.itemid).one()
        output += "Basket index: " + str(basket.id) + "</br>"
        #output += "Item description: " + str(item.description) + "</br>"
        output += "Item description: " + str(basket.description) + "</br>"
        output += "Brand: " + str(basket.brand) + "</br>"
        output += "Price: " + str(basket.price) + "</br></br>"

    return output

@app.route('/catalog/<int:id>/delete', methods = ['GET', 'POST'])
def deleteItem(id):
    user = session.query(User).filter_by(name = login_session['username']).first()
    item = session.query(Item).filter_by(id = id).one()

    brands = session.query(Item).distinct(Item.brand).group_by(Item.brand).all()
    sizes = session.query(Item).distinct(Item.size).group_by(Item.size).all()
    return render_template('editCart.html', item = item, brands = brands, sizes = sizes, user = user)



#Delete user's basket
@app.route('/delete')
def deleteBasket():
    user = session.query(User).filter_by(name = login_session['username']).first()
    basket = session.query(Basketz).filter_by(userid = user.userid).delete()
    session.commit()
    return "%s's basket is empty!" % user.name


#Delete all users and their baskets.
@app.route('/delete/users')
def deleteUsers():
    basket = session.query(Basketz).delete()
    user = session.query(User).delete()
    session.commit()
    return "All users deleted!"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
