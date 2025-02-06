-- INSERT INTO users(username,password) VALUES ('admin','password');

CREATE TABLE diaries(id INTEGER PRIMARY KEY autoincrement,
                     developer TEXT NOT NULL,
                     project TEXT NOT NULL,
                     StartTime DATETIME,
                     EndTime DATETIME,
                     RepoURL TEXT NOT NULL,
                     DevNote TEXT NOT NULL,
                     CodeSnippet TEXT NOT NULL,
                     language TEXT NOT NULL,
                     owner INTEGER NOT NULL)



CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    email VARCHAR(255) UNIQUE NOT NULL, -- Email address
    password VARCHAR(255) NOT NULL, -- Hashed password
    otp_secret VARCHAR(255) NOT NULL, -- Two-factor authentication secret key
    api_key VARCHAR(255) NOT NULL, -- API key
    api_key_expiration DATETIME NOT NULL -- API key expiration date
);
