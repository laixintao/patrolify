from patrolify.decorators import trigger


@trigger(interval_seconds=2 * 60)
def generate_jobs(time_target):
    return True, "always pass"
