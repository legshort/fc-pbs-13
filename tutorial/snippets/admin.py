from django.contrib import admin
from rest_framework import authtoken

from snippets.models import Snippet

admin.register(authtoken)


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'linenos', 'language', 'style', 'price',)
