"""
URL configuration for autotune project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from workflow.views import (
    ConfigView,
    DatasetView,
    HealthCheckView,
    ModelIterationView,
    PingCheckView,
    TaskView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("task/status/<uuid:task_id>/", TaskView.as_view(), name="task-status"),
    path("v1/workflow/", include(("workflow.urls", "workflow"), namespace="v1")),
    path("v2/workflow/", include(("workflowV2.urls", "workflowV2"), namespace="v2")),
    path("config", ConfigView.as_view(), name="config"),
    path("datasets/", DatasetView.as_view(), name="dataset-list"),
    path("health/", HealthCheckView.as_view(), name="health_check"),
    path("health/ping", PingCheckView.as_view(), name="health_check"),
    path("model/iterate/", ModelIterationView.as_view(), name="model-iteration"),
]
