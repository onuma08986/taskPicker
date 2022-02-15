from typing import Any, Dict
from django.http.response import HttpResponse
from django.shortcuts import render
from models import Service
from django.views.generic.edit import CreateView


class ServiceCreateView(CreateView):
    model = Service
    template_name = "jobflows/service_create_view.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
