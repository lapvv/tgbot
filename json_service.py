import json

with open("users.json", "r") as f_o:
    data_from_json = json.load(f_o)

user_id = 1
username = "Max"

if str(user_id) not in data_from_json:
    data_from_json[user_id] = {"username": username}

with open("users.json", "w") as f_o:
    json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)

print(data_from_json)
