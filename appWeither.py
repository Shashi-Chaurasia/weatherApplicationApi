# Import necessary libraries
from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps
import requests

# Create Flask app and set secret key for JWT
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

# Set the username and password for login
_userName = "api-connect"
_passWord = "fQx35X5FZUJ7bYSjPTDjn9Zj"

# Login API
@app.route('/login', methods=['POST','GET'])
def _loginUser():
    # Get username and password from request headers
    _authUserPass = request.authorization

    # Check if the username and password are correct
    if _authUserPass and _authUserPass.username == _userName and _authUserPass.password == _passWord:
        # If correct, generate JWT token with user details and set expiration time
        _authThoken = jwt.encode({'user': _authUserPass.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        print(_authThoken)
        # Return the token in a JSON response
        return jsonify({'token': _authThoken})

    # If incorrect, return unauthorized status
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Logout API
@app.route('/logout' ,methods=['POST','GET'])
def _logoutUser():
    # Return a success message for logout
    return jsonify({'message': 'Logged out successfully!'})

# JWT token verification decorator
def _tokenRequired(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Get the JWT token from request headers
        _getToken = None
        if 'x-access-token' in request.headers:
            _getToken = request.headers['x-access-token']

        # If token is missing, return unauthorized status
        if not _getToken:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Verify the token and get the user details
            _userData = jwt.decode(_getToken, app.config['SECRET_KEY'], algorithms=['HS256'])
            _currentUser = _userData['user']
        except:
            # If token is invalid, return unauthorized status
            return jsonify({'message': 'Token is invalid!'}), 401

        # Call the API function with the user details and other arguments
        return f(_currentUser, *args, **kwargs)

    return decorated

# Get Weather Information API
@app.route('/weather', methods=['GET'])
@_tokenRequired
def _getWetherInform(current_user):
    # Set the API key and list of cities to get weather information for
    _apiKey = '1943f181a532b1e3893cd979df052c81'
    _citiesInIndia =["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Visakhapatnam", "Bhopal", "Patna", " Ludhiana", "Agra", "Nashik", "Vadodara", "Faridabad", "Madurai", "Hubli–Dharwad", "Varanasi", "Salem", "Amritsar", "Allahabad", "Srinagar", "Vijayawada", "Raipur"]

    _weatherData = []

    # Loop through the cities and get weather information for each
    for _city in _citiesInIndia:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={_city}&APPID={_apiKey}'
        response = requests.get(url)
        _weatherData.append(response.json())

    # Pagination
    _page = request.args.get('page', default=1, type=int)
    _pageSize = 10
    _startIndex = (_page - 1) * _pageSize
    _endIndex = _startIndex + _pageSize
    _paginatedData = _weatherData[_startIndex:_endIndex]
    return jsonify({'weather_data': _paginatedData})

if __name__ == '__main__':
    app.run(port=5001, debug=True,use_reloader=True)
