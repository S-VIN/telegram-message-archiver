class User:
    def __init__(self, tg_user=None):
        if tg_user is None:
            return
        self.id = tg_user.users[0].id
        self.first_name = tg_user.users[0].first_name
        self.last_name = tg_user.users[0].last_name
        self.username = tg_user.users[0].username
        self.bot = tg_user.users[0].bot
        self.contact = tg_user.users[0].contact
