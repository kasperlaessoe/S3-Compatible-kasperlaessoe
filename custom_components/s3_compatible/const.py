"""Constants for the S3 Compatible integration."""

from collections.abc import Callable
import ssl
from typing import Final

import certifi
from botocore.config import Config
from botocore.loaders import Loader

from homeassistant.util.hass_dict import HassKey

DOMAIN: Final = "s3_compatible"

CONF_ACCESS_KEY_ID = "access_key_id"
CONF_SECRET_ACCESS_KEY = "secret_access_key"
CONF_ENDPOINT_URL = "endpoint_url"
CONF_BUCKET = "bucket"
CONF_PREFIX = "prefix"
CONF_REGION = "region"
CONF_VERIFY = "verify"

AWS_DOMAIN = "amazonaws.com"
DEFAULT_REGION = "us-east-1"
DEFAULT_ENDPOINT_URL = f"https://s3.{DEFAULT_REGION}.{AWS_DOMAIN}/"

DATA_BACKUP_AGENT_LISTENERS: HassKey[list[Callable[[], None]]] = HassKey(
    f"{DOMAIN}.backup_agent_listeners"
)

DESCRIPTION_AWS_S3_DOCS_URL = "https://docs.aws.amazon.com/general/latest/gr/s3.html"
DESCRIPTION_BOTO3_DOCS_URL = "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html"

BOTO_CONFIG = Config(
    request_checksum_calculation="when_required",
    response_checksum_validation="when_required",
)

_BOTOCORE_PRELOADED = False


def preload_botocore_data() -> None:
    """Pre-load botocore service data and SSL certs.

    This function should be called in an executor before creating aiobotocore
    clients to avoid blocking the event loop with synchronous I/O operations.
    Botocore caches loaded service data, so this only needs to happen once.
    """
    global _BOTOCORE_PRELOADED
    if _BOTOCORE_PRELOADED:
        return

    loader = Loader()
    loader.load_service_model("s3", "service-2")

    ctx = ssl.create_default_context()
    ctx.load_verify_locations(certifi.where())

    _BOTOCORE_PRELOADED = True
