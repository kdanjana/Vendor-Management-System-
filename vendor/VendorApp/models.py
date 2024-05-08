from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg
from django.db.models import F
from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, primary_key=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_data = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivered_data is None:
        instance.delivered_data = timezone.now()
        instance.save()

    vendor = instance.vendor
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

    # Update On-Time Delivery Rate
    total_completed_orders = completed_orders.count()
    on_time_deliveries = completed_orders.filter(delivered_data__lte=F('delivery_date')).count()
    on_time_delivery_rate = on_time_deliveries / total_completed_orders if total_completed_orders > 0 else 0
    vendor.on_time_delivery_rate = on_time_delivery_rate

    # Update Quality Rating Average
    quality_rating_avg = completed_orders.exclude(quality_rating__isnull=True).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
    vendor.quality_rating_avg = quality_rating_avg

    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    vendor = instance.vendor

    # Update Average Response Time
    response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).values_list('acknowledgment_date', 'issue_date')
    total_response_times = len(response_times)
    average_response_time = sum((ack_date - issue_date).total_seconds() for ack_date, issue_date in response_times) / total_response_times if total_response_times > 0 else 0
    vendor.average_response_time = average_response_time
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    vendor = instance.vendor

    # Update Fulfillment Rate
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    fulfillment_rate = fulfilled_orders.count() / total_orders if total_orders > 0 else 0
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()