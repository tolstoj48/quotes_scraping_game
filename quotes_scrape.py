import requests
from random import randint
from bs4 import BeautifulSoup


def fetch_start_data():
    """
    The function scrapes all the data from the web of quotes.
    Gets all the quotes from all the available pages.
    Returns the list of all the scraped quotes.
    """
    result_list = []
    flag_for_next = True
    page_number = 1
    while flag_for_next:
        request_result = requests.get(
            f"https://quotes.toscrape.com/page/{page_number}/")
        soup = BeautifulSoup(request_result.text, "html.parser")
        if len(soup.select(".next")) == 0:
            flag_for_next = False
        data = soup.select(".quote")
        for quote in data:
            result_list.append([
                quote.select(".text")[0].get_text(),
                quote.select(".author")[0].get_text(),
                quote.select(".author")[0].find_next_sibling().attrs["href"]])
        page_number += 1
    return result_list


def fetch_hint(href):
    """
    The function scrapes only data about the author of the hint.
    Accepts correct link suffix of the quotes page.
    Returns the tuple of the date and place of the author birth.
    """
    request_result = requests.get(
        f"https://quotes.toscrape.com/{href}")
    soup = BeautifulSoup(request_result.text, "html.parser")
    born_date = soup.select(".author-born-date")[0].get_text()
    born_location = soup.select(".author-born-location")[0].get_text()
    return (born_date, born_location)


def game():
    """
    The main gaim function. Driver of the whole game.
    """
    # flag - does user want another game round?
    another_game = True
    # functions data
    data = fetch_start_data()
    while another_game:
        # returns the user´s input
        another_game = play_game(data)
        # to be more user friendly
        if another_game not in ("y", "Y", "yes", "Yes", "YES"):
            another_game = False
    return "GAME OVER!!!"


def play_game(data):
    """
    The function of the main game´s logic.
    Prints all the questions.
    Returns the answer whether the user wants another round of the game.
    """
    question = data[randint(0, len(data))]
    number_of_guesses = 4
    hints = fetch_hint(question[2])
    print(question[0])
    while number_of_guesses:
        if number_of_guesses == 3:
            print(
                f"Here is the hint: The author was born on the {hints[0]} and {hints[1]}.")
        print(f"You have {number_of_guesses} remaining guesses.")
        answer = str(input("Who is the author of the quote? "))
        if answer == question[1]:
            print("You guessed it right. You won!!!")
            break
        # always decrement - while loop flag
        number_of_guesses -= 1
    # it has to be the end of the game
    if not number_of_guesses:
        print(f"Tha author was {question[1]}. You lost!!!")
    # gets the data for main  function flag in the while loop
    return str(input("If you want to play another game, type y, please: "))


if __name__ == "__main__":
    print(game())
