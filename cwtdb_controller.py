import sqlite3
from sqlite3 import Error
from flask import *
import os 

app=Flask(__name__)

DatabaseURL = os.path.join(app.root_path , "") + "/database/CWTDB.db"
app.config['DatabaseURL']= DatabaseURL

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def Create_Story(Property):
    """
    Create a new PropertyName into the PropertyNames table
    :param conn:
    :param PropertyName:
    :return: PropertyName id
    """
    conn = create_connection(DatabaseURL)
    with app.app_context():
        
        sql = '''INSERT INTO Storymode(ArtToken , OwnerID , Category , Comments , Subject  , Views , Dateline , Timeline ,   Likes , Dislikes  , Billings , Complaints  )
            VALUES(?,?,?,?,?,?,?,?,0,0,0,0) '''
        cur = conn.cursor()
        cur.execute(sql,Property)
        conn.commit()
        conn.close()
        return "Success"
    



def Print_All_Stories():
    """
    Query all DatabaseFeed in theProperty_Schema table
    :param conn: the Connection object
    :return:
    """
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Storymode ")

    DatabaseFeed =cur.fetchall()
    Datalist = []
    for DataChunk in DatabaseFeed:
        print("This is " , DataChunk)
        Datalist.append(DataChunk)
    return DatabaseFeed


# Dashboard Intrinsic Methods For Handling Common Dat  

# Manually Retrieves Consumer ID from Db as doing it in a pool return discombubulated datav 
def Render_Consumer_ID(Bindings):
    """
    Query all DataItem in the Clientelle_Pool ss table
    :param conn: the Connection object
    :return:
    """
    
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT CustomID FROM CommunityCharter  WHERE PAT = ? ", (Bindings,))

    DataItem = cur.fetchall()

    for bit in DataItem:
        print(bit)
    return str(DataItem).strip("[]()'',")




# Returns Consumer Username from Db thrust 
def Render_Consumer_Username(Bindings):
    """
    Query all DataItem in the Clientelle_Pool ss table
    :param conn: the Connection object
    :return:
    """
    
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT Username FROM CommunityCharter  WHERE PAT = ? ", (Bindings,))

    DataItem = cur.fetchall()

    for bit in DataItem:
        print(bit)
    return str(DataItem).strip("[]()'',")




def Render_Profile_Avatar(Bindings):
    """
    Query all DataItem in the Clientelle_Pool ss table
    :param conn: the Connection object
    :return:
    """
    
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT Avatar FROM CommunityCharter  WHERE PAT = ? ", (Bindings,))

    DataItem = cur.fetchall()

    for bit in DataItem:
        print(bit)
    return str(DataItem).strip("[]()'',")


### Cummunity_CHarter Block 
### COntrollers 



def Create_Account(Property):
    """
    Create a new PropertyName into the PropertyNames table
    :param conn:
    :param PropertyName:
    :return: PropertyName id
    """
    conn = create_connection(DatabaseURL)
    with app.app_context():
        
        sql = '''INSERT INTO CommunityCharter(CustomID , PAT , Avatar , Username , Dateline , Timeline , Transactions , Trans_Amounts , Account_ISExistent )
            VALUES(?,?,?,?,?,?,0,0, "True") '''
        cur = conn.cursor()
        cur.execute(sql,Property)
        conn.commit()
        conn.close()
        return "Success"
    


## Return Available User Profiles 



def Confirm_Acc_Visibility(Bindings):
    """
    Query all DataItem in the Clientelle_Pool ss table
    :param conn: the Connection object
    :return:
    """
    
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT CustomID FROM CommunityCharter  WHERE PAT = ? ", (Bindings,))

    DataItem = cur.fetchall()

    for bit in DataItem:
        print(bit)
    return DataItem



def Print_Aggragate_Profiles():
    """
    Query all DatabaseFeed in theProperty_Schema table
    :param conn: the Connection object
    :return:
    """
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM CommunityCharter ")

    DatabaseFeed = cur.fetchall()

    for DataChunk in DatabaseFeed:
        print(DataChunk)
    return (DatabaseFeed)



### Comments Charter Post  ####
### Pre-Lude 

# Contains actions for modifying , creation and retrieval of objects from the communitycharter table 



def Create_Comment(Property):
    """
    Create a new PropertyName into the PropertyNames table
    :param conn:
    :param PropertyName:
    :return: PropertyName id
    """
    conn = create_connection(DatabaseURL)
    with app.app_context():
        
        sql = '''INSERT INTO CommentsCharter(CustomID , ArtToken , Subject , Dateline , Timeline , likes , Dislikes )
            VALUES(?,?,?,?,?,0,0) '''
        cur = conn.cursor()
        cur.execute(sql,Property)
        conn.commit()
        conn.close()
        return "Success"
    

# Selective Comments Based On ArticleID 


def Render_Comments_Per_Article(Bindings ):
    """
    Query all DataItem in the Clientelle_Pool ss table
    :param conn: the Connection object
    :return:
    """
    
    conn = create_connection(DatabaseURL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM CommentsCharter  WHERE ArtToken = ? ", (Bindings,))

    DataItem = cur.fetchall()

    for bit in DataItem:
        print(bit)
    return DataItem


#Test_Story  =["#RITRRIIR" , "0xd48e84bda5351d516b9cd9361fea27b086a93188" , "Political" , "0" ,"Gradually kenya's economy is crumbling" , "0" , "3:14:pm " , "2025/27/02" , "0" , "0" , "0", "0"]
#Create_Story(Test_Story)



#Test_Account  = ["#RITRRIIR" , "0xd48e84bda5351d516b9cd9361fea27b086a93188" , "ramp.png" ,  "DeathRawl"  , "2025/27/02" , "3:14:pm" ]
#Create_Account(Test_Account)

#Print_All_Stories()
#Print_Aggragate_Profiles()
