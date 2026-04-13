from django.core import signing
from django.http import HttpRequest

from .models import Product, Stock, User


TOKEN_SALT = "stock-api-auth"
TOKEN_MAX_AGE_SECONDS = 60 * 60 * 24


class InvalidTokenError(Exception):
    pass


def create_access_token(user: User) -> str:
    signer = signing.TimestampSigner(salt=TOKEN_SALT)
    value = f"{user.pk}:{user.role}"
    return signer.sign(value)


def get_authenticated_user(request: HttpRequest):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None

    token = header.removeprefix("Bearer ").strip()
    signer = signing.TimestampSigner(salt=TOKEN_SALT)

    try:
        unsigned_value = signer.unsign(token, max_age=TOKEN_MAX_AGE_SECONDS)
        user_id, role = unsigned_value.split(":", 1)
        user = User.objects.get(pk=user_id, role=role, is_disabled=False)
    except (signing.BadSignature, signing.SignatureExpired, ValueError, User.DoesNotExist) as exc:
        raise InvalidTokenError("Invalid or expired token.") from exc

    return user


def authenticate_credentials(username: str, password: str):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if user.is_disabled or not user.check_password(password):
        return None

    return user


def filter_products(queryset, params):
    product_id = params.get("id")
    name = params.get("name")
    category = params.get("category")

    if product_id:
        queryset = queryset.filter(pk=product_id)
    if name:
        queryset = queryset.filter(name__icontains=name)
    if category:
        queryset = queryset.filter(category__name__icontains=category)

    sort = params.get("sort", "default")
    if sort == "id_asc":
        queryset = queryset.order_by("id")
    elif sort == "price_desc":
        queryset = queryset.order_by("-price", "id")
    elif sort == "manufacturer_asc":
        queryset = queryset.order_by("manufacturer__name", "id")
    else:
        queryset = queryset.order_by("-created_at", "id")

    return queryset


def filter_stocks(queryset, params):
    category = params.get("category")
    manufacturer = params.get("manufacturer")
    product_name = params.get("product_name")

    if category:
        queryset = queryset.filter(product__category__name__icontains=category)
    if manufacturer:
        queryset = queryset.filter(product__manufacturer__name__icontains=manufacturer)
    if product_name:
        queryset = queryset.filter(product__name__icontains=product_name)

    sort = params.get("sort", "stock_id")
    if sort == "category":
        queryset = queryset.order_by("product__category__name", "id")
    elif sort == "manufacturer":
        queryset = queryset.order_by("product__manufacturer__name", "id")
    else:
        queryset = queryset.order_by("id")

    return queryset
