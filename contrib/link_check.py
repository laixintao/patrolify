import OpenSSL
import ssl
from reporter.decorators import check, trigger
from reporter.target import Target


class SiteTarget(Target):
    def __init__(self, domain):
        self.domain = domain


@check(SiteTarget)
def check_site(target):
    cert = ssl.get_server_certificate(("www.google.com", 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    x509.get_notAfter()


@trigger(interval_seconds=3 * 60)
def generate_jobs():
    for domain in [
        "www.google.com",
        "www.twitter.com",
        "www.github.com",
        "kawabangga.com",
    ]:
        yield SiteTarget(domain=domain)
