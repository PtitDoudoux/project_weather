#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" File containing multiple helping functions """


import os
import requests
from app.exceptions import GeolocationError

def is_empty(any_structure):
    """
    | Check if a Python structure is empty
    | in the pythonic way
    |
    | :param structure: The structure to be checked of emptyness
    | :type any_structure: any
    | :return: True if the structure is empty, False otherwise
    | :rtype: bool
    """

    if any_structure:
        return False
    else:
        return True

def print_terminal_line_char(char='*'):
    """
    | Print a character that take all width in the terminal
    | :return: Nothing
    """

    terminal = os.get_terminal_size()

    column = 0
    while column < terminal[0]:
        print(char, end='')
        column += 1


def get_postal_code(city):
    """
    | Retrieve the postal code from a city code with the French
    | API WORK ONLY FOR FRANCE
    |
    | :param city: The city with unknow postal_code
    | :type text: string
    | :return: The postal_code associated to the city
    | :rtype: string
    """

    request = requests.get("https://geo.api.gouv.fr/communes?nom=" + city)
    request.raise_for_status()
    data = request.json()

    if is_empty(data):
        raise GeolocationError("The requested city could not be found")
    elif len(data) > 1:
        print("We cannot retrieve the exact postal code please inquire it : ", end='')
        postal_code = str(input())
    else:
        postal_code = data[0]["codesPostaux"][0]

    return postal_code


def get_city(postal_code):
    """
    | Retrieve the city from a postal code with the French
    | API WORK ONLY FOR FRANCE
    |
    | :param postal_code: The postal_code of the city
    | :type text: string
    | :return: The city associated to the postal_code
    | :rtype: string
    """

    request = requests.get("https://geo.api.gouv.fr/communes?codePostal=" + postal_code)
    request.raise_for_status()
    data = request.json()

    if is_empty(data):
        raise GeolocationError("The requested postal code could not be found")

    return data[0]["nom"]


def get_arrow_icon(text):
    """
    | Return the unicode icon depending on text crawled
    | on meteofrance.fr about the direction of the wind
    |
    | :param text: The text of the unicode associated
    | :type text: string
    | :return: The icon unicode of the text
    | :rtype: string
    """
    # TODO: Code this function
    pass


def get_weather_icon(text):
    """
    | Return the unicode icon depending on text crawled
    | on meteofrance.fr about the weather
    |
    | :param text: The text of the unicode associated
    | :type text: string
    | :return: The icon unicode of the text
    | :rtype: string
    """

    return {
        "Ensoleillé": "\U0001F323",
        "Nuit claire": "\U0001F319",
        "Ciel voilé": "\U0001F324",
        "Éclaircies": "\U000026C5",
        "Très nuageux": "\U00002601",
        "Brume ou bancs de brouillard": "\U0001F32B",
        "Brouillard": "\U0001F32B",
        "Brouillard givrant": "\U0001F32B",
        "Bruine": "\U0001F326",
        "Pluie faible": "\U0001F326",
        "Pluie verglaçante": "\U0001F327",
        "Pluies éparses": "\U0001F326",
        "Rares averses": "\U0001F326",
        "Pluie": "\U0001F327",
        "Averses": "\U0001F327",
        "Pluie forte": "\U0001F327",
        "Pluies orageuses": "\U000026C8",
        "Quelques flocons": "\U0001F328",
        "Pluie et neige": "\U0001F327 \U0001F328",
        "Neige": "\U0001F328",
        "Averses de neige": "\U0001F328",
        "Neige forte": "\U0001F328",
        "Risque de grêle": "\U0001F328",
        "Risque d’orages": "\U0001F329",
        'Orages': "\U0001F329",
    }.get(text, "\U00002620")


def print_presenter():
    """
    | Print a girl presenter in terminal
    |
    | :return: Nothing
    """
    print(r"""
        _._
      .'   '.       |
     / //\\\ \      |
    ( ( -\- ) )     |
     '-\_=_/-'      //
    .-'\   /'-.    (|/
   /    '-'    \  / /
   | \__   __/_/\/ /|
   | |\     / \   /
   \  \     \  '-'
    `\/\     ;
     |/|\    |
     |       |
     |       |
     |       |
     |_______|
      |  |  |
       \ | /
       /=|=\
      (_/T\_)
      """)
