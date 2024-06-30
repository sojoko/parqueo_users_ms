import bcrypt

input_password = '2020'


hashed_password = bcrypt.hashpw(input_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# a = bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

print(hashed_password)
# print(input_password.encode('utf-8'))
# print(a)