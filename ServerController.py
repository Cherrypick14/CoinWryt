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
            Username = base.Construct_String_Address(10)
            # Minor ommissions 
            if not Username: 
                Username = base.Construct_String_Address(10)
            # We need to check if the said address erxists offchain 
            # If so , then this a validly created account under Coinwryt 
            # Else throw off a UNI error and enforce account abtstraction 
            if(CWTInterface.Confirm_Acc_Visibility(Address)):
                # Account Address Exists Offchain 
                # Update minor details on chain 
                return redirect(url_for('Stories' ,  AccountAddress = Address ))
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
                return redirect(url_for('Stories' ,  AccountAddress = User_Account_Data[1]))



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
        
class Story_Mode_Portal(View): 
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
        

        return render_template('StoryMode_Concept.html' , AccountAddress = AccountAddress , Article_Listings = Article_Listings  , Article_Volume = Article_Volume , Account_Profiles = Account_Profiles  , Account_Volume = Account_Volume , Render_Article_Commentary = Render_Article_Commentary  , Return_StorySets = Return_StorySets , Render_Adverts = Render_Adverts , System_Timestamp = System_Timestamp , Custom_ID = Custom_ID , Access_Username  = Access_Username  , Profile_Avatar = Profile_Avatar  )


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
        return redirect(url_for('Stories' , AccountAddress = AcctAddress ))
    else:
        return redirect(url_for('Stories' , AccountAddress = AcctAddress ))
    # Generally Returning the Tempplate 
    return redirect(url_for('Stories' , AccountAddress = AcctAddress ))


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
                return redirect(url_for('Stories' , AccountAddress = AccountAddr))
            else: 
            # THis means that our stiry wasnt creaeted  
            # Convince the user to try again 
                return redirect(url_for('Stories' , AccountAddress = AccountAddr))
        
        return redirect(url_for('Stories' , AccountAddress = AccountAddr))

class MyAccount_Display_Dashboard(View): 
    methods = ['GET'] 

    def Compose_Dateline_Sys(self): 
        Max_Limit = int(31) 
        return Max_Limit

    def dispatch_request(self , AccountAddr) -> str : 
        # Dateline System Setup  
        Max_Date_Limit = self.Compose_Dateline_Sys()
        # Date - Time -Calendar  Indexer   
        # Implementatio nfrom  base 

        # Date String 
        Date_String_Fmt = base.Space_Time_Generator("DateStr")
        Time_Numeric_Fmt  = base.Space_Time_Generator("TimeInt")
        Custom_ID = CWTInterface.Render_Consumer_ID(AccountAddr)
        Profile_Avatar = CWTInterface.Render_Profile_Avatar(AccountAddr)
        Access_Username = CWTInterface.Render_Consumer_Username (AccountAddr)

        # Day Date Assumption  
        Current_Date = int(12) 

        return render_template('Dashboard.html' , AccountAddr = AccountAddr , Custom_ID = Custom_ID ,  Access_Username = Access_Username , Profile_Avatar = Profile_Avatar ,  Date_String_Fmt = Date_String_Fmt , Time_Numeric_Fmt = Time_Numeric_Fmt , Max_Date_Limit = Max_Date_Limit , Current_Date  = Current_Date  )


