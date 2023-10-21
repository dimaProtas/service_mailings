from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, MailingListViewSet, MessageViewSet, TimeZoneViewSet, OperatorCodeViewSet, TagViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="API mailing DRF",
        default_version='v1',
        description="Message sending service",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="dima_protasevich92@mail.ru"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailing_lists', MailingListViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'timezone', TimeZoneViewSet)
router.register(r'tag', TagViewSet)
router.register(r'operator_code', OperatorCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mailing_list/delete/<int:pk>/', MailingListViewSet.as_view({'delete': 'delete_mailing_list'})),
    path('client/delete/<int:pk>/', ClientViewSet.as_view({'delete': 'delete_client'})),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
