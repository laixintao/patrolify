from patrolify.decorators import check, trigger
from patrolify.target import Target
import logging

logger = logging.getLogger(__name__)


class MyCheckTarget(Target):
    def __init__(self, string_data):
        super().__init__()
        self.my_string = string_data

    def __str__(self) -> str:
        return f"this is my target: {self.my_string}"


@check(MyCheckTarget)
def check_my_target(target):
    check_success = True
    if check_success:
        return True, f"the check is passed"
    else:
        return False, f"The check is failed because ..."


@trigger(cron_string="* * * * *", description="As a job example")
def generate_jobs(time_target):
    my_check_list = []
    for target_id in my_check_list:
        yield MyCheckTarget(target_id)

    # can always return this
    return True, "The job has been started"
