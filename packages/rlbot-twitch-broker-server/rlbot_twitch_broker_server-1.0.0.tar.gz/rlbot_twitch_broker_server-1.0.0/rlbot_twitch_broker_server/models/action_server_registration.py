# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from rlbot_twitch_broker_server.models.base_model_ import Model
from rlbot_twitch_broker_server import util


class ActionServerRegistration(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, base_url: str=None):  # noqa: E501
        """ActionServerRegistration - a model defined in Swagger

        :param base_url: The base_url of this ActionServerRegistration.  # noqa: E501
        :type base_url: str
        """
        self.swagger_types = {
            'base_url': str
        }

        self.attribute_map = {
            'base_url': 'baseUrl'
        }
        self._base_url = base_url

    @classmethod
    def from_dict(cls, dikt) -> 'ActionServerRegistration':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ActionServerRegistration of this ActionServerRegistration.  # noqa: E501
        :rtype: ActionServerRegistration
        """
        return util.deserialize_model(dikt, cls)

    @property
    def base_url(self) -> str:
        """Gets the base_url of this ActionServerRegistration.


        :return: The base_url of this ActionServerRegistration.
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str):
        """Sets the base_url of this ActionServerRegistration.


        :param base_url: The base_url of this ActionServerRegistration.
        :type base_url: str
        """

        self._base_url = base_url
