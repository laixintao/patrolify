from patrolify.decorators import trigger


def today_is_sunnyday():
    return True


@trigger(cron_string="* * * * *", description="Check todays weather")
def check_weather(time_target):
    if today_is_sunnyday():
        return True, "I'm very happy"
    else:
        return False, "I'm not happy"
