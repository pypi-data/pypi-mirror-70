## AWS Cognito code grant for Django Rest Framework

This package implements an authentication backend and a set of handlers that enable your application to use 
code grant authentication with AWS Cognito.

The package has been developed by STITCH (https://www.stitchdesignlab.com/)

The documentation for this project is a work-in-progress and is pretty much bare bones. Do not hesitate to 
contact us, or open an issue or PR for contribution.

#### Links
 - [AWS Cognito](https://aws.amazon.com/cognito/)
 - [Django Rest Framework](https://www.django-rest-framework.org/)
 - [Grant types of Cognito explained by AWS](https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/)

#### Code grant
Code grant is an OAuth 2.0 flow that allows one to use Cognito as a data store and authentication backend 
for users, while maintaining an updating replica of User and Group information in your applications database.
This way, the application gains the possibility to add custom business logic for users, while the user data is
still stored and managed centrally through Cognito.  


This is especially useful when you are implementing multiple API backends for a platform that consist of multiple 
applications that need to operate on a shared userbase.

See the link above for a detailed explanation of the standard.

#### Installation
You can install this package from pip: `pip install cognito_code_grant`

#### Usage
The implementation consists of an [authentication backend](https://www.django-rest-framework.org/api-guide/authentication/), a login handler, and a logout handler.
To use the backend, simply specify it in your Django Settings:
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'cognito_code_grant.authentication.CognitoAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        ...
    )
```
To use the handlers, include them in your URLs using a helper function:
```
from cognito_code_grant.views import include_auth_urls

urlpatterns = [
    path('auth/', include_auth_urls()),
    ...
]
```
Additionally, you will need to set the following settings to point to your instance of Cognito:
```
AUTH_COGNITO_CLIENT_ID = # your client ID
AUTH_COGNITO_CODE_GRANT_URL = # your token endpoint (https://AUTH_DOMAIN/oauth2/token)
AUTH_COGNITO_JWKS_URL = # the url for your JWKs (https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json.)
```

### Development
To run tests, you need to point Django to local test settings, and run the migrations (it will use an sqllite db in a temp folder).  
```python
export DJANGO_SETTINGS_MODULE=tests.settings
python -m django migrate
python -m django test
```

On a merge to master, CICD will automatically create a `patch` version bump, and deploy to pypi. Minor/Major realeases need to be handled manually by the maintainers.
