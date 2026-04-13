from django.db import DatabaseError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import Category, Manufacturer, Product, Stock
from .permissions import AdminRequiredMixin, AuthenticatedMixin
from .serializers import (
    CategoryForm,
    LoginForm,
    ManufacturerForm,
    ProductForm,
    StockCreateForm,
    StockOutForm,
    StockUpdateForm,
)
from .services import authenticate_credentials, create_access_token, filter_products, filter_stocks
from .utils import (
    error_response,
    maybe_table_response,
    paginate_queryset,
    parse_json_body,
    success_response,
    validation_error_response,
)


def category_to_dict(category: Category):
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "created_at": category.created_at.isoformat(),
    }


def manufacturer_to_dict(manufacturer: Manufacturer):
    return {
        "id": manufacturer.id,
        "name": manufacturer.name,
        "description": manufacturer.description,
        "address": manufacturer.address,
        "license": manufacturer.license,
    }


def product_to_dict(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "made_at_date": product.made_at_date.isoformat(),
        "expiration_date": product.expiration_date.isoformat(),
        "created_at": product.created_at.isoformat(),
        "manufacturer": {
            "id": product.manufacturer_id,
            "name": product.manufacturer.name,
        },
        "category": {
            "id": product.category_id,
            "name": product.category.name,
        },
    }


def stock_to_dict(stock: Stock):
    return {
        "id": stock.id,
        "qty": stock.qty,
        "created_date": stock.created_date.isoformat(),
        "product": {
            "id": stock.product_id,
            "name": stock.product.name,
            "category": stock.product.category.name,
            "manufacturer": stock.product.manufacturer.name,
        },
        "user": {
            "id": stock.user_id,
            "username": stock.user.username,
            "role": stock.user.role,
        },
    }


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = LoginForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        user = authenticate_credentials(
            form.cleaned_data["username"],
            form.cleaned_data["password"],
        )
        if user is None:
            return error_response("Invalid username or password.", status=401)

        token = create_access_token(user)
        return success_response(
            {
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "email": user.email,
                },
            },
            message="Login successful.",
        )


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCollectionView(AuthenticatedMixin):
    def get(self, request):
        queryset = Category.objects.order_by("id")
        try:
            page_obj, page_info = paginate_queryset(queryset, request)
        except ValueError as exc:
            return error_response("Invalid pagination parameters.", details=str(exc))
        rows = [category_to_dict(category) for category in page_obj.object_list]
        table_response = maybe_table_response(request, rows)
        if table_response:
            return table_response
        return success_response({"items": rows, "pagination": page_info})

    def post(self, request):
        if self.user.role != self.user.ROLE_ADMIN:
            return error_response("Admin access is required.", status=403)

        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = CategoryForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        try:
            category = form.save()
        except DatabaseError as exc:
            return error_response("Failed to create category.", status=500, details=str(exc))

        return success_response(category_to_dict(category), status=201, message="Category created.")


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(AdminRequiredMixin):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response("Category not found.", status=404)
        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = CategoryForm(payload, instance=category)
        if not form.is_valid():
            return validation_error_response(form)

        category = form.save()
        return success_response(category_to_dict(category), message="Category updated.")

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return error_response("Category not found.", status=404)
        category.delete()
        return success_response(message="Category deleted.")


@method_decorator(csrf_exempt, name="dispatch")
class ManufacturerCollectionView(AuthenticatedMixin):
    def get(self, request):
        queryset = Manufacturer.objects.order_by("id")
        try:
            page_obj, page_info = paginate_queryset(queryset, request)
        except ValueError as exc:
            return error_response("Invalid pagination parameters.", details=str(exc))
        rows = [manufacturer_to_dict(item) for item in page_obj.object_list]
        table_response = maybe_table_response(request, rows)
        if table_response:
            return table_response
        return success_response({"items": rows, "pagination": page_info})

    def post(self, request):
        if self.user.role != self.user.ROLE_ADMIN:
            return error_response("Admin access is required.", status=403)

        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = ManufacturerForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        manufacturer = form.save()
        return success_response(
            manufacturer_to_dict(manufacturer),
            status=201,
            message="Manufacturer created.",
        )


