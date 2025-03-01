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
import offchain_compass as OffInitializer 
import cwtdb_controller as CWTInterface
from utils import base_plugins as base

#import Twilio_Content_Provider as Twilio_Service
app=Flask(__name__)
sslify = SSLify(app)
app.config.update(
    PERMANENT_SESSION_LIFETIME = 600 ,
)
cors = CORS(app , resources = {r"/*" : {"origins" : "*" }})


StorySets  = os.path.join(app.static_folder , "Sources" , "assets" , "img" , "Stories")  
app.config['StorySets']= StorySets

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
    def dispatch_request(self , AccountAddress ) -> str : 
        # Retreiving All Available stories offchain 
        Article_Listings = CWTInterface.Print_All_Stories()
        # Retreiving All Available Users offchain  
        Account_Profiles =  CWTInterface.Print_Aggragate_Profiles()
        # Retreival of Comments Per Article Cant Be Done Thru a one time init 
        # Due to the dynamicness of data in the system therefore  
        # We'll have to introduce a function that returns data based on articleid  provided while 
        # laveraging the comments_per_article db-impl at the same time 

        def Render_Article_Commentary(ArticleID):
            NoComments = " No comments exist relating to the content - " + str(ArticleID) 
            if(CWTInterface.Render_Comments_Per_Article(ArticleID)):
                Commentary = CWTInterface.Render_Comments_Per_Article(ArticleID) 
                return Commentary
            else:
                return NoComments

        # Reendering Article Related Pictures Available in the system 
        # This returns a list of items available in a set folder  



        def Return_StorySets(ArticleID): 
            if(ArticleID):
                FixedPath =  os.path.join(app.static_folder , StorySets , ArticleID ) 
            print(os.listdir(FixedPath))
            return os.listdir(FixedPath)




        # Reendering Article Related Pictures Available in the system 
        # This returns a list of items available in a set folder  


        def Render_Board_Adverts(): 
            FixedPath =  os.path.join(app.static_folder , "Sources" , "assets" , "img" ,  "Advertisements") 
            print(os.listdir(FixedPath))
            return os.listdir(FixedPath)





        Article_Volume = int(0)
        if not (Article_Listings):
            Article_Volume = int(0)
        else:
            Article_Volume = len(Article_Listings)
        
        if not (Account_Profiles):
            Account_Volume = int(0)
        else:
            Account_Volume = len(Account_Profiles)
        

        return render_template('Listings.html' , AccountAddress = AccountAddress , Article_Listings = Article_Listings  , Article_Volume = Article_Volume , Account_Profiles = Account_Profiles  , Account_Volume = Account_Volume , Render_Article_Commentary = Render_Article_Commentary  , Return_StorySets = Return_StorySets , Render_Board_Adverts = Render_Board_Adverts)




@app.route("/Comments/<string:AcctAddress>/<string:ArticleID>/" , methods=["POST" , "GET"])
def Commentative_Post_Sections(AcctAddress , ArticleID ):
    Data = request.form.get("SubjectLine")
    Comment_Post = []
    for Attribute in AcctAddress , ArticleID , Data , base.Space_Time_Generator("TimeInt") , base.Space_Time_Generator("DateStr")  :
        Comment_Post.append(Attribute)
    print(Comment_Post)
    # Appending Data to the DB 
    if(CWTInterface.Create_Comment(Comment_Post)):
    # Here manage this route by returning alerts if Comment Post was successfull 
        return redirect(url_for('Blogs' , AccountAddress = AcctAddress ))
    else:
        return redirect(url_for('Blogs' , AccountAddress = AcctAddress ))
    # Generally Returning the Tempplate 
    return redirect(url_for('Blogs' , AccountAddress = AcctAddress ))


@app.route("/Create/Story/<string:AccountAddr>/" , methods=['POST'])
def Create_Story_Mode(AccountAddr):
        Datapoint = []
        CategoryLine = request.form.get("Category")
        SubjectMatter = request.form.get("Subject")
        file = request.files['MediaStories']
        print(file.filename)
        # Test for SubjectMatter 
        #print("This is now called" , SubjectMatter)
        if(SubjectMatter):
            # Here we return to the dashboard with a successfull story creation 
            # Notify the user that all went well 

        
            # Secondly lets add the story to the database 
            # Reflect with image files presented which will be sent to universal id | location 

            for dataclip in base.Construct_String_Address(8) , AccountAddr , CategoryLine , int(0) , SubjectMatter , int(0) , base.Space_Time_Generator("DateStr") , base.Space_Time_Generator("TimeInt") :
                Datapoint.append(dataclip)

            # Handle FOrm Submission
            # NOTE : We need to create a directory that will hold data for the pictures created  
            # Without this A function dependent on this directory will raise an alarm : lets proceed 

            if(CWTInterface.Create_Story(Datapoint)):
            # Creating Directory Fpr The Said DAta
            # Critical Data obtn from Dpoint[0] 

                os.mkdir(os.path.join(app.static_folder , "Sources" , "assets" , "img" , "Stories" , Datapoint[0]))
                print("Physicall path" , os.path.join(app.static_folder , "Sources" , "assets" , "img" , "Stories" , Datapoint[0]))
                file.save(os.path.join(app.config['StorySets'] , Datapoint[0] , file.filename ))

            # This means that our story was created successfully notify the user 
                return redirect(url_for('Blogs' , AccountAddress = AccountAddr))
            else: 
            # THis means that our stiry wasnt creaeted  
            # Convince the user to try again 
                return redirect(url_for('Blogs' , AccountAddress = AccountAddr))
        
        return redirect(url_for('Blogs' , AccountAddress = AccountAddr))

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
