-- INSERT INTO users(username,password) VALUES ('admin','password');

CREATE TABLE diaries (
    HAUIe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Nzdvy_developer TEXT NOT NULL,
    hBbdT_project TEXT NOT NULL,
    uYCKJ_start_time DATETIME,
    MbOId_end_time DATETIME,
    Aiiyt_repo_url TEXT NOT NULL,
    LaH8Y_dev_note TEXT NOT NULL,
    qVKdx_code_snippet TEXT NOT NULL,
    xI1ka_language TEXT NOT NULL,
    FVtfU_owner INTEGER,
    FOREIGN KEY (FVtfU_owner) REFERENCES users(xpp9x_id)
);

CREATE TABLE users (
    xpp9x_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    K3hq4_email VARCHAR(255) UNIQUE NOT NULL, -- Email address
    55ama_password VARCHAR(255) NOT NULL, -- Hashed password
    vx6rf_otp_secret VARCHAR(255) NOT NULL, -- Two-factor authentication secret key
    UsA17_api_key VARCHAR(255) NOT NULL, -- API key
    0RIEp_api_key_expiration DATETIME NOT NULL -- API key expiration date
);