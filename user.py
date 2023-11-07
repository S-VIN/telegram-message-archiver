class User:
    @staticmethod
    def from_tg_user(tg_user):
        result = User()
        result.id = tg_user.users[0].id
        result.first_name = tg_user.users[0].first_name
        result.last_name = tg_user.users[0].last_name
        result.username = tg_user.users[0].username
        result.bot = tg_user.users[0].bot
        result.contact = tg_user.users[0].contact
        return result
