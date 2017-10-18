from rest_framework import serializers

from .models import ( 
    Invoice,
    Transaction,
)

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    def get_transactions(self, obj):
        invoice = TransactionSerializer(obj.transactions, many=True)
        return invoice.data
    
    class Meta:
        model = Invoice
        fields = ("id", "customer", "date", "total_quantity", "total_amount", "transactions")

# class StockSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Stock
#         fields = '__all__'

# class ProductSerializer(serializers.ModelSerializer):
#     stock_details = StockSerializer(many=True)
#     #categories = SubCategorySerializer(many=True, allow_null=True)

#     class Meta:
#         model = Product
#         fields = (
#             'sku', 'product_name', 'product_description', 'manufacturer_id',
#             'msrp', 'available_size', 'available_colors', 'discount', 'product_available', 
#             'discount_available', 'picture_url', 'ranking', 'note', 'categories',
#             'stock_details',       
#         )
#         #read_only_fields = ('stock_details',)

#     def create(self, validated_data):
#         categories = validated_data.pop('categories')
#         stock_details = validated_data.pop('stock_details')
#         product = Product.objects.create(**validated_data)
#         #product.save()
#         print("catogories", categories, product.id)
#         for category in categories:
#             print (category)
#             product.categories.add(category) 
#         for stock in stock_details:
#             stock.pop('product')
#             #stock.pop('id')
#             stock = Stock.objects.create(product=product, **stock)
#         return product

#     def update(self, instance, validated_data):
#         categories = validated_data.pop('categories')
#         stock_details = validated_data.pop('stock_details')
#         print("at update ****", categories, stock_details)
#         for item in validated_data:
#             if Product._meta.get_field(item):
#                 setattr(instance, item, validated_data[item])
#         if stock_details:
#             stock = stock_details[0]
#             stock = dict(stock)
#             curr_stock = Stock.objects.get(product=instance)
#             for item in stock:
#                 if Stock._meta.get_field(item):
#                     setattr(curr_stock, item, stock[item])
#         if categories:
#             curr_categories = instance.categories.all()
#             for c in curr_categories:
#                 instance.categories.remove(c)
#             for category in categories:
#                 instance.categories.add(category)
#         return instance


# class SizeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Size
#         fields = '__all__'

# class ColorSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Color
#         fields = '__all__'
