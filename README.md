## Running the app
1. Ensure all dependencies are installed
3. Run main.py
4. Run api.py

## Registering
1. Enter a valid email address
2. Enter a password
3. Scan the QR code with your authenticator app

## Logging in

1. Enter your email and username
2. Enter the OTP from your authenticator app
3. Working login:
   - username: minhkhuattuan.nguyen@gmail.com
   - password: mocnhicam
   - otp_secret: WXZ6P3IWV6XM54H6F3SNDYOEDP6JPEMP to enter manually
   - QR code:
![image](https://github.com/user-attachments/assets/38ecfdb3-6223-4535-8d20-4c26040cd9f7)


## Making a new entry
1. Enter all of the information
2. Press submit

## Viewing your API key
1. Press API on the top bar.
2. If your key expired, press "Generate New API Key" for a new one.
   ![image](https://github.com/user-attachments/assets/e439bad9-c166-4b48-b3e4-9ad1f2659e43)


## Retrieving entries (API)
1. Ensure that the request header has your API key with a Bearer prefix
   ![image](https://github.com/user-attachments/assets/9a615a36-5d56-4038-8dd9-a94e355998d0)

2. Query parameters:
   - column_name: from the list [developer, project, start_time, end_time, time_worked, repo_url, dev_note, code_snippet, language]
   - value: the value to look for
  
## Uploading entries (API)
1. Ensure that the request header has your API key with a Bearer prefix
   ![image](https://github.com/user-attachments/assets/655d3400-839b-448b-b7f9-4c6bc7e95dc6)
3. Enter your data in as a json
4. Schema:
   ```json
   {
        "developer": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "project": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "start_time": {
            "type": "string",
            "pattern": "^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}"
        },
        "end_time": {
            "type": "string",
            "pattern": "^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}"
        },
        "repo_url": {
            "type": "string",
            "pattern": "^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$"
        },
        "dev_note": {
            "type": "string",
            "minLength": 1,
            "maxLength": 500
        },
        "code_snippet": {
            "type": "string",
            "minLength": 1,
            "maxLength": 2000
        },
        "language": {
            "type": "string",
            "enum": ["PYTHON", "CPP", "BASH", "SQL", "HTML", "CSS", "JAVASCRIPT"]
        }
   }
   ```
