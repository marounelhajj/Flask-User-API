# seed_and_test.py
from db import create_db_table, insert_user, get_users, get_user_by_id, update_user, delete_user

create_db_table()

u = insert_user({
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "067765434567",
    "address": "Doe Street 1",
    "country": "Austria",
})
print("Inserted:", u)

print("All users:", get_users())

uid = u.get("user_id")
print("Get by id:", get_user_by_id(uid))

u["name"] = "John Updated"
print("Updated:", update_user(u))

print("Delete:", delete_user(uid))
print("All after delete:", get_users())
