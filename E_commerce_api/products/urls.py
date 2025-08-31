

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet
from django.urls import path, include

from .views import UserViewSet



router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'users', UserViewSet, basename='user')


#urlpatterns = [
#    path('api/', include(router.urls)),
    
#]

urlpatterns = router.urls