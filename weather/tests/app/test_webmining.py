#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Testing file of the app/webmining.py """


import pytest
import bs4
from weather.app.webmining import MeteoFrance
from weather.app.exceptions import MeteoFranceError
from weather.app.helpers import empty


@pytest.fixture
def good_meteofrance():
    """
    Pytest fixture for working with a predifined
    well formed MeteoFrance object
    """
    return MeteoFrance("drancy", "93700")


@pytest.fixture
def bad_meteofrance():
    """
    Pytest fixture for working with a predifined
    bad formed MeteoFrance object
    """
    return MeteoFrance("city_that_does_not_exist", "0123456789")


def test_meteofrance_retrieve_weather():
    """
    Function for testing if the method retrieve_weather
    of the class MeteoFrance behave as expected
    only the exception is tested because of the wrapper nature
    of this function
    """

    gmf = good_meteofrance()
    with pytest.raises(ValueError):
        gmf.retrieve_weather("buggy")


def test_meteofrance_retrieve_daily_weather():
    """
    Function for testing if the method retrieve_daily_weather
    of the class MeteoFrance behave as expected
    """

    gmf = good_meteofrance()

    assert isinstance(gmf.retrieve_daily_weather("today"), dict)
    assert isinstance(gmf.retrieve_daily_weather("tommorow"), dict)
    assert isinstance(gmf.retrieve_daily_weather("after_tommorow"), dict)

    with pytest.raises(ValueError):
        gmf.retrieve_daily_weather("buggy")


def test_meteofrance_retrieve_weekly_weather():
    """
    Function for testing if the method retrieve_weekly_weather
    of the class MeteoFrance behave as expected
    """

    gmf = good_meteofrance()
    assert all(isinstance(wd_el, dict) for wd_el in gmf.retrieve_weekly_weather())
    assert all(empty(wd_el) is False for wd_el in gmf.retrieve_weekly_weather())


def test_meteofrance_retrieve_next_week_weather():
    """
    Function for testing if the method retrieve_next_week_weather
    of the class MeteoFrance behave as expected
    """

    gmf = good_meteofrance()
    assert all(isinstance(wd_el, dict) for wd_el in gmf.retrieve_next_week_weather())
    assert all(empty(wd_el) is False for wd_el in gmf.retrieve_next_week_weather())


def test_meteofrance_retrieve_web_page_content():
    """
    Function for testing if the method retrieve_web_page_content
    of the class MeteoFrance behave as expected
    """

    gmf = good_meteofrance()
    assert isinstance(gmf.weather, bs4.element.ResultSet)
    assert all(isinstance(elem, bs4.element.Tag) for elem in gmf.weather)

    with pytest.raises(MeteoFranceError):
        bad_meteofrance()
