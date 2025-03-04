from datetime import datetime
import time , string , random , asyncio
from flask import *
import uuid , os

app=Flask(__name__)



# Function To Yield System Formatted Time 
# Params : FORM : arguments to control specified time 

def Space_Time_Generator(Form) -> str:
    """A Function To Yield System Formatted Time In Layed Out Formats  """
    # Initiate The Time Object 
    TimeComponent = datetime.now()

    # Determine Printing Form --DateInt --Time  -DateString 
    if (Form == str('DateInt')) :
        # Returns Only The Date In Int Form 
        FormatedString =TimeComponent.strftime("%D")
    elif ( Form == str('DateStr')):
        # Returns The Day - Str , Date - Int and Year - Int e.g Sunday:05:2024
        FormatedString =TimeComponent.strftime(f"%A:%m:%Y")
    elif(Form == str('TimeInt')):
        # Returns int time in form of Hrs Min Sec
        FormatedString =TimeComponent.strftime(f"%H:%M:%S")
    elif(Form == str('Mutate')):
        # Returns the full string date object all in Int form such as : 05/19/24:04:40:38
        FormatedString =TimeComponent.strftime(f"%D:%H:%M:%S")


    return FormatedString 



# Unique Random Address Table 
# Return  Non - Reccurring Unique Addresses From The Random Module 
# Params : Int : A set of Random Numbers  To Be  Returned 
#        : Chars  :  Formulates The Alphabetical Table A-Z and Append The Int Range 0-9 For Random Number Generations 
# Returns A Formated String Object 

def Construct_String_Address(size, chars=string.ascii_uppercase + string.digits) -> str: 
    """ Creates A Random Int and String Character Sets For Unique Token Generations """
    return ''.join(random.choice(chars) for x in range(size))



# Unique Random Address Table 
# Return  Non - Reccurring Unique Addresses From The Random Module 
# Params : Int : A set of Random Numbers  To Be  Returned 
#        : Chars  :  Formulates  The Int Range 0-9 For Random Number Generations 
# Returns A Formated Int Object 
def Construct_Int_Address(size, chars=string.digits) -> str: 
    """ Creates A Unique Addresses For System Use . Current USe Cases Is To Provide A One Time 4 Set Token Number For OTP Verifications"""
    return ''.join(random.choice(chars) for x in range(size))





# A Function return profile avatars based on filepath   
# Fetches collectives on the said path and returns the length index after passing it random.randrange 


# A Color Visulaization Protocol 
# Developed to rteturn Color Profiles Based On randomly generated list indexes 
def ColorSort():
    " A Color mixer developed for profiling different elements by returning colorschemes in list based indexes  "
    Index = random.randrange(0,5)
    return Index
