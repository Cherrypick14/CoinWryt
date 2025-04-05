import os
import resend

resend.api_key = "re_C9UKrcbL_73NxSUTM8YuhEgQi5qQ14ngw"

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["ahoyaclyde@gmail.com"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)
print(email)
