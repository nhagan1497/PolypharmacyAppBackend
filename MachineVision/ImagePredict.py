import random

from Crud.Pill import get_pills, get_pill
from Crud.PillSchedule import get_pill_schedules


def identify_pill(session, user_id, image):
    pills = get_pills(session, 0, 100, user_id)
    pill = random.choice(pills)
    return pill


def identify_pills(session, user_id, image):
    pill_schedules = get_pill_schedules(session, 0, 100, user_id)

    num_items = random.randint(1, len(pill_schedules))
    pill_schedules = random.sample(pill_schedules, num_items)
    pills = []
    for pill_schedule in pill_schedules:
        pills.append(get_pill(session, pill_schedule.pill_id, user_id))

    return pills
