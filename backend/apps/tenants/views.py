from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse


def tenant_test(request):

    if request.tenant:

        return JsonResponse({
            "empresa": request.tenant.nome,
            "banco": request.tenant.banco
        })


    return JsonResponse({
        "empresa": None
    })