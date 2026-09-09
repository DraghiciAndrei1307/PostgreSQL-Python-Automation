"""
URL configuration for django_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers

from provisioner_api import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"inf/vms", views.InfrastructureVMViewSet)
router.register(r'postgres/vms', views.PostgreSQLVMViewSet)
router.register(r'postgres/instances', views.PostgreSQLInstanceViewSet)
router.register(r'postgres/dbs', views.PostgreSQLDatabaseViewSet)
router.register(r'postgres/backups', views.PostgreSQLBackupViewSet)
router.register(r'postgres/users', views.PostgreSQLUserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework"
        )
    ),
    path('api/', include(router.urls)),
]
