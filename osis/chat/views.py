from django.urls import reverse
from django.http import JsonResponse

def chat_endpoint(request, sender_id, recipient_id):
    room_name = f"{sender_id}_{recipient_id}"
    websocket_url = reverse('chat_endpoint', kwargs={'sender_id': sender_id, 'recipient_id': recipient_id})
    return JsonResponse({'websocket_url': f'ws://{request.get_host()}{websocket_url}'})
