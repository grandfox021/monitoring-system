from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


bot_id = 756551375

chat_id = 1386608470

api_token = "756551375:5IKEabRwxxG3FzgENgaj3zu24mQwFfEwQWRwEw9L"

bale_url = f"https://tapi.bale.ai/bot{api_token}/METHOD_NAME"


def home (request):
    return render(request, 'home.html')


def api_info(request):

    response = requests.get(bale_url.replace("METHOD_NAME", "getMe"))
    return JsonResponse(response.json())


def send_message(request, text):
    url = bale_url.replace("METHOD_NAME", "sendMessage")
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # همیشه JsonResponse برگردون
    try:
        return JsonResponse(response.json(), safe=False)
    except Exception:
        return JsonResponse({"status": "failed", "response": response.text})
    

@csrf_exempt
def post_alert(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Alertmanager payload:", data)

            url = bale_url.replace("METHOD_NAME", "sendMessage")

            # ساخت متن پیام مرتب
            text_lines = []
            alerts = data.get("alerts", [])
            for alert in alerts:
                name = alert.get("labels", {}).get("alertname", "NoName")
                severity = alert.get("labels", {}).get("severity", "unknown")
                instance = alert.get("labels", {}).get("instance", "")
                description = alert.get("annotations", {}).get("description", "No description")

                text_lines.append(
                    f"🚨 *{name}* (Severity: {severity})\n"
                    f"Instance: {instance}\n"
                    f"{description}\n"
                    "----------------------"
                )

            text = "\n".join(text_lines)

            payload = {
                "chat_id": chat_id,
                "text": text
            }
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)

            return JsonResponse({
                "status": "ok",
                "bale_response": response.json()
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "invalid method"}, status=405)