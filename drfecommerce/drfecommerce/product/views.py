from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from django.db import connection

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqliteConsoleLexer, SqlLexer
from sqlparse import format

from .models import Category, Brand,Product
from .serializers import CategorySerializer,BrandSerializer,ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple viewsets to viewing categories
    """

    queryset=Category.objects.all()
    @extend_schema(responses=CategorySerializer)
    def list(self,request):
        serializer=CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple viewsets to viewing brands 
    """

    queryset=Brand.objects.all()
    print(connection.queries)

    @extend_schema(responses=BrandSerializer)
    def list(self,request):
        serializer=BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
         

class ProductViewSet(viewsets.ViewSet):
    """
    A simple viewsets to viewing prodcuts
    """
    queryset=Product.objects.isactive()
    lookup_field="slug"

    def retrieve(self,request, slug=None):
        serializer=ProductSerializer(
            self.queryset.filter(slug=slug).select_related("category","brand"),
              many=True
              )
        x=self.queryset.filter(slug=slug)
        sqlformatted = format(str(x.query), reindent=True )
        # print(highlight(sqlformatted, SqliteConsoleLexer(),TerminalFormatter()))
        data= Response(serializer.data)

        q=list(connection.queries)
        print(q)
        # for qq in q:
        #     sqlformatted=format(str(qq["sql"]), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer() , TerminalFormatter()))

        return data

    @extend_schema(responses=ProductSerializer)
    def list(self,request):
        serializer=ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(
            methods=["get"],
            detail=False,
            url_path=r"category/(?P<category>\w+)/all",
            url_name="all",
            )
    def list_product_by_category(self,request, category=None):
        """
        A simple endpoints to return product by category
        """
        serializer=ProductSerializer(
            self.queryset.filter(category__name=category), many=True
            )
        return Response(serializer.data)


        