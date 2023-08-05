from __future__ import annotations
from abc import ABC, abstractmethod


class Type(ABC):
    """ Abstract base class for all Cowait types. """

    @abstractmethod
    def validate(self, value: any, name: str) -> None:
        """ Validates a value as this type. Raises ValueError if invalid """
        raise NotImplementedError()

    def serialize(self, value: Type) -> object:
        """ Returns a JSON-serializable representation of the value """
        return value

    def deserialize(self, value: any) -> Type:
        """ Deserializes a JSON representation of a value """
        return value
