#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" File for handling GUI for the Weather app """


from OpenGL import GL  # Needed monkey patch because of bugs on some device with OpenGL and PyQt5
import pkg_resources
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from weather.app.webmining import MeteoFrance
from weather.app.exceptions import MeteoFranceError
from weather.app.helpers import empty

# Load needed uis files
uifile_1 = pkg_resources.resource_filename('weather', 'ressources/qt_ui/weather_form.ui')
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = pkg_resources.resource_filename('weather', 'ressources/qt_ui/main_weather.ui')
form_2, base_2 = uic.loadUiType(uifile_2)


class WeatherForm(form_1, base_1):
    """ Class which show the entry form of the the weather app """

    def __init__(self):
        """
        Initialization of the form and behavior
        of the Weather app entry form
        """
        super(base_1, self).__init__()
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.print_weather)
        self.setWindowTitle("Weather APP")

    def print_weather(self):
        """
        Method for switching to the Main
        windows when form is sent
        """
        if not empty(self.city_edit.text()) or not empty(self.postalcode_edit.text()):
            try:
                meteofrance = MeteoFrance(city=self.city_edit.text(),
                                          postal_code=self.postalcode_edit.text())
                self.main = MainWeatherWindow(url=meteofrance.url)
                self.main.show()
                self.close()
            except MeteoFranceError as error:
                self.alert = AlertWindow(msg=str(error))
                self.alert.show()
                self.show()
        else:
            self.alert = AlertWindow(msg="At least one of two form should be filled")
            self.alert.show()
            self.show()


class MainWeatherWindow(form_2, base_2):
    """ Class for printing the weather """

    def __init__(self, url):
        """ Initialization of the WeatherGUI """
        super(base_2, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Weather APP")
        self.webview.load(QUrl(url))

        if self.other_weather.triggered:
            self.weather_form = WeatherForm()
            self.other_weather.triggered.connect(self.weather_form.show)
            self.close()


class AlertWindow(QMessageBox):
    """ Class for simuling an alert like JS Box """

    def __init__(self, msg, title="Alert !"):
        """ Initialize de class with a message """
        super(AlertWindow, self).__init__()
        self.setWindowTitle(title)
        self.setText(msg)
