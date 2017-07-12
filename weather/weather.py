#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" File for handling CLI inputs for the Weather app """


import sys
import fire
from requests.exceptions import RequestException
from PyQt5.QtWidgets import QApplication
from .app.exceptions import GeolocationError, MeteoFranceError
from .app.webmining import MeteoFrance
from .app.gui import WeatherForm
from .app.helpers import print_presenter, print_terminal_line_char


class Weather:
    """ A Weather Fire class for CLI purpose """

    def today(self, city=None, postal_code=None):  # pylint: disable=R0201
        """ Retrieve and print in terminal the today weather """

        try:
            meteo_france = MeteoFrance(city, postal_code)
            weather = meteo_france.retrieve_weather("today")
        except (GeolocationError, MeteoFranceError, RequestException,
                ValueError) as error:
            sys.exit(error)

        print_terminal_line_char('*')
        print("* A :", weather["geo"])
        print("* Au :", weather["datetime"])
        print("* La température sera de :", weather["temp"])
        print("* Quant au temps :", weather["weather_type"], weather["weather_icon"])
        print("* Les UVs :", weather["uv"])
        print("* Et le vent :", weather["wind"])
        print_terminal_line_char('*')

    def tommorow(self, city=None, postal_code=None):  # pylint: disable=R0201
        """ Retrieve and print in terminal the tommorow weather """

        try:
            meteo_france = MeteoFrance(city, postal_code)
            weather = meteo_france.retrieve_weather("tommorow")
        except (GeolocationError, MeteoFranceError, RequestException,
                ValueError) as error:
            sys.exit(error)

        print_terminal_line_char('*')
        print("* A :", weather["geo"])
        print("* Au :", weather["datetime"])
        print("* La température sera de :", weather["temp"])
        print("* Quant au temps :", weather["weather_type"], weather["weather_icon"])
        print("* Les UVs :", weather["uv"])
        print("* Et le vent :", weather["wind"])
        print_terminal_line_char('*')

    def after_tommorow(self, city=None, postal_code=None):  # pylint: disable=R0201
        """ Retrieve and print in terminal the after tommorow weather """

        try:
            meteo_france = MeteoFrance(city, postal_code)
            weather = meteo_france.retrieve_weather("after_tommorow")
        except (GeolocationError, MeteoFranceError, RequestException,
                ValueError) as error:
            sys.exit(error)

        print_terminal_line_char('*')
        print("* A :", weather["geo"])
        print("* Au :", weather["datetime"])
        print("* La température sera de :", weather["temp"])
        print("* Quant au temps :", weather["weather_type"], weather["weather_icon"])
        print("* Les UVs :", weather["uv"])
        print("* Et le vent :", weather["wind"])
        print_terminal_line_char('*')

    def week(self, city=None, postal_code=None):  # pylint: disable=R0201
        """ Retrieve and print in terminal the week weather """

        try:
            meteo_france = MeteoFrance(city, postal_code)
            weather = meteo_france.retrieve_weather("week")
        except (GeolocationError, MeteoFranceError, RequestException,
                ValueError) as error:
            sys.exit(error)

        print_terminal_line_char('*')
        for wd_el in weather:

            print("* A :", wd_el["geo"])
            print("* Au :", wd_el["datetime"])
            print("* La température sera de :", wd_el["temp"])
            print("* Quant au temps :", wd_el["weather_type"], wd_el["weather_icon"])
            if "uv" in wd_el:
                print("* Les UVs :", wd_el["uv"])
            print("* Et le vent :", wd_el["wind"])
            if "trust" in wd_el:
                print("* Indice de confiance :", wd_el["trust"])
            print_terminal_line_char('*')

    def next_week(self, city=None, postal_code=None):  # pylint: disable=R0201
        """ Retrieve and print in terminal the next week weather """

        try:
            meteo_france = MeteoFrance(city, postal_code)
            weather = meteo_france.retrieve_weather("next_week")
        except (GeolocationError, MeteoFranceError, RequestException,
                ValueError) as error:
            sys.exit(error)

        print_terminal_line_char('*')
        for wd_el in weather:
            print("* A :", wd_el["geo"])
            print("* Au :", wd_el["datetime"])
            print("* La température sera de :", wd_el["temp"])
            print("* Quant au temps :", wd_el["weather_type"], wd_el["weather_icon"])
            print("* Et le vent :", wd_el["wind"])
            print("* Indice de confiance :", wd_el["trust"])
            print_terminal_line_char('*')

    def presenter(self):  # pylint: disable=R0201
        """ LOL Func who print a female presenter for the meteo """

        print("Say Hi to Évelyne Dhéliat !")
        print_presenter()

    def gui(self):  # pylint: disable=R0201
        """ Function for launching the Weather GUI """
        app = QApplication(sys.argv)
        weather_gui = WeatherForm()
        weather_gui.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    fire.Fire(Weather)
