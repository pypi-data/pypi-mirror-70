from .pywhois import _PyWhoIs
from .tlds import parser_supported_tlds

__all__ = ['lookup', 'aio_lookup', 'has_parser_support']
__version__ = '0.2.0'


def lookup(url: str, timeout: int = 10) -> _PyWhoIs:
    """
    Module entry point for whois lookups.

    :param url: Any correctly formatted URL (e.g. https://en.wikipedia.org/wiki/WHOIS)
    :param timeout: whois server connection timeout (default 10 seconds)
    :return: instance of _PyWhoIs with "query_output" and "parser_output" attributes
    """
    whois = _PyWhoIs._from_url(url, timeout)
    return whois


async def aio_lookup(url: str, timeout: int = 10) -> _PyWhoIs:
    """
    Async module entry point for whois lookups.

    :param url: Any correctly formatted URL (e.g. https://en.wikipedia.org/wiki/WHOIS)
    :param timeout: whois server connection timeout (default 10 seconds)
    :return: instance of _PyWhoIs with "query_output" and "parser_output" attributes
    """
    whois = await _PyWhoIs._aio_from_url(url, timeout)
    return whois


def has_parser_support(tld: str) -> bool:
    """
    Check if the module has explicit parser support for a given top level domain.

    :param tld: Top level domain (e.g. "com")
    :return: True if tld parser exists else False
    """
    tld = tld.lstrip(".")
    return tld in parser_supported_tlds
