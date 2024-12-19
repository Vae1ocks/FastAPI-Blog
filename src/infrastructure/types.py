from typing import Literal, NewType

# password
PasswordPepper = NewType("PasswordPepper", str)

# jwt
JWTSecret = NewType("JwtSecret", str)
JWTAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
JWTAuthScheme = NewType("JWTAuthScheme", str)
