import requests


def vk_wall_post(token: str, message: str, group_id: int) -> int:
    url = "https://api.vk.com/method/wall.post"
    response = requests.post(
        url=url,
        params={
            "access_token": token,
            "from_group": 1,
            "owner_id": -group_id,
            "message": message,
            "v": "5.131",
        },
        timeout=10,
    )
    return response.status_code
