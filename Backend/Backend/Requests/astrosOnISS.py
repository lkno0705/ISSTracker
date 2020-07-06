import requests


def getAstrosOnISS():
    r = requests.get("http://api.open-notify.org/astros.json");
    data = r.json()
    astros = data["people"]
    astrosOnISS = []
    for astro in astros:
        if astro['craft'] == "ISS":
            astrosOnISS.append(astro['name'])
    return astrosOnISS


# print(getAstrosOnISS())


