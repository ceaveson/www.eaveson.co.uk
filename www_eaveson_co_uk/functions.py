import hmac
import hashlib
from datetime import date


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split("=", 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, "latin-1")
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


def date_with_day_suffix(date: date) -> str:
    """
    Give the function a date object and a string will be
    returned with the date in day, month year format but
    the day will have the correct suffix added like 1st,
    2nd, 3rd, 4th etc...
    
    an example use would be:

    test_date = date(2023,1,22)
    a = date_with_day_suffix(test_date)
    print(a)
    
    22nd January 2023
    """
    day = date.strftime("%d").lstrip("0")
    if day == "11" or day == "12" or day == "13":
        day = day + "th"
    elif day[-1] == "1":
        day = day + "st"
    elif day[-1] == "2":
        day = day + "nd"
    elif day[-1] == "3":
        day = day + "rd"
    else:
        day = day + "th"
    return f"{day} {date.strftime('%B %Y')}"
