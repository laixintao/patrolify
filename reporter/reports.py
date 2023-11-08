import logging


logger = logging.getLogger(__name__)


def generate_report(check_name, check_id):
    logger.info("Start to generate reports for %s check_id=%s", check_name, check_id)
