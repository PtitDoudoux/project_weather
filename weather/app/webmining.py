#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
File For using webmining techniques
on diverse site here each class represented
a web-mined site
"""

import datetime
from abc import ABCMeta
import requests
from bs4 import BeautifulSoup
from .exceptions import GeolocationError, MeteoFranceError
from .helpers import get_city, get_postal_code, get_weather_icon, empty


class Location(metaclass=ABCMeta):
    """
    Abstract Class for defining a location (only in France ATM)
    which consist of a city and a postal code
    """

    def __init__(self, city, postal_code):
        """
        Initialise a location object with a given city and postal code

        :param city: The name of the city
        :param postal_code: The postal code
        :raises GeolocationError: Raise an exception if no city or postal code is inquired
        """

        if city is None and postal_code is not None:
            self.postal_code = str(postal_code)
            self.city = get_city(str(postal_code)).lower()
        elif city is not None and postal_code is None:
            self.city = city.lower()
            self.postal_code = get_postal_code(city)
        elif city is not None and postal_code is not None:
            self.postal_code = str(postal_code)
            self.city = city.lower()
        else:
            raise GeolocationError("You should at least inquire either the postal code or the city")


class MeteoFrance(Location):
    """ Class for mining some webpage of meteofrance.fr """

    def __init__(self, city, postal_code):
        """
        Initialize a MeteoFrance object with a given city and postal code
        and setup the connection to meteofrance.fr, plus scrap the content
        of the city / postal code webpage

        :param city: The city to retrieve the weather
        :param postal_code: The postal code to retrieve the weather
        """

        super(MeteoFrance, self).__init__(city, postal_code)
        self.session = requests.Session()
        self.weather = self._retrieve_web_page_content()

    def retrieve_weather(self, timestamps):
        """
        Return all Weather info from a city
        depending on the timestamps asked

        :param timestamps: The timestamps of the weather wanted
        :type timestamps: string
        :return: The weather associated
        :rtype: dict
        :raises ValueError: Raise an error if the timestamps is innapropriate
        """

        if timestamps == "today":
            return self.retrieve_daily_weather("today")
        elif timestamps == "tommorow":
            return self.retrieve_daily_weather("tommorow")
        elif timestamps == "after_tommorow":
            return self.retrieve_daily_weather("after_tommorow")
        elif timestamps == "week":
            return self.retrieve_weekly_weather()
        elif timestamps == "next_week":
            return self.retrieve_next_week_weather()
        else:
            raise ValueError("Error, Unknow type of daily retrieval")

    def retrieve_daily_weather(self, timestamps):
        """
        Return all Weather info from a city
        depending on the day asked

        :param timestamps: The timestamps of the weather wanted
        :type timestamps: string
        :return: The weather associated
        :rtype: dict
        :raises ValueError: Raise an error if the timestamps is innapropriate
        """

        if timestamps == "today":
            weather_datas = [data for data in self.weather[0].stripped_strings]
            time = datetime.datetime.now()
        elif timestamps == "tommorow":
            weather_datas = [data for data in self.weather[1].stripped_strings]
            time = datetime.datetime.now() + datetime.timedelta(days=1)
        elif timestamps == "after_tommorow":
            weather_datas = [data for data in self.weather[2].stripped_strings]
            time = datetime.datetime.now() + datetime.timedelta(days=2)
        else:
            raise ValueError("Error, Unknow type of daily retrieval")

        weather_infos = dict(geo=self.city.capitalize() + ' ' + self.postal_code,
                             datetime=weather_datas[0].capitalize() + '/' +
                                      str(time.month) + '/' + str(time.year),
                             temp=' '.join(weather_datas[1:4]),
                             weather_type=weather_datas[4],
                             weather_icon=get_weather_icon(weather_datas[4]),
                             uv=weather_datas[5],
                             wind=' '.join(weather_datas[6:])
                             )

        return weather_infos

    def retrieve_weekly_weather(self):
        """
        Return all Weather info from a city for the week

        :return: The weather associated
        :rtype: dict
        """

        for i in range(0, 7):
            time = datetime.datetime.now() + datetime.timedelta(days=i)
            weather_datas = [data for data in self.weather[i].stripped_strings]
            formatted_wd = {
                "geo": self.city.capitalize() + ' ' + self.postal_code,
                "datetime": weather_datas[0].capitalize() + '/' + str(time.month)
                            + '/' + str(time.year),
                "temp": ' '.join(weather_datas[1:4]),
                "weather_type": weather_datas[4],
                "weather_icon": get_weather_icon(weather_datas[4]),
            }

            if i < 4:
                formatted_wd["uv"] = weather_datas[5]
                formatted_wd["wind"] = ' '.join(weather_datas[6:])
            else:
                formatted_wd["wind"] = ' '.join(weather_datas[5:-1])  # TODO: Add wind direction
                formatted_wd["trust"] = weather_datas[-1]

            yield formatted_wd

    def retrieve_next_week_weather(self):
        """
        Return all Weather info from a city for the next week

        :return: The weather associated
        :rtype: dict
        """

        for i in range(8, 14):
            time = datetime.datetime.now() + datetime.timedelta(days=i)
            weather_datas = [data for data in self.weather[i].stripped_strings]
            formatted_wd = {
                "geo": self.city.capitalize() + ' ' + self.postal_code,
                "datetime": weather_datas[0].capitalize() + '/' + str(time.month)
                            + '/' + str(time.year),
                "temp": ' '.join(weather_datas[1:4]),
                "weather_type": weather_datas[4],
                "weather_icon": get_weather_icon(weather_datas[4]),
                "wind": ' '.join(weather_datas[6:9]) if len(weather_datas) > 9 else weather_datas[6],
                "trust": weather_datas[-1]
            }

            yield formatted_wd

    def _retrieve_web_page_content(self):
        """
        Get the content of the weather of meteofrance.fr
        web page as a text

        :return: The weather content of a MeteoFrance page
        :rtype: bs4.element.ResultSet
        :raises MeteoFranceError: Raise an error if the web page of the city
        or postal code doesn't exist
        :raises RequestException: Raise RequestException if any error related to
        to a request occured
        """

        headers = {"User-agent": "Mozilla/5.0"}
        self.session.headers.update(headers)

        query = self.city.upper() + ' (' + self.postal_code + ')'

        request = self.session.post("http://www.meteofrance.com/recherche/resultats",
                                    data={"facet": "previsions",
                                          "type-search": "previsions",
                                          "query": query})

        request.raise_for_status()

        soup = BeautifulSoup(request.text, 'html.parser')
        weather = soup.findAll("article", {"class": "bloc-day-summary"})

        self.url = request.url
        if empty(weather):
            raise MeteoFranceError("The weather couldn't be retrieved from your city / postal code")

        return weather
