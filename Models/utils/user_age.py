def binAge(user_age):
    age_binned = 0
    if user_age < 18:
        age_binned = 0
    elif user_age < 25:
        age_binned = 1
    elif user_age < 35:
        age_binned = 2
    elif user_age < 45:
        age_binned = 3
    elif user_age < 55:
        age_binned = 4
    elif user_age < 65:
        age_binned = 5
    else:
        age_binned = 6

    return age_binned
