-- INSERT INTO users(username,password) VALUES ('admin','password');

-- CREATE TABLE diaries(id INTEGER PRIMARY KEY autoincrement,
                     --developer TEXT NOT NULL,
                     --project TEXT NOT NULL,
                     --StartTime DATETIME,
                     --EndTime DATETIME,
                     --RepoURL TEXT NOT NULL,
                     --DevNote TEXT NOT NULL,
                     --CodeSnippet TEXT NOT NULL
                     --language TEXT NOT NULL)

-- UPDATE diaries
-- SET TimeWorked = ROUND((julianday(EndTime) - julianday(StartTime)) * 1440 / 15) * 15;

-- INSERT INTO diaries(developer, project, StartTime, EndTime, RepoURL, DevNote, CodeSnippet) VALUES ('John Howard', '2024SE', '2024/10/10 08:45:00', '2024/10/10 10:15:00', 'https://github.com/TempeHS/The_Unsecure_PWA-Source.git', 'I worked on the example API, implementing rate limiting to increase API security. The documentation was easy to follow: Flask-Limiter Docs. I executed a range of tests using HTML requests from browsers and Postman to make sure it functioned to specification.', ' python \nfrom flask_limiter import Limiter\nfrom flask_limiter.util import get_remote_address\n\napi = Flask(__name__)\ncors = CORS(api)\napi.config["CORS_HEADERS"] = "Content-Type"\nlimiter = Limiter(\n get_remote_address,\n app=api,\n default_limits=["200 per day", "50 per hour"],\n storage_uri="memory://",\n)\n\n@api.route("/", methods=["GET"])\n@limiter.limit("1/second", override_defaults=False)\n')
-- SELECT developer, project, StartTime, Endtime FROM diaries

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    email VARCHAR(255) UNIQUE NOT NULL, -- Email address
    password VARCHAR(255) NOT NULL -- Hashed password);
);
SELECT * FROM users
DROP TABLE users

ALTER TABLE diaries ADD COLUMN TimeWorked INTEGER;

UPDATE diaries
SET TimeWorked = ROUND((strftime('%s', EndTime) - strftime('%s', StartTime)) / 60.0 / 15);

UPDATE diaries
SET TimeWorked = printf('%d:%02d', (TimeWorked * 15) / 60, (TimeWorked * 15) % 60)

ALTER TABLE diaries ADD COLUMN language TEXT;
UPDATE diaries
SET language = 'python';

DELETE TimeWorked from diaries;
SELECT * from diaries WHERE TimeWorked;

ALTER TABLE diaries
RENAME COLUMN TimeWorked TO time_worked;

SELECT * FROM diaries WHERE developer = 'Jane Doe';

DROP TABLE users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    email VARCHAR(255) UNIQUE NOT NULL, -- Email address
    password VARCHAR(255) NOT NULL, -- Hashed password
    otp_secret VARCHAR(255) NOT NULL, -- Two-factor authentication secret key
    api_key VARCHAR(255) NOT NULL, -- API key
    api_key_expiration DATETIME NOT NULL -- API key expiration date
);
