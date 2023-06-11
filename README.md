# PPY1
Author: Anonyo Mitra(s25833@pjwstk.edu.pl)
# Features:
* ## Accounts: 
  Login/Signup system, using bcrypt to encrypt stored passwords
  On signup the system uses ip-api.com api to get the location of the user and stores it in user locations
  (since we are running this server locally there is a patchwork system where if the user's ip is 127.0.0.1
  the system will use the api to obtain it's own location.)
* ## Front/Back End:
   As required there are to fast api servers, front end listening on port 5000 accepts HTTP requests from the
   browser, sends the data to the backend server listening on port 5001, the back end server connects to a mysql
   server situated on dbserver.anonyo.net using sqlAlchemy.
* ## Weather:
    api.open-meteo.com is used to obtain current/hourly weather data using any given coordinates.
* ## Time: 
    The data obtained from open-metro is in GMT time so ip-api is used again to obtain the timezone of at
    user's ip location. Pytz package is then used to convert the times in the date to the user's timezone 
* ## Map:
    maps.googleapis.com is used on the webpage to display a map, allowing the user to select a point on the map
    coordinates of the point are obtained and sent to the server side to obtain weather information.
