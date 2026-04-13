from django import forms

from .models import Category, Manufacturer, Product, Stock


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=255)


class PaginationForm(forms.Form):
    page = forms.IntegerField(min_value=1, required=False)
    page_size = forms.IntegerField(min_value=1, max_value=100, required=False)
    format = forms.ChoiceField(choices=(("json", "json"), ("table", "table")), required=False)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "description")


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ("name", "description", "address", "license")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "made_at_date",
            "manufacturer",
            "expiration_date",
            "category",
        )

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("Price must be greater than or equal to 0.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        made_at_date = cleaned_data.get("made_at_date")
        expiration_date = cleaned_data.get("expiration_date")
        if made_at_date and expiration_date and expiration_date <= made_at_date:
            raise forms.ValidationError("Expiration date must be after made date.")
        return cleaned_data


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ("product", "qty", "user")

    def clean_qty(self):
        qty = self.cleaned_data["qty"]
        if qty <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return qty


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ("product", "qty", "user")

    def clean_qty(self):
        qty = self.cleaned_data["qty"]
        if qty < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return qty


class StockOutForm(forms.Form):
    qty = forms.IntegerField(min_value=1)
