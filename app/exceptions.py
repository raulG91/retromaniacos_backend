class EventNotFoundException(Exception):
    """Raised when an event is not found."""
    pass

class UserAlreadyParticipatingException(Exception):
    """Raised when a user is already participating in an event."""
    pass
class UserParticipationNotFoundException(Exception):
    """Raised when a user's participation in an event is not found."""
    pass
class MaterialNotFoundException(Exception):
    """Raised when a material is not found."""
    pass