#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
| File containing custom Exceptions related
| to the app
"""

class MeteoFranceError(Exception):
    """
    | Exception raised when a postal code doesn't
    | exist or is misformed
    """
    pass

class GeolocationError(Exception):
    """
    | Exception raised when a postal code doesn't
    | exist or is misformed
    """
    pass
