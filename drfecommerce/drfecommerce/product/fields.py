from typing import Any
from django.db import models
from django.core import checks

class OrderField(models.PositiveIntegerField):
    
    description="Ordaring field on a unique field"

    def __init__(self, unique_for_field=None , *args, **kwargs):

        self.unique_for_field=unique_for_field
        super().__init__(*args, **kwargs)
    
    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs)
        ]
    
    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error(
                    """OrderField must define a 'unique_for_field attribute' """
                )
            ]
        elif self.unique_for_field not in [f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error(
                    """OrderField entered doesn't match """
                )
            ]
        return []
    def pre_save(self, model_instance: models.Model,add):
        print("hello")
        print(model_instance)
        
        return super().pre_save(model_instance, add)