class Content_Collections_Concept(View):
   methods = ['GET']  
   def dispatch_request(self , AccountAddress , Type  ) -> str :
        # ----------------------------------------------------------------------
        # We need to assert context based on  route redirection for All / Specific
        # Meaning we need to address one var in particular -- Type &  Storyline_Concept - Render proper db code as expx: 
        CompanyID = "CoinWryt"
        if request.method == 'GET':
            Creator_Listings =  CWTInterface.Render_All_Consumers() 
            Current_Dateline = base.Space_Time_Generator("DateStr")
            Current_Timeline  = base.Space_Time_Generator("TimeInt")
            UserToken = CWTInterface.Render_Consumer_ID(AccountAddress)
            Profile_Avatar = CWTInterface.Render_Profile_Avatar(AccountAddress)
            # Retreive Context Wallet Address Username 
            Access_Username = CWTInterface.Render_Consumer_Username (AccountAddress)
            # Retreive All Available NFT's in Base_Nft's
            Nft_Tags = CWTInterface.Render_Nft_Base_Assets()
            # Handling Type Scpefication here -- control for route specification  
            if(Type == 'All'): 
                Storyline_Concept =  CWTInterface.Print_All_Stories()  
            else:
                Storyline_Concept = CWTInterface.Render_Storyline_Accounts(Type)
                

            # Check Scnearios For Dry Runs  , 

            # Check For Creator_Listings  
            if(Creator_Listings): 
                Creator_Index = len(Creator_Listings)
            else: 
                Creator_Index = int(0) 

            # Check For Storyline Concept 
            if (Storyline_Concept): 
                Storyline_Index  =  len(Storyline_Concept)
            else:
                Storyline_Index = int(0)


            # Check For NFt Tags  
            if(Nft_Tags):
                Nft_Tag_Index = len(Nft_Tags)
            else:
                Nft_Tag_Index = int(0)

                
            


            return render_template('Collections.html'   , AccountAddress = AccountAddress  , Current_Dateline = Current_Dateline , Current_Timeline =  Current_Timeline , UserToken = UserToken , Access_Username = Access_Username , Profile_Avatar =  Profile_Avatar , Creator_Listings = Creator_Listings , Creator_Index = Creator_Index ,  Storyline_Concept = Storyline_Concept ,  Storyline_Index = Storyline_Index ,  Nft_Tags = Nft_Tags , Nft_Tag_Index = Nft_Tag_Index ,  CompanyID = CompanyID)
        
        return render_template('Collections.html' ,  AccountAddress = AccountAddress  )



class Market_Place_Nft(View):
   methods = ['GET']  
   def dispatch_request(self , AccountAddress ) -> str :
        CompanyID = "CoinWryt"
        if request.method == 'GET':
            # Controlling Functions 
            Profile_Avatar =  CWTInterface.Render_Profile_Avatar(AccountAddress)
            # Retreiving All Available Nft's To Ship To Market Place 
            Base_Nft_Assets = CWTInterface.Render_Nft_Base_Assets()  
            # Retreiving Market Place Based Transactions And Their Index 
            Base_Transaction_Logs = CWTInterface.Render_Full_Transaction_Logs()



            # Data Check For Exported Functions 
            # Base_Nft_Assets 
            if(Base_Nft_Assets):
                Base_Nft_Index = len(Base_Nft_Assets)
            else:
                Base_Nft_Index = int(0)
            # Check -2
            # Base_Transaction-Logs Check
            if(Base_Transaction_Logs):
                Base_Trans_Index = len(Base_Transaction_Logs)
            else: 
                Base_Trans_Index = int(0) 


            return render_template('MarketPlace-Nft.html'   , AccountAddress = AccountAddress  , Profile_Avatar = Profile_Avatar , Base_Nft_Assets = Base_Nft_Assets , Base_Nft_Index = Base_Nft_Index , Base_Transaction_Logs = Base_Transaction_Logs , Base_Trans_Index = Base_Trans_Index )
        
        return render_template('MarketPlace-Nft.html' ,  AccountAddress = AccountAddress  )




class Creators_Content_Paradox(View):
   methods = ['GET']  
   def dispatch_request(self , AccountAddress ) -> str :
        CompanyID = "CoinWryt"
        if request.method == 'GET':
            # Operational Zone  
            
            # Exporting All Accounts  ->  Creator_Records   <- Render_All_Consumers()  
            Creator_Records =  CWTInterface.Render_All_Consumers() 
            Profile_Avatar =  CWTInterface.Render_Profile_Avatar(AccountAddress) 

            return render_template('Creators-Paradox-Concept.html'   , AccountAddress = AccountAddress  , Creator_Records  = Creator_Records , Profile_Avatar = Profile_Avatar  )
        
        return render_template('Creators-Paradox-Concept.html' ,  AccountAddress = AccountAddress  )



