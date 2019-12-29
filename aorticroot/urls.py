"""aorticroot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("objectives/", include("objectives.urls")),
    path("questions/", include("questions.urls")),
    path("users/", include("users.urls")),

    # Path for Open API schema
    path('openapi/', get_schema_view(
        title="Aortic Root API",
        description="API for AORTA.",
        version="0.2"
    ), name='openapi-schema'),

    # Path for Redoc schema view
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi-schema"}
        ),
    ),

]

urlpatterns = format_suffix_patterns(urlpatterns)
