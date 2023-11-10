import logging
import glob
from .globals import g


logger = logging.getLogger(__name__)


def generate_report(check_name, check_id):
    logger.info("Start to generate reports for %s check_id=%s", check_name, check_id)
    check_directory = g.result_dir(check_name, check_id)

    for file in glob.glob(str(check_directory / "*.json")):
        logger.debug("Parse result %s...", file)

    # render to html

    # upload reports...
