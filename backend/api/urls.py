from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, IssueViewSet, LabelViewSet, issue_webhook

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'labels', LabelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/', issue_webhook),
]