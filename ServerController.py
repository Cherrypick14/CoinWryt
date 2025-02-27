import asyncio
from flask import Flask  , url_for , render_template , request , redirect , send_from_directory
from jinja2 import Environment , FileSystemLoader
from flask.views import View
from flask import g
import os , random , string 
import json 
from werkzeug.utils import secure_filename
import time
import sqlite3
from sqlite3 import Error
from flask_cors import CORS 
import uuid
import datetime
from flask_sslify import SSLify



#import Twilio_Content_Provider as Twilio_Service
app=Flask(__name__)
sslify = SSLify(app)
app.config.update(
    PERMANENT_SESSION_LIFETIME = 600 ,
)
cors = CORS(app , resources = {r"/*" : {"origins" : "*" }})




@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(error):
  return render_template("404.html" , error = error)



class Authentication_Profile(View):
   methods = ['GET' , 'POST']  
   def dispatch_request(self) -> str :
        CompanyID = "CoinWryt"
        if request.method == 'GET':
            return render_template('Auth.html' , CompanyID = CompanyID  )
        elif request.method == 'POST': 
            AccountAddress = request.form.get('Address')
            # Subtle check for Account Address 
            # Remove this once we go live : only for testnet 
            if not AccountAddress : 
                AccountAddress = "0xd48e84bda5351d516b9cd9361fea27b086a93188/"
            # Return requested profile thru client connect 
            return redirect(url_for('Blogs' , CompanyID = CompanyID  , AccountAddress = AccountAddress ))
        else:
            return render_template('Auth.html' , CompanyID = CompanyID  )
        


class Company_Display_Profile(View):
   methods = ['GET']  
   def dispatch_request(self) -> str :
        CompanyID = "CoinWryt"
        if request.method == 'GET':
            return render_template('Display.html' , CompanyID = CompanyID  )
        else: 
            # Return requested profile thru client connect 
            return render_template('Display' , CompanyID = CompanyID  )
        
class Blog_List(View): 
    methods = ['GET'] 
    def dispatch_request(self , AccountAddress) -> str : 
        return render_template('Listings.html' , AccountAddress = AccountAddress)




class Dashboard_Display_Profile(View): 
    methods = ['GET'] 
    def dispatch_request(self , AccountAddr) -> str : 
        AccountAddress = "023948304282"
        return render_template('Dashboard.html' , AccountAddress = AccountAddress)


app.add_url_rule('/', view_func=Company_Display_Profile.as_view('Home'))
app.add_url_rule('/Dashboard/<string:AccountAddr>/', view_func=Dashboard_Display_Profile.as_view('Dash'))
app.add_url_rule('/Login/' , view_func = Authentication_Profile.as_view('Auth'))
app.add_url_rule('/Dashboard/Blog/Listings/<string:AccountAddress>/' , view_func = Blog_List.as_view('Blogs'))



if __name__=='__main__':
   app.run(host="0.0.0.0" , debug="False" )
