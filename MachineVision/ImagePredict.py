import random
import requests
from PIL import Image
import io

from Crud.Pill import get_pills, get_pill
from Crud.PillSchedule import get_pill_schedules


def random_pill_choice(properties, pills):
    scores = []
    for pill in pills:
        score = 0
        for string in properties:
            if string in pill.properties:
                score += 5
            else:
                score -= 1
        for string in pill.properties:
            if string not in properties:
                score -= 1
        scores.append(score)

    # Step 2: Transform Scores
    transformed_scores = [(score ** 2 if score >= 0 else -(score ** 2)) for score in scores]
    if min(transformed_scores) < 0:
        transformed_scores = [item - min(transformed_scores) + 1 for item in transformed_scores]

    # Step 3: Weighted Selection
    total_score = sum(transformed_scores)
    probabilities = [ts / total_score for ts in transformed_scores]
    chosen_pill = random.choices(pills, weights=probabilities, k=1)[0]

    return chosen_pill


def identify_pill(session, user_id, image: Image):
    pills = get_pills(session, 0, 100, user_id)

    url = "http://18.219.9.33:8000/process-image"
    api_key = "11223344"
    headers = {"api_key": api_key}

    image_buffer = io.BytesIO()
    image.save(image_buffer, format="JPEG")  # Specify format (e.g., JPEG, PNG)
    image_buffer.seek(0)
    response = requests.post(url, params=headers, files={"image": ('image.jpg', image_buffer, 'image/jpeg')})

    properties = sorted(response.json(), key=lambda x: len(x), reverse=True)[0]
    return random_pill_choice(properties, pills)


def identify_pills(session, user_id, image):
    pills = get_pills(session, 0, 100, user_id)

    url = "http://18.219.9.33:8000/process-image"
    api_key = "11223344"
    headers = {"api_key": api_key}

    image_buffer = io.BytesIO()
    image.save(image_buffer, format="JPEG")
    image_buffer.seek(0)
    response = requests.post(url, params=headers, files={"image": ('image.jpg', image_buffer, 'image/jpeg')})

    properties_list = response.json()

    pills_id = []
    for properties in properties_list:
        pills_id.append(random_pill_choice(properties, pills))
    return pills_id
