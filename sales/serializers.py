

# from decimal import Decimal
# from rest_framework import serializers
# from .models import Sale


# class SaleSerializer(serializers.ModelSerializer):
#     # merchandiser info (read-only; set by backend in perform_create)
#     merchandiser_id = serializers.IntegerField(source="merchandiser.id", read_only=True)
#     merchandiser_name = serializers.CharField(source="merchandiser.username", read_only=True)

#     # store/product display fields
#     store_name = serializers.CharField(source="store.name", read_only=True)
#     store_contact = serializers.CharField(source="store.contact_number", read_only=True)
#     product_name = serializers.CharField(source="product.name", read_only=True)

#     # pricing fields (computed)
#     unit_price = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Sale
#         fields = [
#             "id",
#             "date",

#             # owner (who recorded the sale)
#             "merchandiser_id",
#             "merchandiser_name",

#             # store/product
#             "store", "store_name", "store_contact",
#             "product", "product_name",

#             # sale numbers
#             "quantity",
#             "unit_price",
#             "total_amount",

#             "created_at",
#         ]
#         read_only_fields = [
#             "id",
#             "created_at",
#             "total_amount",
#             "unit_price",
#             "merchandiser_id",
#             "merchandiser_name",
#             "store_name",
#             "store_contact",
#             "product_name",
#         ]

#     def get_unit_price(self, obj):
#         """
#         Pull price from Product model.
#         Supports either `price` or `selling_price`.
#         """
#         p = obj.product
#         return getattr(p, "price", None) or getattr(p, "selling_price", None) or 0

#     def validate(self, attrs):
#         """
#         Compute total_amount = unit_price * quantity
#         """
#         product = attrs.get("product")
#         qty = attrs.get("quantity", 1)

#         if not product:
#             raise serializers.ValidationError({"product": "Product is required."})

#         if not qty or int(qty) < 1:
#             raise serializers.ValidationError({"quantity": "Quantity must be at least 1."})

#         price = getattr(product, "price", None) or getattr(product, "selling_price", None)
#         if price is None:
#             raise serializers.ValidationError({"product": "This product has no price set."})

#         attrs["total_amount"] = Decimal(str(price)) * Decimal(int(qty))
#         return attrs

from decimal import Decimal
from rest_framework import serializers
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    # merchandiser info (read-only; set by backend in perform_create)
    merchandiser_id = serializers.IntegerField(source="merchandiser.id", read_only=True)
    merchandiser_name = serializers.CharField(source="merchandiser.username", read_only=True)

    # store/product display fields
    store_name = serializers.CharField(source="store.name", read_only=True)
    # ✅ remove contact later if you want; keeping it here is fine even if frontend doesn't show it
    store_contact = serializers.CharField(source="store.contact_number", read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)

    # pricing fields (computed)
    unit_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "date",

            "merchandiser_id",
            "merchandiser_name",

            "store", "store_name", "store_contact",
            "product", "product_name",

            "quantity",
            "unit_price",
            "total_amount",

            # ✅ ADD THIS so you can update paid/pending
            "payment_status",

            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "total_amount",
            "unit_price",
            "merchandiser_id",
            "merchandiser_name",
            "store_name",
            "store_contact",
            "product_name",
        ]

    def get_unit_price(self, obj):
        p = obj.product
        return getattr(p, "price", None) or getattr(p, "selling_price", None) or 0

    def validate(self, attrs):
        """
        Compute total_amount = unit_price * quantity

        - On CREATE: require product + quantity
        - On PATCH/UPDATE: only recompute if product or quantity is being changed
        """
        request = self.context.get("request")
        is_partial = bool(request and request.method == "PATCH")

        # Existing instance values (for update)
        instance = getattr(self, "instance", None)

        # If this is a PATCH that doesn't touch product/quantity, skip pricing validation
        if is_partial and instance and "product" not in attrs and "quantity" not in attrs:
            return attrs

        # Determine product + qty from attrs OR fallback to existing instance (update)
        product = attrs.get("product") or (instance.product if instance else None)
        qty = attrs.get("quantity", None)
        if qty is None:
            qty = instance.quantity if instance else 1

        if not product:
            raise serializers.ValidationError({"product": "Product is required."})

        if not qty or int(qty) < 1:
            raise serializers.ValidationError({"quantity": "Quantity must be at least 1."})

        price = getattr(product, "price", None) or getattr(product, "selling_price", None)
        if price is None:
            raise serializers.ValidationError({"product": "This product has no price set."})

        attrs["total_amount"] = Decimal(str(price)) * Decimal(int(qty))
        return attrs