class Account_Transactions_Concept(View):
   methods = ['GET']  

   def Compose_Dateline_Sys(self): 
        Max_Limit = int(31) 
        return Max_Limit

   def dispatch_request(self , AccountAddress) -> str :
        CompanyID = "CoinWryt"

        Max_Date_Limit = self.Compose_Dateline_Sys()
        # Date String 
        Date_String_Fmt = base.Space_Time_Generator("DateStr")
        Time_Numeric_Fmt  = base.Space_Time_Generator("TimeInt")
        Custom_ID = CWTInterface.Render_Consumer_ID(AccountAddress)
        Profile_Avatar = CWTInterface.Render_Profile_Avatar(AccountAddress)
        Access_Username = CWTInterface.Render_Consumer_Username (AccountAddress)

        if request.method == 'GET':
            return render_template('Transactions_Concept.html' , CompanyID = CompanyID  , Date_String_Fmt = Date_String_Fmt , Time_Numeric_Fmt = Time_Numeric_Fmt , Custom_ID = Custom_ID , Profile_Avatar = Profile_Avatar , Access_Username = Access_Username , Max_Date_Limit  = Max_Date_Limit , AccountAddress = AccountAddress )
        else: 
            # Return requested profile thru client connect 
            return render_template('Transactions_Concept.html' , CompanyID = CompanyID  )
        
        return render_template("Account_Transcaction_Log.html" , )


### NFT Creation MEthod 
 ### With Paired GET |  SET  methods Access protocols  
 ### Takes the form , completes the form then switches the data 
 ### One instance  - The data from the form apart from the article content does not go to the Dbase 

class Create_Nft_Technology(View): 
    methods = ['GET' , 'POST']
    # Special In - Class Function Run Here  
    #   Block Sync available  
    def dispatch_request(self , AccountAddress ) -> list : 
        Nft_Piped_Content =  [] 
        Date_String_Fmt = base.Space_Time_Generator("DateStr")
        Creation_Time  = base.Space_Time_Generator("TimeInt")
        Custom_ID = CWTInterface.Render_Consumer_ID(AccountAddress)
        Profile_Avatar = CWTInterface.Render_Profile_Avatar(AccountAddress)
        Generate_Token = base.Construct_String_Address  
        if request.method == 'GET': 
            return render_template("Nft_Creator_Concept.html"  , AccountAddress = AccountAddress  ,   Date_String_Fmt = Date_String_Fmt , Creation_Time = Creation_Time , Generate_Token  = Generate_Token )  
        elif request.method == 'POST': 
            # Handle Form Submission Here 
            # Also handle IPFS Exporting of Obj.Contect() --
            Nft_Form_Data = request.form 
            for slot in Nft_Form_Data.values() : 
                Nft_Piped_Content.append(slot)

            # Appending Changes & Content To Db 
            # Creating New NFT Technology  
            CWTInterface.Craft_Nft_Technology(Nft_Piped_Content)
            return render_template("Nft_Creator_Concept.html"  , AccountAddress = AccountAddress  ,   Date_String_Fmt = Date_String_Fmt , Creation_Time = Creation_Time , Generate_Token = Generate_Token ) 
        else:
            return render_template("Nft_Creator_Concept.html" , AccountAddress  =AccountAddress , Date_String_Fmt = Date_String_Fmt  , Creation_Time = Creation_Time , Generate_Token  = Generate_Token)





app.add_url_rule('/', view_func=Company_Display_Profile.as_view('Home'))
app.add_url_rule('/MyAccount/Dashboard/<string:AccountAddr>/', view_func=MyAccount_Display_Dashboard.as_view('Dash'))
app.add_url_rule('/Login/' , view_func = Authentication_Profile.as_view('Auth'))
app.add_url_rule('/Dashboard/StoryMode/<string:AccountAddress>/' , view_func = Story_Mode_Portal.as_view('Stories'))
app.add_url_rule('/MyAccount/Dashboard/Transactions/<string:AccountAddress>/' , view_func = Account_Transactions_Concept.as_view('Transactions'))
app.add_url_rule('/Dashboard/Collections/<string:AccountAddress>/Target/<string:Type>/' , view_func = Content_Collections_Concept.as_view('Collections'))
app.add_url_rule('/Dashboard/Nft/MarketPlace/<string:AccountAddress>/' , view_func = Market_Place_Nft.as_view('NftMarket'))
app.add_url_rule('/Dashboard/Creators/<string:AccountAddress>/Listings/' , view_func = Creators_Content_Paradox.as_view('Creators'))
app.add_url_rule('/Dashboard/NFT/<string:AccountAddress>/Create/' , view_func = Create_Nft_Technology.as_view('Create-Nft'))
# Returns the listings of stories that the user has created summarised in a table with a unique textarea below each \
# Row to show message content of the story mode in question  

#app.add_url_rule('/Dashboard/StoryMode/Listings/<string:AccountAddress>/' , view_func = StoryMode_Log_List.as_view('StoryLogs'))




if __name__=='__main__':
   app.run(host="0.0.0.0" , debug="False" )
