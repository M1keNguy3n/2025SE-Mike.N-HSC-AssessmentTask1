from datetime import datetime, timezone, timedelta
date = datetime.now(timezone.utc) + timedelta(days=30)
print(type(date))