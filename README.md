## Overview
Identify the unique information contained in the header and implement ratelimit.


## Libraries used
[responder](https://pypi.org/project/responder/)  
[asgi-ratelimit](https://pypi.org/project/asgi-ratelimit/)

## Try to use
### application start
```
docker compose build
docker compose up
```

### request
Unrestricted endpoints
```
curl --location --request GET 'http://localhost:8000/no_limit' \
--header 'Unique-User-Id: Client A'
```
Restricted endpoints
(Up to once per minute per user)
```
curl --location --request GET 'http://localhost:8000/rate_limit' \
--header 'Unique-User-Id: Client A'
```