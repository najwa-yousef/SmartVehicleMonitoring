def check_speed(speed):

    SPEED_LIMIT = 100

    if speed > SPEED_LIMIT:
        return f"ALERT! Speed limit exceeded: {speed} km/h"

    return None