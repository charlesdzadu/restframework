from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from shop import views 

router = routers.SimpleRouter()
router.register('category', views.CategoryViewSet, basename="category")
router.register('admin/category', views.AdminCategoryViewSet, basename="admin-category")
router.register('product', views.ProductViewSet, basename="product")
router.register('article', views.ArticleViewset, basename="article")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', TokenObtainPairView.as_view() , name="token_obtain_pair"),
    path('api/token/refresh', TokenRefreshView.as_view() , name="token_refresh"),
    path('api/', include(router.urls))

]
