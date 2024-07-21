class GoogleAuthError(Exception):
    pass

class InvalidGoogleClientIDError(Exception):
    pass

class UserProcessingError(Exception):
    pass

class JWTCreationError(Exception):
    pass

class JWTValidationError(Exception):
    pass

class DatabaseError(Exception):
    pass

class SpamCreationError(DatabaseError):
    pass

class SpamRetrievalError(DatabaseError):
    pass

class UserNotFoundError(DatabaseError):
    pass

class UserCreationError(DatabaseError):
    pass

class TokenNotFoundError(DatabaseError):
    pass

class TokenUpdateError(DatabaseError):
    pass

class TokenCreationError(DatabaseError):
    pass

class TokenDeletionError(DatabaseError):
    pass