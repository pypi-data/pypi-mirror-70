# coding: utf-8

"""
    Bot Action Server

    Allows custom Rocket League bots to accept tactical suggestions in the middle of a game.  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: rlbotofficial@gmail.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class AvailableActions(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'entity_name': 'str',
        'current_action': 'BotAction',
        'available_actions': 'list[BotAction]'
    }

    attribute_map = {
        'entity_name': 'entityName',
        'current_action': 'currentAction',
        'available_actions': 'availableActions'
    }

    def __init__(self, entity_name=None, current_action=None, available_actions=None):  # noqa: E501
        """AvailableActions - a model defined in Swagger"""  # noqa: E501
        self._entity_name = None
        self._current_action = None
        self._available_actions = None
        self.discriminator = None
        if entity_name is not None:
            self.entity_name = entity_name
        if current_action is not None:
            self.current_action = current_action
        if available_actions is not None:
            self.available_actions = available_actions

    @property
    def entity_name(self):
        """Gets the entity_name of this AvailableActions.  # noqa: E501

        The name of the bot or script that these actions are associated with.  # noqa: E501

        :return: The entity_name of this AvailableActions.  # noqa: E501
        :rtype: str
        """
        return self._entity_name

    @entity_name.setter
    def entity_name(self, entity_name):
        """Sets the entity_name of this AvailableActions.

        The name of the bot or script that these actions are associated with.  # noqa: E501

        :param entity_name: The entity_name of this AvailableActions.  # noqa: E501
        :type: str
        """

        self._entity_name = entity_name

    @property
    def current_action(self):
        """Gets the current_action of this AvailableActions.  # noqa: E501


        :return: The current_action of this AvailableActions.  # noqa: E501
        :rtype: BotAction
        """
        return self._current_action

    @current_action.setter
    def current_action(self, current_action):
        """Sets the current_action of this AvailableActions.


        :param current_action: The current_action of this AvailableActions.  # noqa: E501
        :type: BotAction
        """

        self._current_action = current_action

    @property
    def available_actions(self):
        """Gets the available_actions of this AvailableActions.  # noqa: E501


        :return: The available_actions of this AvailableActions.  # noqa: E501
        :rtype: list[BotAction]
        """
        return self._available_actions

    @available_actions.setter
    def available_actions(self, available_actions):
        """Sets the available_actions of this AvailableActions.


        :param available_actions: The available_actions of this AvailableActions.  # noqa: E501
        :type: list[BotAction]
        """

        self._available_actions = available_actions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AvailableActions, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AvailableActions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
