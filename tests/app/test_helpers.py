#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Testing file of the app/helpers.py """


import pytest
from project_weather.app.exceptions import GeolocationError
from project_weather.app.helpers import empty, get_city, get_postal_code


@pytest.fixture
def test_postal_code_values(tpcv=""):
    """ Pytest fixture of postal code for testing purposes """
    return {
        "good_postal_code": "93700",
        "bad_postal_code": "21444477788",
        "misformed_postal_code": "i wan't you to bug"
    }.get(tpcv, "")


@pytest.fixture
def test_city_values(tcv=""):
    """ Pytest fixture of postal code for testing purposes """
    return {
        "good_city": "Drancy",
        "bad_city": "azertyuiop",
        "misformed_city": "80085",
        "paris_case": "Paris"
    }.get(tcv, "")


def test_empty():
    """ Test if the function check well is a structure is empty or not """

    empty_str = ""
    empty_list = []
    empty_dict = {}

    assert empty(empty_str) is True
    assert empty(empty_list) is True
    assert empty(empty_dict) is True

    not_empty_str = "test"
    not_empty_list = ['t', 'e', 's', 't']
    not_empty_dict = {"foo": "bar"}

    assert empty(not_empty_str) is False
    assert empty(not_empty_list) is False
    assert empty(not_empty_dict) is False


def test_get_postal_code():
    """
    Test if a city is retrieved from a postal code
    and raise an GeolocationError if the postal is misformed
    """

    good_city = test_city_values("good_city")
    test_postal_code = get_postal_code(good_city)
    assert test_postal_code == "93700"

    # TODO: Test Paris Case
    # paris_case = test_city_values("paris_case")
    # test_postal_code = get_postal_code(paris_case)

    with pytest.raises(GeolocationError):
        bad_city = test_city_values("bad_city")
        get_postal_code(bad_city)

    with pytest.raises(GeolocationError):
        empty_city = test_city_values()
        get_postal_code(empty_city)


def test_get_city():
    """
    Test if a postal_code is retrieved from a city
    and raise an GeolocationError if the postal is misformed
    """

    good_postal_code = test_postal_code_values("good_postal_code")
    test_city = get_city(good_postal_code)
    assert test_city == "Drancy"

    with pytest.raises(GeolocationError):
        bad_postal_code = test_postal_code_values("bad_postal_code")
        get_city(bad_postal_code)

    with pytest.raises(GeolocationError):
        empty_postal_code = test_postal_code_values()
        get_city(empty_postal_code)
