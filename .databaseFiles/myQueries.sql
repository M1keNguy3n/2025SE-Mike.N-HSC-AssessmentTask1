-- CREATE TABLE users(id INTEGER PRIMARY KEY autoincrement,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);

-- INSERT INTO users(username,password) VALUES ('admin','password');

-- SELECT * FROM users;

-- CREATE TABLE diaries(id INTEGER PRIMARY KEY autoincrement,
                     --developer TEXT NOT NULL,
                     --project TEXT NOT NULL,
                     --StartTime DATETIME,
                     --EndTime DATETIME,
                     --RepoURL TEXT NOT NULL,
                     --DevNote TEXT NOT NULL,
                     --CodeSnippet TEXT NOT NULL)
--ALTER TABLE diaries ADD COLUMN TimeWorked INT;

-- UPDATE diaries
-- SET TimeWorked = ROUND((julianday(EndTime) - julianday(StartTime)) * 1440 / 15) * 15;

--ALTER TABLE diaries
--DROP COLUMN DiaryEntryTime;

-- INSERT INTO diaries(developer, project, StartTime, EndTime, RepoURL, DevNote, CodeSnippet) VALUES ('John Howard', '2024SE', '2024/10/10 08:45:00', '2024/10/10 10:15:00', 'https://github.com/TempeHS/The_Unsecure_PWA-Source.git', 'I worked on the example API, implementing rate limiting to increase API security. The documentation was easy to follow: Flask-Limiter Docs. I executed a range of tests using HTML requests from browsers and Postman to make sure it functioned to specification.', ' python \nfrom flask_limiter import Limiter\nfrom flask_limiter.util import get_remote_address\n\napi = Flask(__name__)\ncors = CORS(api)\napi.config["CORS_HEADERS"] = "Content-Type"\nlimiter = Limiter(\n get_remote_address,\n app=api,\n default_limits=["200 per day", "50 per hour"],\n storage_uri="memory://",\n)\n\n@api.route("/", methods=["GET"])\n@limiter.limit("1/second", override_defaults=False)\n')
-- SELECT developer, project, StartTime, Endtime FROM diaries
-- DROP TABLE users
--CREATE TABLE users (
    --id SERIAL PRIMARY KEY, -- Auto-incrementing ID
    --email VARCHAR(255) UNIQUE NOT NULL, -- Email address
    --password VARCHAR(255) NOT NULL -- Hashed password);
SELECT * FROM users WHERE email = 'minhkhuattuan.nguyen@gmail.com'