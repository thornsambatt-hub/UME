from django.urls import path

from .views import (
    CategoryCollectionView,
    CategoryDetailView,
    LoginView,
    ManufacturerCollectionView,
    ManufacturerDetailView,
    ProductCollectionView,
    ProductDetailView,
    StockCollectionView,
    StockDetailView,
    StockOutView,
)


urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("categories/", CategoryCollectionView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    path("manufacturers/", ManufacturerCollectionView.as_view(), name="manufacturer-list"),
    path("manufacturers/<int:pk>/", ManufacturerDetailView.as_view(), name="manufacturer-detail"),
    path("products/", ProductCollectionView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("stocks/", StockCollectionView.as_view(), name="stock-list"),
    path("stocks/<int:pk>/", StockDetailView.as_view(), name="stock-detail"),
    path("stocks/<int:pk>/stock-out/", StockOutView.as_view(), name="stock-out"),
]