@method_decorator(csrf_exempt, name="dispatch")
class ManufacturerDetailView(AdminRequiredMixin):
    def get_object(self, pk):
        try:
            return Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return None

    def put(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response("Manufacturer not found.", status=404)
        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = ManufacturerForm(payload, instance=manufacturer)
        if not form.is_valid():
            return validation_error_response(form)

        manufacturer = form.save()
        return success_response(manufacturer_to_dict(manufacturer), message="Manufacturer updated.")

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        manufacturer = self.get_object(pk)
        if manufacturer is None:
            return error_response("Manufacturer not found.", status=404)
        manufacturer.delete()
        return success_response(message="Manufacturer deleted.")


@method_decorator(csrf_exempt, name="dispatch")
class ProductCollectionView(AuthenticatedMixin):
    def get(self, request):
        queryset = Product.objects.select_related("category", "manufacturer")
        queryset = filter_products(queryset, request.GET)
        try:
            page_obj, page_info = paginate_queryset(queryset, request)
        except ValueError as exc:
            return error_response("Invalid pagination parameters.", details=str(exc))
        rows = [product_to_dict(item) for item in page_obj.object_list]
        table_response = maybe_table_response(request, rows)
        if table_response:
            return table_response
        return success_response({"items": rows, "pagination": page_info})

    def post(self, request):
        if self.user.role != self.user.ROLE_ADMIN:
            return error_response("Admin access is required.", status=403)

        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = ProductForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        product = form.save()
        product = Product.objects.select_related("category", "manufacturer").get(pk=product.pk)
        return success_response(product_to_dict(product), status=201, message="Product created.")


@method_decorator(csrf_exempt, name="dispatch")
class ProductDetailView(AdminRequiredMixin):
    def get_object(self, pk):
        try:
            return Product.objects.select_related("category", "manufacturer").get(pk=pk)
        except Product.DoesNotExist:
            return None

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return error_response("Product not found.", status=404)
        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = ProductForm(payload, instance=product)
        if not form.is_valid():
            return validation_error_response(form)

        product = form.save()
        product = Product.objects.select_related("category", "manufacturer").get(pk=product.pk)
        return success_response(product_to_dict(product), message="Product updated.")

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return error_response("Product not found.", status=404)
        product.delete()
        return success_response(message="Product deleted.")


@method_decorator(csrf_exempt, name="dispatch")
class StockCollectionView(AuthenticatedMixin):
    def get(self, request):
        queryset = Stock.objects.select_related(
            "product",
            "product__category",
            "product__manufacturer",
            "user",
        )
        queryset = filter_stocks(queryset, request.GET)
        try:
            page_obj, page_info = paginate_queryset(queryset, request)
        except ValueError as exc:
            return error_response("Invalid pagination parameters.", details=str(exc))
        rows = [stock_to_dict(item) for item in page_obj.object_list]
        table_response = maybe_table_response(request, rows)
        if table_response:
            return table_response
        return success_response({"items": rows, "pagination": page_info})

    def post(self, request):
        if self.user.role != self.user.ROLE_ADMIN:
            return error_response("Admin access is required.", status=403)

        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = StockCreateForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        stock = form.save()
        stock = Stock.objects.select_related(
            "product",
            "product__category",
            "product__manufacturer",
            "user",
        ).get(pk=stock.pk)
        return success_response(stock_to_dict(stock), status=201, message="Stock added.")


@method_decorator(csrf_exempt, name="dispatch")
class StockDetailView(AdminRequiredMixin):
    def get_object(self, pk):
        try:
            return Stock.objects.select_related(
                "product",
                "product__category",
                "product__manufacturer",
                "user",
            ).get(pk=pk)
        except Stock.DoesNotExist:
            return None

    def put(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return error_response("Stock record not found.", status=404)
        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = StockUpdateForm(payload, instance=stock)
        if not form.is_valid():
            return validation_error_response(form)

        stock = form.save()
        stock = self.get_object(stock.pk)
        return success_response(stock_to_dict(stock), message="Stock updated.")

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        stock = self.get_object(pk)
        if stock is None:
            return error_response("Stock record not found.", status=404)
        stock.delete()
        return success_response(message="Stock deleted.")


@method_decorator(csrf_exempt, name="dispatch")
class StockOutView(AdminRequiredMixin):
    def post(self, request, pk):
        try:
            stock = Stock.objects.select_related(
                "product",
                "product__category",
                "product__manufacturer",
                "user",
            ).get(pk=pk)
        except Stock.DoesNotExist:
            return error_response("Stock record not found.", status=404)

        try:
            payload = parse_json_body(request)
        except ValueError as exc:
            return error_response(str(exc))

        form = StockOutForm(payload)
        if not form.is_valid():
            return validation_error_response(form)

        qty = form.cleaned_data["qty"]
        if qty > stock.qty:
            return error_response("Stock out quantity exceeds available stock.")

        stock.qty -= qty
        stock.save(update_fields=["qty"])
        stock = Stock.objects.select_related(
            "product",
            "product__category",
            "product__manufacturer",
            "user",
        ).get(pk=stock.pk)
        return success_response(stock_to_dict(stock), message="Stock removed.")
