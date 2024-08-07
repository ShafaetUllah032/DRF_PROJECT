import factory

from drfecommerce.product.models import Category,Brand,Product

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Category
    
    name=factory.Sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Brand
    
    name=factory.Sequence(lambda n: "Brand_%d" % n)

 
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Product
    
    name=factory.Sequence(lambda n: "Product_%d" % n)
    description="test_description"
    is_digital=True
    brand=factory.SubFactory(BrandFactory)
    category=factory.SubFactory(CategoryFactory)
    is_active=True
     


