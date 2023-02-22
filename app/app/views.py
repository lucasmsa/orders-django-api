from django.http import JsonResponse


def health_check(_request):
    status = {
        'Status': '✅',
    }
    return JsonResponse(status)