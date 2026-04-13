import json
from datetime import timedelta

from django.test import Client, TestCase
from django.utils import timezone

from .models import Category, Manufacturer, Product, Stock, User
from .services import create_access_token


class StockApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create(
            username="admin",
            email="admin@example.com",
            password="admin123",
            role=User.ROLE_ADMIN,
        )
        self.normal_user = User.objects.create(
            username="user1",
            email="user1@example.com",
            password="user123",
            role=User.ROLE_USER,
        )
        self.category = Category.objects.create(name="Drinks", description="Cold drinks")
        self.manufacturer = Manufacturer.objects.create(name="Fresh Co")
        self.product = Product.objects.create(
            name="Orange Juice",
            description="Bottle",
            price=10.5,
            made_at_date=timezone.now(),
            expiration_date=timezone.now() + timedelta(days=30),
            manufacturer=self.manufacturer,
            category=self.category,
        )
        self.stock = Stock.objects.create(product=self.product, qty=25, user=self.admin_user)

    def auth_headers(self, user):
        token = create_access_token(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {token}"}

    def test_login_returns_token_and_role(self):
        response = self.client.post(
            "/api/auth/login/",
            data=json.dumps({"username": "admin", "password": "admin123"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["success"])
        self.assertEqual(body["data"]["user"]["role"], User.ROLE_ADMIN)
        self.assertIn("token", body["data"])

    def test_user_cannot_create_category(self):
        response = self.client.post(
            "/api/categories/",
            data=json.dumps({"name": "Snacks", "description": "Light food"}),
            content_type="application/json",
            **self.auth_headers(self.normal_user),
        )

        self.assertEqual(response.status_code, 403)

    def test_product_search_by_name(self):
        response = self.client.get(
            "/api/products/",
            {"name": "Orange"},
            **self.auth_headers(self.normal_user),
        )

        self.assertEqual(response.status_code, 200)
        items = response.json()["data"]["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["name"], "Orange Juice")

    def test_stock_out_reduces_quantity(self):
        response = self.client.post(
            f"/api/stocks/{self.stock.id}/stock-out/",
            data=json.dumps({"qty": 5}),
            content_type="application/json",
            **self.auth_headers(self.admin_user),
        )

        self.assertEqual(response.status_code, 200)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.qty, 20)

    def test_stock_out_more_than_available_fails(self):
        response = self.client.post(
            f"/api/stocks/{self.stock.id}/stock-out/",
            data=json.dumps({"qty": 30}),
            content_type="application/json",
            **self.auth_headers(self.admin_user),
        )

        self.assertEqual(response.status_code, 400)
