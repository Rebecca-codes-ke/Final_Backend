# from django.core.management.base import BaseCommand
# from django.db import transaction
# from products.models import Product

# PRODUCT_CATALOG = PRODUCT_CATALOG = [
#     {
#         "group": "3500 Puffs",
#         "items": [
#             ("Manhattan mint", 1500),
#             ("Strawberry Cosmo", 1500),
#             ("Blueberry Razz Ice", 1500),
#             ("Grape Ice", 1500),
#             ("Pineapple Ice", 1500),
#             ("Peach Ice", 1500),
#             ("Polar Energy", 1500),
#             ("Spritz", 1500),
#         ],
#     },
#     {
#         "group": "1500 Puffs",
#         "items": [
#             ("Manhattan mint", 800),
#             ("Strawberry ice", 800),
#             ("Blueberry ice", 800),
#             ("Grape ice", 800),
#             ("Watermelon ice", 800),
#         ],
#     },
#     {
#         "group": "Nicotine pouches",
#         "items": [
#             ("GOAT Crystal ice", 700),
#             ("GOAT wild cherry", 700),
#             ("PAZ Berry Frost", 700),
#             ("PAZ Cool mint", 700),
#             ("Red Reaper", 700),
#             ("Hart cold mint", 700),
#         ],
#     },
# ]

# def first_existing_field(model, candidates):
#     fields = {f.name for f in model._meta.fields}
#     for c in candidates:
#         if c in fields:
#             return c
#     return None


# class Command(BaseCommand):
#     help = "Seed initial products into the database (safe to re-run)."

#     @transaction.atomic
#     def handle(self, *args, **options):
#         name_field = first_existing_field(Product, ["name", "title", "product_name"])
#         group_field = first_existing_field(Product, ["group", "category", "type"])
#         price_field = first_existing_field(Product, ["price", "selling_price"])

#         if not name_field:
#             self.stderr.write(
#                 self.style.ERROR(
#                     "Could not find a name field on Product. Expected one of: name, title, product_name."
#                 )
#             )
#             return

#         created = 0
#         updated = 0

#         for g in PRODUCT_CATALOG:
#             group = g["group"]
#             for item in g["items"]:
#                 label = f"{group} — {item}".strip()

#                 lookup = {name_field: label}
#                 defaults = {}

#                 if group_field:
#                     defaults[group_field] = group

#                 # If your Product model requires a price, set a default (0) for now.
#                 if price_field:
#                     defaults[price_field] = 1

#                 obj, was_created = Product.objects.get_or_create(**lookup, defaults=defaults)

#                 if not was_created and defaults:
#                     changed = False
#                     for k, v in defaults.items():
#                         if getattr(obj, k, None) != v:
#                             setattr(obj, k, v)
#                             changed = True
#                     if changed:
#                         obj.save()
#                         updated += 1
#                 else:
#                     created += 1

#         self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))
#         self.stdout.write(self.style.SUCCESS("You can now GET /api/products/ and use IDs in SalesEntry."))


from django.core.management.base import BaseCommand
from products.models import Product

PRODUCT_CATALOG = [
    {
        "group": "3500 Puffs",
        "items": [
            ("Manhattan mint", 1500),
            ("Strawberry Cosmo", 1500),
            ("Blueberry Razz Ice", 1500),
            ("Grape Ice", 1500),
            ("Pineapple Ice", 1500),
            ("Peach Ice", 1500),
            ("Polar Energy", 1500),
            ("Spritz", 1500),
        ],
    },
    {
        "group": "1500 Puffs",
        "items": [
            ("Manhattan mint", 800),
            ("Strawberry ice", 800),
            ("Blueberry ice", 800),
            ("Grape ice", 800),
            ("Watermelon ice", 800),
        ],
    },
    {
        "group": "Nicotine pouches",
        "items": [
            ("GOAT Crystal ice", 700),
            ("GOAT wild cherry", 700),
            ("PAZ Berry Frost", 700),
            ("PAZ Cool mint", 700),
            ("Red Reaper", 700),
            ("Hart cold mint", 700),
        ],
    },
]

CATEGORY_MAP = {
    "3500 Puffs": Product.Category.VAPE_3500,
    "1500 Puffs": Product.Category.VAPE_1500,
    "Nicotine pouches": Product.Category.NIC_POUCH,
}

class Command(BaseCommand):
    help = "Seed products into DB (create or update) with correct prices."

    def handle(self, *args, **options):
        created, updated = 0, 0

        for group in PRODUCT_CATALOG:
            category = CATEGORY_MAP[group["group"]]

            for name, price in group["items"]:
                obj, was_created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        "category": category,
                        "price": price,
                        "is_active": True,
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(self.style.SUCCESS(f"Done ✅ Created: {created}, Updated: {updated}"))
