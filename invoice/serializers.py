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
        instance.customer = validated_data.get('customer', instance.customer)
        total_quantity = 0
        total_amount = 0
        old_ids = map(lambda x: x.id, old_transactions)
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
                Transaction.objects.create(invoice_id=instance, **transaction)
            total_quantity += quantity
            total_amount += line_total
        for id_ in old_ids:
            Transaction.objects.filter(id=id_).delete()
        instance.total_amount = total_amount
        instance.total_quantity = total_quantity
        instance.save()
        return instance