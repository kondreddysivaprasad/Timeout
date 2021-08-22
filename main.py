import json


def venue_is_good_for_all(venue: dict, users: list):
    venue_name, venue_food, venue_drinks = (venue.get("name"), set(venue.get("food")), set(venue.get("drinks")))

    ret_val, reason = user_check(venue_name, venue_food, venue_drinks, users)

    if ret_val is True:
        is_visit = True
    else:
        is_visit = False

    return is_visit, reason


def user_check(name: str, food: set, drinks: set, user_list: list):
    lower_food = set([x.lower() for x in food])
    lower_drinks = set([x.lower() for x in drinks])

    all_user = []
    reason_list = []

    for user in user_list:
        user_name, user_dont_eat, user_drinks = (user.get("name"), set(user.get("wont_eat")), set(user.get("drinks")))

        lower_user_dont_eat = set([x.lower() for x in user_dont_eat])
        lower_user_drinks = set([x.lower() for x in user_drinks])

        if (len(lower_food.difference(lower_user_dont_eat)) > 0) and (len(lower_drinks.intersection(lower_user_drinks)) > 0):
            all_user.append(True)
        else:
            if len(lower_food.difference(lower_user_dont_eat)) == 0:
                reason = f"There is nothing for {user_name} to eat."
            elif len(lower_drinks.intersection(lower_user_drinks)) == 0:
                reason = f"There is nothing for {user_name} to drink."
            reason_list.append(reason)
            all_user.append(False)

    return all(all_user), reason_list


with open("users.json", 'r') as users_file:
    user_data = json.load(users_file)


with open("venues.json", 'r') as venues_file:
    venue_data = json.load(venues_file)

results = {}
visit_list = []
avoid_list = []

results["places_to_visit"] = ''
results["places_to_avoid"] = ''

for venue in venue_data:
    #venue_name, venue_food, venue_drinks = (venue.get("name"), venue.get("food"), venue.get("drinks"))

    place_to_avoid = {}

    if (venue_is_good_for_all(venue, user_data))[0] is True:
        visit_list.append(venue.get("name"))
    else:
        #avoid_list.append(venue.get("name"))
        place_to_avoid["name"] = venue.get("name")
        place_to_avoid["reason"] = (venue_is_good_for_all(venue, user_data))[1]

    avoid_list.append(place_to_avoid)

results["places_to_visit"] = visit_list
results["places_to_avoid"] = avoid_list

with open("output.json", 'w') as out:
  json.dump(results, out, sort_keys = False, indent = 4, ensure_ascii = False)