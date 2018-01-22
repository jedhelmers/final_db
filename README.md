# Welcome to my catalog!

I ripped all the items off of the Target website, pared it with some
random stuff from excel then created a basket system using OAuth for Flask.

Basically, one logs in with Google, the page checks if the user exists,
if not, it adds that user to a table, else, it pulls the users basket.

The database was designed to expand for future products other than electronics.
The templates would need to change a little, but that's mostly cosmetic.

I've created some API's for debugging:

* '/basket' will export ALL ITEMS in ALL BASKTS.
  This lets me keep track of how the data enters the table.

* '/users/JSON' exports the users with accounts and their user ids.

* '/catalog/basket/JSON' exports the contents of a user's basket.

* '/catalog/TV/all/all/JSON' exports ALL items displayed on the front page.
  If the filters in the sidebar are applied, the API will adjust. For example:
  '/catalog/TV/43/all/JSON' exports data for two 43" TVs.

* '/all' displays all items on the screen.

* '/delete' Delete a user's basket.

* '/delete/users' Deletes all users AND their baskets.


In your vagrant command line, run python lotsofTVs.py. This will setup
the database and tables. It will also fill it with catalog data.

Now, run python Final_Catalog.py. This initiates localhost:5000

Run http://localhost:5000/catalog/TV/all/all in your browser. Login with your
Google account. Fill your cart. Edit quantities. Play around with the
aforementioned APIs.

Clicking on your Account Icon will log you out. Login with a different
Google account. This will create a new account in the User table
and will assign it a userid. Items entered into this account's basket
belong to this user and this user alone.
