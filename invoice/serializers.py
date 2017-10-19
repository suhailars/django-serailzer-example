from rest_framework import serializers

from .models import ( 
    Invoice,
    Transaction,
)


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Transaction
        fields = ("id", "product", "quantity", "price", "line_total")
        read_only_fields = ('line_total',)


class InvoiceSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
    
    class Meta:
        model = Invoice
        fields = ("id", "customer", "date", "total_quantity", "total_amount", "transactions")

    def create(self, validated_data):
        transactions = validated_data.pop('transactions')
        print transactions
        invoice = Invoice.objects.create(**validated_data)
        total_quantity = 0
        total_amount = 0
        for transaction in transactions:
            transaction.pop("id", "")
            price = transaction["price"]
            quantity = transaction["quantity"]
            line_total = price * quantity
            total_quantity += quantity
            total_amount += line_total
            transaction["line_total"] = line_total
            transaction["invoice_id"] = invoice
            Transaction.objects.create(**transaction)

        invoice.total_amount = total_amount
        invoice.total_quantity = total_quantity
        invoice.save()
        return invoice

    def update(self, instance, validated_data):
        transactions = validated_data.pop('transactions')
        old_transactions = instance.transactions.all()
        print "******", type(old_transactions)
        instance.customer = validated_data.get('customer', instance.customer)
        total_quantity = 0
        total_amount = 0
        old_ids = map(lambda x: x.id, old_transactions)
        print old_ids
        for transaction in transactions:
            transaction_id = transaction.pop("id", None)
            price = transaction.get("price")
            quantity = transaction.get("quantity")
            line_total = price * quantity
            transaction["line_total"] = line_total
            if transaction_id and transaction_id in old_ids:
                old_ids.remove(transaction_id)
                Transaction.objects.filter(id=transaction_id).update(**transaction)
            else:
                print "at create ", transaction_id
                Transaction.objects.create(invoice_id=instance, **transaction)
            total_quantity += quantity
            total_amount += line_total
        for id_ in old_ids:
            Transaction.objects.filter(id=id_).delete()
        instance.total_amount = total_amount
        instance.total_quantity = total_quantity
        instance.save()
        return instance


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
