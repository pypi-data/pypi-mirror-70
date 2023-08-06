"""
Main interface for cur service type definitions.

Usage::

    from mypy_boto3.cur.type_defs import DeleteReportDefinitionResponseTypeDef

    data: DeleteReportDefinitionResponseTypeDef = {...}
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "DeleteReportDefinitionResponseTypeDef",
    "ReportDefinitionTypeDef",
    "DescribeReportDefinitionsResponseTypeDef",
    "PaginatorConfigTypeDef",
)

DeleteReportDefinitionResponseTypeDef = TypedDict(
    "DeleteReportDefinitionResponseTypeDef", {"ResponseMessage": str}, total=False
)

_RequiredReportDefinitionTypeDef = TypedDict(
    "_RequiredReportDefinitionTypeDef",
    {
        "ReportName": str,
        "TimeUnit": Literal["HOURLY", "DAILY"],
        "Format": Literal["textORcsv", "Parquet"],
        "Compression": Literal["ZIP", "GZIP", "Parquet"],
        "AdditionalSchemaElements": List[Literal["RESOURCES"]],
        "S3Bucket": str,
        "S3Prefix": str,
        "S3Region": Literal[
            "us-east-1",
            "us-west-1",
            "us-west-2",
            "eu-central-1",
            "eu-west-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "eu-north-1",
            "ap-northeast-3",
            "ap-east-1",
        ],
    },
)
_OptionalReportDefinitionTypeDef = TypedDict(
    "_OptionalReportDefinitionTypeDef",
    {
        "AdditionalArtifacts": List[Literal["REDSHIFT", "QUICKSIGHT", "ATHENA"]],
        "RefreshClosedReports": bool,
        "ReportVersioning": Literal["CREATE_NEW_REPORT", "OVERWRITE_REPORT"],
    },
    total=False,
)


class ReportDefinitionTypeDef(_RequiredReportDefinitionTypeDef, _OptionalReportDefinitionTypeDef):
    pass


DescribeReportDefinitionsResponseTypeDef = TypedDict(
    "DescribeReportDefinitionsResponseTypeDef",
    {"ReportDefinitions": List[ReportDefinitionTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
