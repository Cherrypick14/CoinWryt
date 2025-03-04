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
   def Create_Profile_Avatar(self) -> list :
    FixedPath = os.path.join(app.static_folder , "Sources" , "assets" , "img" ,  "Avatars" ) 
    if(FixedPath):
        Collectives  = list(os.listdir(FixedPath))
        #Remember to check for empty randrange here   as getting nill collectives 
        #throws error :  empty rand range in executor ::   

        RangeSlice = random.randrange(0,len(Collectives))  
        return Collectives[RangeSlice]
    else: 
        return "Couldnt Generate Profile Image "


   def dispatch_request(self) -> str :
        CompanyID = "CoinWryt"
        User_Account_Data =  []
        if request.method == 'GET':
            return render_template('Auth.html' , CompanyID = CompanyID  )
        elif request.method == 'POST': 
            Address = request.form.get('WalletAddress')
            Username = request.form.get('CustomName')
            # Minor ommissions 
            if not Username: 
                Username = "Unknown"
            # We need to check if the said address erxists offchain 
            # If so , then this a validly created account under Coinwryt 
            # Else throw off a UNI error and enforce account abtstraction 
            if(CWTInterface.Confirm_Acc_Visibility(Address)):
                # Account Address Exists Offchain 
                # Update minor details on chain 
                return redirect(url_for('Blogs' ,  AccountAddress = Address ))
            else:
                # Register Wallet Account Activities  
                # Creation Of accounts happen here   
                print("Unknown Wallet Construct Found")

                for Datafeed in base.Construct_String_Address(10) , Address , self.Create_Profile_Avatar() , Username , base.Space_Time_Generator("DateStr") , base.Space_Time_Generator("TimeInt") : 
                    User_Account_Data.append(Datafeed) 
                

                if(len(User_Account_Data) == int(6)):
                    # Safe to push data to the database   
                    # Call to communitycharter thru createaccount() 
                    CWTInterface.Create_Account(User_Account_Data)
                else: 
                    # You could either dump them to cookies or json 
                    # Then upon page loads check for necessaryy storage cookies  

                    print("Unable to save details to account ")
                return redirect(url_for('Blogs' ,  AccountAddress = User_Account_Data[0]))



                # EOF :  Data pump >> CommunityCharter 
            # Subtle check for Account Address 
            # Remove this once we go live : only for testnet 
           
            # Return requested profile thru client connect 
            
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
        # A universallly accessible time specifier 
        System_Timestamp = base.Space_Time_Generator("Mutate")
        # Retreiving Account Details for the said user 
        # Compacted in List based form 
    
        Custom_ID = CWTInterface.Render_Consumer_ID(AccountAddress)
        Profile_Avatar = CWTInterface.Render_Profile_Avatar(AccountAddress)
        Access_Username = CWTInterface.Render_Consumer_Username (AccountAddress)

    
        # Retreiving All Available stories offchain 
        Article_Listings = CWTInterface.Print_All_Stories()
        # Retreiving All Available Users offchain  
        Account_Profiles =  CWTInterface.Print_Aggragate_Profiles()
        # Retreival of Comments Per Article Cant Be Done Thru a one time init 
        # Due to the dynamicness of data in the system therefore  
        # We'll have to introduce a function that returns data based on articleid  provided while 
        # laveraging the comments_per_article db-impl at the same time 

        def Render_Article_Commentary(ArticleID):
            
            if(CWTInterface.Render_Comments_Per_Article(ArticleID)):
                Commentary = CWTInterface.Render_Comments_Per_Article(ArticleID) 
                return Commentary
            else:
                return None 

        # Reendering Article Related Pictures Available in the system 
        # This returns a list of items available in a set folder  



        def Return_StorySets(ArticleID): 
            if(ArticleID):
                FixedPath =  os.path.join(app.static_folder , StorySets , ArticleID ) 
            #print(os.listdir(FixedPath))
            return os.listdir(FixedPath)




        # Reendering Article Related Pictures Available in the system 
        # This returns a list of items available in a set folder  


        def Render_Board_Adverts(): 
            FixedPath =  os.path.join(app.static_folder , "Sources" , "assets" , "img" ,  "Advertisements") 
            #print(os.listdir(FixedPath))
            return os.listdir(FixedPath)



        Render_Adverts = Render_Board_Adverts()

        Article_Volume = int(0)
        if not (Article_Listings):
            Article_Volume = int(0)
        else:
            Article_Volume = len(Article_Listings)
        
        if not (Account_Profiles):
            Account_Volume = int(0)
        else:
            Account_Volume = len(Account_Profiles)
        

        return render_template('Listings.html' , AccountAddress = AccountAddress , Article_Listings = Article_Listings  , Article_Volume = Article_Volume , Account_Profiles = Account_Profiles  , Account_Volume = Account_Volume , Render_Article_Commentary = Render_Article_Commentary  , Return_StorySets = Return_StorySets , Render_Adverts = Render_Adverts , System_Timestamp = System_Timestamp , Custom_ID = Custom_ID , Access_Username  = Access_Username  , Profile_Avatar = Profile_Avatar  )


@app.route("/")
def LandingPage():
    CompanyID = "CoinWryt"
    return render_template("Home.html" , CompanyID = CompanyID)


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
        files = request.files.getlist('MediaStories')
        #print(file.filename)
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
                #print("Physicall path" , os.path.join(app.static_folder , "Sources" , "assets" , "img" , "Stories" , Datapoint[0]))
                for file in files : 
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
