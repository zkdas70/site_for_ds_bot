with open('token.png', encoding='utf-8') as f_in:
    token = f_in.readlines()[0]

settings = {
    'token': token,
    #'token': ',
    'bot': 'Valera',
    'id': 849713822250958868,
    'prefix': ['V ', 'В ', 'v ', 'в ']
}