from django.db import models
from mptt.models import MPTTModel,TreeForeignKey
from .fields import OrderField



class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)
        



class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    is_active=models.BooleanField(default=False)
    parent=TreeForeignKey("self",on_delete=models.PROTECT,
                          null=True,blank=True
                          )
    
    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name



class Brand(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=255)
    description=models.TextField(blank=True)
    is_digital=models.BooleanField(default=False)
    brand=models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, 
        null=True,blank=True
    )
    is_active=models.BooleanField(default=False)

    objects=ActiveQueryset.as_manager()
    def __str__(self):
        return self.name

    
class ProductLine(models.Model):
    price=models.DecimalField(decimal_places=2, max_digits=4)
    sku=models.CharField(max_length=100)
    stock_qty=models.IntegerField()
    product=models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_line",
    )
    is_active=models.BooleanField(default=False)
    order=OrderField(unique_for_field="product" ,blank=True)

    objects=ActiveQueryset.as_manager()