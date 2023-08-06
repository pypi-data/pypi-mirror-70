#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Sequence
from typing import Sized

from neodroid.utilities.unity_specifications.unobservables import Unobservables

__author__ = "Christian Heider Nielsen"

import json

from .reaction_parameters import ReactionParameters


class Reaction(object):
    """

    """

    def __init__(
        self,
        *,
        parameters: ReactionParameters = None,
        motions: Sized = (),
        configurations: Sequence = (),
        unobservables: Unobservables = None,
        displayables: Sequence = None,
        environment_name: str = "None",
        serialised_message: str = "",
    ):
        """

The environment_name argument lets you specify which environments to react in, 'all' means all environment
receives the same reaction.

"""

        self._serialised_message = serialised_message
        self._environment_name = environment_name
        if not parameters:
            parameters = ReactionParameters()
        self._parameters = parameters
        self._configurations = configurations
        self._motions = motions
        self._unobservables = unobservables
        self._displayables = displayables

    @property
    def environment_name(self):
        """

        @return:
        @rtype:
        """
        return self._environment_name

    @property
    def parameters(self):
        """

        @return:
        @rtype:
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        self._parameters = parameters

    @property
    def motions(self):
        """

        @return:
        @rtype:
        """
        return self._motions

    @motions.setter
    def motions(self, motions):
        self._motions = motions

    @property
    def configurations(self):
        """

        @return:
        @rtype:
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        self._configurations = configurations

    @property
    def displayables(self):
        """

        @return:
        @rtype:
        """
        return self._displayables

    @displayables.setter
    def displayables(self, displayables):
        self._displayables = displayables

    @property
    def unobservables(self):
        """

        @return:
        @rtype:
        """
        return self._unobservables

    @unobservables.setter
    def unobservables(self, unobservables):
        self._unobservables = unobservables

    @property
    def serialised_message(self):
        """

        @return:
        @rtype:
        """
        return self._serialised_message

    @serialised_message.setter
    def serialised_message(self, message):
        self._serialised_message = message

    def to_dict(self):
        """

        @return:
        @rtype:
        """
        return {
            "_configurations": [
                configuration.to_dict() for configuration in self._configurations
            ],
            "_motions": [motion.to_dict() for motion in self._motions],
        }

    def to_json(self):
        """

        @return:
        @rtype:
        """
        return json.dumps(self.to_dict())

    def __repr__(self):
        return (
            f"<Reaction>\n"
            f"<environment_name>{self.environment_name}</environment_name>\n"
            f"<configurations>\n{self.configurations}</configurations>\n"
            f"<motions>\n{self.motions}</motions>\n"
            f"<parameters>\n{self.parameters}</parameters>\n"
            f"<configurations>\n{self.configurations}</configurations>\n"
            f"<displayables>\n{self.displayables}</displayables>\n"
            f"<unobservables>\n{self.unobservables}</unobservables>\n"
            f"<serialised_message>{self.serialised_message}</serialised_message>\n"
            f"</Reaction>\n"
        )

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__repr__()
