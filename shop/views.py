from unicodedata import category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from shop.permissions import IsAdminAuthenticated

from shop.models import Category, Product, Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer, CategoryDetailSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is None:
            return self.detail_serializer_class
        return super().get_serializer_class()



class CategoryAPIView(APIView):
    
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)





class ProductAPIView(APIView):

    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)


class CategoryViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):
    """On verra quoi mettre dedans"""
    serializer_class = CategorySerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active = True)


    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        category = self.get_object()
        category.disable()
        return Response()


class ProductViewSet(ReadOnlyModelViewSet):
    """On verra quoi mettre dedans"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active = True)
        
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id = category_id)
        
        return queryset




class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer


    def get_queryset(self):
        queryset = Article.objects.filter(active = True)

        product_id = self.request.GET.get("product_id")
        if product_id is not None:
            queryset = queryset.filter(product = product_id)
        return queryset







class AdminCategoryViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategorySerializer
    detail_serializer_class = CategoryDetailSerializer

    permission_classes = [IsAuthenticated, IsAdminAuthenticated]

    def get_queryset(self):
        return Category.objects.all()




