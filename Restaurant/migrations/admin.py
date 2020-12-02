from django.contrib import admin
from django.contrib.auth.models import Group, User
from . import models


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["id", 'business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude',
                    'stars', 'review_count', 'is_open', 'categories']


class AtttributesAdmin(admin.ModelAdmin):
    list_display = ["id", 'BusinessAcceptsCreditCards', 'BikeParking', 'GoodForKids', 'BusinessParking',
                    'ByAppointmentOnly', 'RestaurantsPriceRange2']


class HoursAdmin(admin.ModelAdmin):
    list_display = ["id", 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class NewCovAdmin(admin.ModelAdmin):
    list_display = ["id", "city", "case_rate", "cases", "zipcode"]


class FoodsAdmin(admin.ModelAdmin):
    list_display = ['code', 'creator', 'created_datetime', 'product_name', 'countries', 'energy_100g',
                    'fat_100g']


admin.site.register(models.Restaurant, RestaurantAdmin)
admin.site.register(models.Atttributes, AtttributesAdmin)
admin.site.register(models.Hours, HoursAdmin)
admin.site.register(models.NewCov, NewCovAdmin)
admin.site.register(models.Foods, FoodsAdmin)
