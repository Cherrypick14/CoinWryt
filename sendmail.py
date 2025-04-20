import os
import resend

# Needs To be Exported To Fit Environment Sec Rules  
resend.api_key = "re_C9UKrcbL_73NxSUTM8YuhEgQi5qQ14ngw"


def Dispatch_Onboarding_Email(): 
    print(0) 



def Create_Email(Recipient ,Subject , Body):
    if Body : 
        if(Recipient) :
            if(Subject) : 

                params: resend.Emails.SendParams = {
                "from": " Godark@coinwryt <onboarding@resend.dev>",
                "to": [Recipient],
                "subject": Subject ,
                "html": Body ,
                }
              

                email = resend.Emails.send(params)
                print(email)
    else: 
        return "Unable to create email : Reason : Empty Parameters supplied ! "

# Main - Body Declaration 
params: resend.Emails.SendParams = {
    "from": " Godark@coinwryt <onboarding@resend.dev>",
    "to": ["ahoyaclyde@gmail.com"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}



Create_Email("ahoyaclyde@gmail.com" , "Test 1" , "Good morning")
