import requests


def find_birthdays(monthDay, year, size=10):
    # monthDay is in form "mm/dd"
    # year is in form "yyyy"
    # returns a list of names, birth years and thumbnails
    # sortedbyClosestYear[i]['text'] has name of ith match
    # sortedbyClosestYear[i]['year'] has year of ith match's birthdate
    # sortedbyClosestYear[i]['thumbnail'] has url of ith match's thumbnail picture or localhost if there is none
    size = int(size)
    year = int(year)
    path = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
    response = requests.get(path + "/births/" + monthDay)
    data = response.json()
    sortedbyClosestYear = sorted(
        data["births"], key=lambda i: abs(int(i["year"]) - year)
    )
    if len(sortedbyClosestYear) > size:
        sortedbyClosestYear = sortedbyClosestYear[0:size]
    for item in sortedbyClosestYear:
        item[
            "thumbnail"
        ] = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        # item["thumbnail"] = "localhost"
        if "thumbnail" in item["pages"][0]:
            item["thumbnail"] = item["pages"][0]["thumbnail"]["source"]
    return sortedbyClosestYear
