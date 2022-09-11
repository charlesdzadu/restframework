from dataclasses import field
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

from shop.models import Category, Product, Article

class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "active", "ecoscore", "category", "date_created", "date_updated"]


class CategorySerializer(ModelSerializer):

    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', "active", "description", "products"]

    def get_products(self, instance):
        queryset = instance.products.filter(active = True)
        serializer = ProductSerializer(queryset, many = True)
        return serializer.data
    
    def validate_name(self, value):
        if Category.objects.filter(name = value).exists():
            raise ValidationError("La catégorie existe déja")
        return value

class CategoryDetailSerializer(ModelSerializer):

    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', "active", "description", "products", "date_created", "date_updated"]

    def get_products(self, instance):
        queryset = instance.products.filter(active = True)
        serializer = ProductSerializer(queryset, many = True)
        return serializer.data




class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = ["id","name", "price", "description", "product", "active", ]