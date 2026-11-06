import requests
from django.conf import settings

headers = {
    "Authorization": f"Bearer {settings.YOUSIGN_API_KEY}",
}

response = requests.get(
    f"{settings.YOUSIGN_BASE_URL}/users/me",
    headers=headers,
)

print(response.status_code)
print(response.json())