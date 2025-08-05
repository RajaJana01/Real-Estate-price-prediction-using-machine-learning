from django.contrib import admin

# Register your models here.
from .models import RealEstate,AboutUs,User
admin.site.register(RealEstate)
admin.site.register(AboutUs)
admin.site.register(User)
