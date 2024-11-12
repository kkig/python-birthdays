from datetime import date


def isNameValid(name: str) -> bool:
    return name.isalnum()


def getDate(bday: str):
    try:
        return date.fromisoformat(bday)
    except ValueError:
        print("Invalid input type for date.")
    except:
        print("Invalid input for date.")
    return None
