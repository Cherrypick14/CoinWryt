import sqlite3 , os 
from flask import *
from sqlite3 import Error
import uuid


app=Flask(__name__)
def create_connection(db_file):
    """ create a database connection to the DFIite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, Create_DB_Schema):
    try:
        c = conn.cursor()
        c.execute(Create_DB_Schema)
    except Error as e:
        print(e)

def Unbox_Database_Scheme(DatabaseURL):
   

    # Usermode  - Represents the user's housing  status wether hes searching . looking , booking 
    # Override @ Init - Use Default constructors if user is absent from zoning() 
    # Protocol - For LoggedIN | LoggedOUT Conditions 

    Storymode_Schema = """CREATE TABLE IF NOT EXISTS Storymode(
                                    ArtToken text UNIQUE  NOT NULL,
                                    OwnerID text NOT NULL,
                                    Comments integer NOT NULL ,
                                    Subject text NOT NULL ,
                                    Views integer NOT NULL ,
                                    Dateline text NOT NULL,
                                    Timeline text NOT NULL,
                                    Likes integer NOT NULL, 
                                    Dislikes integer NOT NULL,
                                    Billings integer NOT NULL ,
                                    Complaints integer NOT NULL 
                                    
                                );"""


    Community_Schema = """CREATE TABLE IF NOT EXISTS CommunityCharter(
                                    CustomID integer UNIQUE  NOT NULL ,
                                    PAT text UNIQUE  NOT NULL,
                                    Avatar text NOT NULL,
                                    Username text NOT NULL ,
                                    Dateline text NOT NULL,
                                    Timeline text NOT NULL,
                                    Transactions integer NOT  NULL ,
                                    Followers integer NOT NULL ,
                                    GrossAmountPerTR integer NOT NULL ,
                                    Account_ISExistent text NOT NULL 

                                    
                                );"""





    Nft_Schema = """CREATE TABLE IF NOT EXISTS NftCharter(
                                    NftID text NOT NULL ,
                                    Title text NOT NULL , 
                                    Description text NOT NULL ,
                                    Creator text NOT NULL ,
                                    CreationTime text NOT NULL ,
                                    CreationDate text NOT  NULL , 
                                    MediaUrl text NOT NULL , 
                                    MediaType text NOT NULL ,
                                    Price interger NOT NULL ,
                                    Positive interger NOT NULL ,
                                    Negative integer NOT NULL , 
                                    Royalties text NOT NULL , 
                                    RoyaltyBag text NOT NULL ,
                                    State text NOT NULL 
                                  
                                );"""


    Transactional_Schema = """CREATE TABLE IF NOT EXISTS TransactionsCharter(
                                    TransID text NOT NULL ,
                                    Sender text NOT NULL , 
                                    Receiver text NOT NULL ,
                                    Reference text NOT NULL ,
                                    PricedAmount interger NOT NULL ,
                                    BlockID text NOT NULL ,
                                    TransHash text NOT  NULL , 
                                    ScanURL text NOT NULL , 
                                    Timeline text NOT NULL , 
                                    Dateline text NOT NULL , 
                                    Status text NOT NULL 
                                    

                                    
                                );"""





    Feedback_Schema = """CREATE TABLE IF NOT EXISTS FeedbackCharter(
                                    FeedID text NOT NULL ,
                                    FeedType text NOT NULL ,
                                    Reference text NOT NULL , 
                                    OwnerID text NOT NULL ,
                                    Timeline text NOT NULL , 
                                    Date text NOT NULL 
                                    

                                    
                                    
                                );"""


    Commentative_Schema = """CREATE TABLE IF NOT EXISTS CommentsCharter(
                                CustomID text NOT NULL ,
                                ArtToken text NOT NULL , 
                                Subject text NOT NULL,
                                Dateline text NOT NULL , 
                                Timeline text NOT NULL , 
                                likes integer NOT NULL , 
                                Dislikes integer NOT NULL 
                    
                                
                            );"""                        


    # create a database connection
    conn = create_connection(DatabaseURL)


# create tables
    if conn is not None:
        # Create Clientelle Table Structure 
        # Hold User Information Here
        create_table(conn, Storymode_Schema)

        # Create Property Table Structure 
        # Hold Property Information Here
        create_table(conn,  Community_Schema)

        create_table(conn , Transactional_Schema)

        create_table(conn , Nft_Schema)

        create_table(conn , Feedback_Schema)

        create_table(conn , Commentative_Schema)
       
        
    else:
        print("Creation Of [RENTLORD] Database Has Failed .")
        print("The Process Ended With The Following Results : ")


#Unbox_Database_Scheme(os.path.join(app.root_path , "database/CWTDB.db"))