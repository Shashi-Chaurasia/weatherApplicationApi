# WeatherApplicationApi
this api return the weather detail of 30 cities based on pagination with proper authentication

# step to run api
1.activate virtualenv or create your own virtualenv 
    # command : python3 -m venv /path/to/new/virtual/environment
    # activate : .\venv\Scripts\activate.ps1.

2.install requirements.txt file for install dependency
    #command : pip install -r requirements.txt

3. run the application using command
        #command : python appWeither.py

# Postman response step:

1. get access token using /login endpoint use below commad:
    curl command : 
        curl --location --request POST 'http://127.0.0.1:5001/login' \
--header 'Authorization: Basic YXBpLWNvbm5lY3Q6ZlF4MzVYNUZaVUo3YllTalBURGpuOVpq' \
--data ''

2. using the above curl command you will get the access token.

3. take access token as a header to call weatherAPi 
    . header  = key:"x-access-token" , value : accessToke from step 1
        Params = key:"page" , vale:int(pagenumber)


4. curl command to call weather Api to get data w.r.t paggination:
    curl --location 'http://127.0.0.1:5001/weather?page=1' \
--header 'x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYXBpLWNvbm5lY3QiLCJleHAiOjE2NzcwNjU3NjR9.q9N56O1Vx_cN09Rs2I00yTn2hW_w_wyyvcFcuT9-Kqc' \
--data ''

note: access Token will expire in 30 min.







   
