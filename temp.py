# # Getting information about yourself
# me = await client.get_me()
#
#
# # "me" is a user object. You can pretty-print
# # any Telegram object with the "stringify" method:
# print(me.stringify())
#
# # When you print something, you see a representation of it.
# # You can access all attributes of Telegram objects with
# # the dot operator. For example, to get the username:
# username = me.username
# print(username)
# print(me.phone)


# await sync_messages_from_dialog(dialog)


# result = await client(functions.contact.GetContactsRequest(
#     hash=-12398745604826
# ))
#


#
# # You can print the message history of any chat:
# async for message in client.iter_messages('533844145'):
#     print(message.id, message.text)
