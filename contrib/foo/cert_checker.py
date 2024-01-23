import OpenSSL
from datetime import datetime
import ssl
from patrolify.decorators import check, trigger
from patrolify.target import Target
import logging

logger = logging.getLogger(__name__)


logger.info("loading the checker... contrib")


class SiteTarget(Target):
    def __init__(self, domain):
        super().__init__()
        self.domain = domain

    def __str__(self) -> str:
        return self.domain


@check(SiteTarget)
def check_site(target):
    domain = target.domain
    cert = ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    time = x509.get_notAfter()
    date_string = time.decode()
    format_string = "%Y%m%d%H%M%SZ"
    parsed_datetime = datetime.strptime(date_string, format_string)

    days = (parsed_datetime - datetime.now()).days

    if days > 30:
        return True, f"{target.domain} will be expired in {days}days."
    else:
        return False, f"{target.domain} will be expired in {days}days."


@trigger(interval_seconds=1 * 60)
def generate_jobs(time_target):
    for domain in [
        "www.google.com",
        "www.twitter.com",
        "www.github.com",
        "abc.com",
        "asdf.com",
        "kawabangga.com",
        "aaaaaaaaaaaaaaaaaaaaaa.com",
    ]:
        yield SiteTarget(domain=domain)

    return True, "The job has been started"
