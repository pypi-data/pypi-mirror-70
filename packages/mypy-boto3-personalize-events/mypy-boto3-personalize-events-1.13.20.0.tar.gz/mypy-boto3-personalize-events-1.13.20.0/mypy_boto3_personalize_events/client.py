"""
Main interface for personalize-events service client

Usage::

    import boto3
    from mypy_boto3.personalize_events import PersonalizeEventsClient

    session = boto3.Session()

    client: PersonalizeEventsClient = boto3.client("personalize-events")
    session_client: PersonalizeEventsClient = session.client("personalize-events")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Any, Dict, List, TYPE_CHECKING, Type
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_personalize_events.type_defs import EventTypeDef


__all__ = ("PersonalizeEventsClient",)


class Exceptions:
    ClientError: Type[Boto3ClientError]
    InvalidInputException: Type[Boto3ClientError]


class PersonalizeEventsClient:
    """
    [PersonalizeEvents.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.20/reference/services/personalize-events.html#PersonalizeEvents.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.20/reference/services/personalize-events.html#PersonalizeEvents.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.20/reference/services/personalize-events.html#PersonalizeEvents.Client.generate_presigned_url)
        """

    def put_events(
        self, trackingId: str, sessionId: str, eventList: List[EventTypeDef], userId: str = None
    ) -> None:
        """
        [Client.put_events documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.20/reference/services/personalize-events.html#PersonalizeEvents.Client.put_events)
        """
