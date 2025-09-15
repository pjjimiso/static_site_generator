# main.py

from textnode import TextType
from textnode import TextNode


def main(): 
    some_text = TextNode("This is an anchor link", TextType.LINK, "https://www.thumpertherapy.com")
    print(some_text)


if __name__ == "__main__": 
    main()

