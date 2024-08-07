from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
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
    @extend_schema(responses=BrandSerializer)
    def list(self,request):
        serializer=BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)
         

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple viewsets to viewing prodcuts
    """
    queryset=Product.objects.all()
    lookup_field="slug"

    def retrieve(self,request, slug=None):
        serializer=ProductSerializer(
            self.queryset.filter(slug=slug),
              many=True
              )
        return Response(serializer.data)

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


        