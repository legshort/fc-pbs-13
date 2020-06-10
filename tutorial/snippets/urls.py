from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from snippets.views import SnippetList, SnippetDetail, SnippetViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'snippets', SnippetViewSet)

urlpatterns = router.urls
