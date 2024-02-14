import requests
import sys
import re
from bs4 import BeautifulSoup

URL = "https://read.lsbible.org/?q="
# romans+1%3A16"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Handling of arguments.
if (
    sys.argv[1].isdigit() == True
):  # Allows for "1 john" rather than only "1john" though the latter will work.
    if len(sys.argv) == 2:
        sys.exit(
            "Seems the verse was formatted incorrectly. (Ex. 2 john 1:1-3 or 2 john 1 for whole chapter)"
        )
    else:
        sys.argv[1] = sys.argv[1] + sys.argv[2]
        sys.argv.pop(2)
if (
    len(sys.argv) == 2
):  # Create a list with our verse info ["book", "chapter", "verse"] or ["book", "chapter"] This part also crafts our URL used for scraping later.
    verselist = [
        sys.argv[1].replace(" ", ""),
    ] + [
        "1",
    ]
    URL = URL + verselist[0] + "+" + verselist[1]
    chap = verselist[1]
elif len(sys.argv) == 3:
    verselist = [
        sys.argv[1].replace(" ", ""),
    ] + sys.argv[
        2
    ].split(":")
    if len(verselist) == 2:
        URL = URL + verselist[0] + "+" + verselist[1]
        chap = verselist[1]
    elif len(verselist) == 3:
        URL = URL + verselist[0] + "+" + verselist[1] + "%3A" + verselist[2]
        chap = verselist[1]
else:
    sys.exit(
        "Seems the verse was formatted incorrectly. (Ex. 2 john 1:1-3 or 2 john 1 for whole chapter)"
    )

# LSB can pull multiple chapters, but it complicates the scraper. We'll just not allow it on our end to keep it simple.
if chap.isdigit() == False:
    sys.exit("One chapter at a time.")


def strip_multiple_spaces(text):
    return re.sub(r"\s+", " ", text)


def check_verse():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    # Loop strips out subheadings.
    for t in soup.find_all("h3"):
        t.decompose()
    title = soup.find(
        "h1", attrs={"class": "Passage__StyledPassageTitle-sc-1drf6wh-0 eUlFsT"}
    )
    verse = soup.findAll("span", attrs={"class": "verse"})
    first = soup.findAll("span", attrs={"class": "verse first-verse"})
    iclass = soup.findAll("i", attrs={"class": "float"})

    # This is our way of checking is a verse was found.
    if title == None:
        sys.exit("No verse was found. Remember LSB uses the critical text.")

    print(title.get_text() + " LSB")

    # Poetry sections have multi-lined verses with no space after. This fixes that.
    for j in iclass:
        j.insert_after(" ")

    for i in verse:
        # voodoo to add the 1 in front of the first verse due to it being a background element :/
        start = ""
        if first:
            if verse.index(i) == 0:
                start = "1 "
            else:
                start = ""
        print(start + strip_multiple_spaces(i.get_text()))


check_verse()
