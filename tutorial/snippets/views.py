from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, SnippetModelSerializer


class SnippetList(APIView):
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get(self, request, format=None):
        print(request.user.username)
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        self.action
        return Response(serializer.data)

    def patch(self, *args, **kwargs):
        return Response(data={'here': 'Patch'})

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    startswith_title = filters.CharFilter(field_name='title', method='filter_startswith_title')

    def filter_startswith_title(self, queryset, name, value):
        title_filter = {f'{name}__startswith': value}
        return queryset.filter(**title_filter)

    class Meta:
        model = Snippet
        fields = ('title', 'code', 'linenos', 'language', 'style', 'price',)


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SnippetFilter
