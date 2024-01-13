from tgtg import TgtgClient
import json

# Save the users dictionary to a JSON file
def save_users():
    with open("users.json", "w") as file:
        json.dump(users, file, indent=2)

# Load users from a JSON file
def load_users():
    global users
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        pass  # File not found, initialize with an empty dictionary

print("(i)nsert or (d)elete")
type = input()

if(type != "i" and type != "d"):
    quit()

users = {}
load_users()

if(type == "i"):
    print("Enter your name: ")
    name = input()
    print("Enter your email: ")
    email = input()

    client = TgtgClient(email=email)
    credentials = client.get_credentials()

    new_user = {"name": name, "email": email, "access_token": credentials["access_token"], "refresh_token": credentials["refresh_token"], "user_id": credentials["user_id"], "cookie": credentials["cookie"]}
    users.append(new_user)
    
    print("User \"" + name + "\" added")

elif(type == "d"):
    print("Enter name to delete: ")
    name = input()

    index_to_remove = None
    for i, user in enumerate(users):
        if user["name"] == name:
            index_to_remove = i
            break

    # Remove the user if found
    if index_to_remove is not None:
        removed_user = users.pop(index_to_remove)

# Save the updated users dictionary
save_users()

