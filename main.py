import json
import csv

def read_followers():
    with open("followers_1.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    followers = set()

    for user in data:
        try:
            followers.add(user["string_list_data"][0]["value"])
        except (KeyError, IndexError, TypeError):
            continue

    return followers

def read_following():
    with open("following.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    following = set()

    for user in data.get("relationships_following", []):
        try:
            following.add(user["title"])
        except KeyError:
            continue

    return following

followers = read_followers()
following = read_following()

non_followers = sorted(following - followers)

with open("non_followers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Usuario"])
    for user in non_followers:
        writer.writerow([user])

print("Resumen:")
print(f"Sigues: {len(following)}")
print(f"Te siguen: {len(followers)}")
print(f"No te siguen: {len(non_followers)}")
print("Exportado a non_followers.csv")
