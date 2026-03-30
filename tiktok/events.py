class CommentEvent:
    def __init__(self, user, message):
        self.user = user
        self.message = message


class JoinEvent:
    def __init__(self, user):
        self.user = user
