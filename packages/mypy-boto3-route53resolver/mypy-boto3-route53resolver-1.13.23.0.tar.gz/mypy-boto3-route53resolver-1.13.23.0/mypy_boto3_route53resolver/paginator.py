"""
Main interface for route53resolver service client paginators.

Usage::

    import boto3
    from mypy_boto3.route53resolver import (
        ListTagsForResourcePaginator,
    )

    client: Route53ResolverClient = boto3.client("route53resolver")

    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Iterator, TYPE_CHECKING
from botocore.paginate import Paginator as Boto3Paginator
from mypy_boto3_route53resolver.type_defs import (
    ListTagsForResourceResponseTypeDef,
    PaginatorConfigTypeDef,
)


__all__ = ("ListTagsForResourcePaginator",)


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Paginator.ListTagsForResource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.23/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource)
    """

    def paginate(
        self, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceResponseTypeDef]:
        """
        [ListTagsForResource.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.13.23/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource.paginate)
        """
