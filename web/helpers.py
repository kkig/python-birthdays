from datetime import date


def isNameValid(name):
    return name.isalnum()


def toDate(dEntry):
    try:
        return date.fromisoformat(dEntry)
    except TypeError:
        print("Invalid input type for date.")
    except:
        print("Invalid input for date.")
    return None
