from enum import Enum


class OrderStatusEnum(Enum):
    NEW = "new"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELED = "canceled"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]
