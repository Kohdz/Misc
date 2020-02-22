import requests


def check_profanity(text_to_check):
    print(text_to_check)
    connection = requests.get(
        'http://www.wdylike.appspot.com/?q={}'.format(text_to_check))

    if connection.text == 'true':
        print("Curse Words Found")
    else:
        print("No Curse Words Found")


def read_text():
    quotes = open("email.txt")
    contents_of_file = quotes.read()
    check_profanity(contents_of_file)
    quotes.close()


read_text()
