from django.db import models


class DocumentType(models.Model):
    code = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Client(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name='clients')
    document_number = models.CharField(max_length=30, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('document_type', 'document_number')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.document_type.code} {self.document_number})"


class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='purchases')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)

    order_number = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra {self.id} - {self.client} - {self.amount}"
