from dataclasses import field
from typing import ClassVar, Type, List, Optional


from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class MessageFrom:
    def __init__(self):
        pass

    id: int
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    def __init__(self):
        pass

    id: int
    username: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    def __init__(self):
        pass

    message_id: int
    msg_from: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: Optional[str] = None

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    def __init__(self):
        pass

    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    def __init__(self):
        pass

    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    def __init__(self):
        pass

    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


