from django.contrib import admin
from django.apps import apps


class AutoModelAdmin(admin.ModelAdmin):
    """
    Safe default admin that doesn't assume field names.
    Shows up to ~8 fields in list_display and allows basic searching.
    """
    def get_list_display(self, request):
        # Show the first few concrete fields (avoid M2M issues in list_display)
        fields = [f.name for f in self.model._meta.fields]
        return tuple(fields[:8]) if fields else ("id",)

    def get_search_fields(self, request):
        # Allow searching over text-like fields automatically
        text_fields = []
        for f in self.model._meta.fields:
            internal = getattr(f, "get_internal_type", lambda: "")()
            if internal in ("CharField", "TextField", "EmailField", "SlugField", "UUIDField"):
                text_fields.append(f.name)
        return tuple(text_fields[:8])


# Auto-register every model in the "metrics" app
app_config = apps.get_app_config("metrics")

for model in app_config.get_models():
    try:
        admin.site.register(model, AutoModelAdmin)
    except admin.sites.AlreadyRegistered:
        pass

