import json

from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponse, JsonResponse

from .serializers import PaginationForm


def parse_json_body(request):
    if not request.body:
        return {}

    try:
        return json.loads(request.body)
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def error_response(message, status=400, details=None):
    payload = {"success": False, "message": message}
    if details:
        payload["details"] = details
    return JsonResponse(payload, status=status)


def success_response(data=None, status=200, message="OK"):
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return JsonResponse(payload, status=status)


def validation_error_response(form, status=400):
    return error_response(
        "Validation failed.",
        status=status,
        details=form.errors.get_json_data(),
    )


def paginate_queryset(queryset, request):
    form = PaginationForm(request.GET)
    if not form.is_valid():
        raise ValueError(form.errors.get_json_data())

    page = form.cleaned_data.get("page") or 1
    page_size = form.cleaned_data.get("page_size") or 10

    paginator = Paginator(queryset, page_size)

    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages or 1)

    return page_obj, {
        "page": page_obj.number,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
        "total_items": paginator.count,
    }


def maybe_table_response(request, rows):
    output_format = request.GET.get("format", "json")
    if output_format != "table":
        return None

    if not rows:
        return HttpResponse("No records found.", content_type="text/plain")

    headers = list(rows[0].keys())
    widths = {
        header: max(len(str(header)), max(len(str(row.get(header, ""))) for row in rows))
        for header in headers
    }

    def render_line(values):
        return " | ".join(str(value).ljust(widths[header]) for header, value in zip(headers, values))

    separator = "-+-".join("-" * widths[header] for header in headers)
    lines = [render_line(headers), separator]
    lines.extend(render_line([row.get(header, "") for header in headers]) for row in rows)
    return HttpResponse("\n".join(lines), content_type="text/plain")
