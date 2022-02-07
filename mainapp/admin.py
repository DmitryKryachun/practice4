from django.contrib import admin
from .models import *

admin.site.site_header = "Налаштування системи моніторингу бункерів з зерном"


# Register your models here.

admin.site.register(Transaction)
admin.site.register(Bunker)
admin.site.register(Grain)