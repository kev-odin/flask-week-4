import requests


def find_birthdays(monthDay="04/29", year="2022", size=10):
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
        item["thumbnail"] = "localhost"
        if "thumbnail" in item["pages"][0]:
            item["thumbnail"] = item["pages"][0]["thumbnail"]["source"]
    return sortedbyClosestYear


def text_data(raw_json: dict):
    names = [item["text"] for item in raw_json]
    years = [item["year"] for item in raw_json]
    image = [item["thumbnail"] for item in raw_json]
    return zip(names, years, image)


if __name__ == "__main__":
    res = find_birthdays()
    stop = 0
    for item in text_data(res):
        print(item)
