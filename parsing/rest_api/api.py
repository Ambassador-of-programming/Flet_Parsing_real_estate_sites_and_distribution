import httpx


def get_instance(TOKEN: str):
    url = f"https://whatsmonster.ru/api/create_instance?access_token={TOKEN}"

    try:
        with httpx.Client() as client:
            response = client.get(url)
            result = response.json()
            return str(result['instance_id'])
    except httpx.RequestError as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


def send_message(phone_number: str, message: str, instance_id: str, access_token: str):
    url = "https://whatsmonster.ru/api/send"

    data = {
        "number": phone_number,
        "type": 'text',
        "message": message,
        "instance_id": str(instance_id),
        "access_token": str(access_token)
    }

    with httpx.Client() as client:
        # POST запрос с JSON телом
        headers = {"Content-Type": "application/json"}
        response = client.post(url, json=data, headers=headers)

        return response.json()
