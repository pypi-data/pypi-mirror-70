"""
Main interface for mediaconnect service.

Usage::

    ```python
    import boto3
    from mypy_boto3_mediaconnect import (
        Client,
        ListEntitlementsPaginator,
        ListFlowsPaginator,
        MediaConnectClient,
    )

    session = boto3.Session()

    client: MediaConnectClient = boto3.client("mediaconnect")
    session_client: MediaConnectClient = session.client("mediaconnect")

    list_entitlements_paginator: ListEntitlementsPaginator = client.get_paginator("list_entitlements")
    list_flows_paginator: ListFlowsPaginator = client.get_paginator("list_flows")
    ```
"""
from mypy_boto3_mediaconnect.client import MediaConnectClient, MediaConnectClient as Client
from mypy_boto3_mediaconnect.paginator import ListEntitlementsPaginator, ListFlowsPaginator


__all__ = ("Client", "ListEntitlementsPaginator", "ListFlowsPaginator", "MediaConnectClient")
