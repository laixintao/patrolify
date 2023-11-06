import OpenSSL
import ssl
from reporter.decorators import check, trigger
from reporter.target import Target
import logging

logger = logging.getLogger(__name__)


logger.info("loading the checker... contrib")


class SiteTarget(Target):
    def __init__(self, domain):
        self.domain = domain


@check(SiteTarget)
def check_site(target):
    cert = ssl.get_server_certificate(("www.google.com", 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    time = x509.get_notAfter()
    return True, time


@trigger(interval_seconds=1 * 60)
def generate_jobs():
    for domain in [
        "www.google.com",
        "www.twitter.com",
        "www.github.com",
        "kawabangga.com",
    ]:
        yield SiteTarget(domain=domain)
