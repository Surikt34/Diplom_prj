from enum import Enum


class UserRoleEnum(Enum):
    CLIENT = "client"
    SUPPLIER = "supplier"
    ADMIN = "admin"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]
