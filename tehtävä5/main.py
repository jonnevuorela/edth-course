import pymongo


def deleteDatabase():
    pymongo.DeleteOne(

    )
    startOver()


def importDatabase():
    startOver()


def queryDatabase():
    startOver()


def promptAction():
    print("--------------------------------------")
    print("Mitä haluat tehdä?")
    print("0. Sulje ohjelma.")
    print("1. Tyhjennä MongoDB titetokanta.")
    print("2. Vie tietokanta Postgrestä MongoDB.")
    print("3. Suorita kysely MongoDB")
    _choice = input(": ")
    match _choice:
        case "0":
            return 0
        case "1":
            deleteDatabase()
        case "2":
            importDatabase()
        case "3":
            queryDatabase()


def startOver():
    _choice = input("Haluatko jatkaa? (k/e): ")
    match _choice.lower():
        case "e":
            return 0
        case "k":
            promptAction()


promptAction()
