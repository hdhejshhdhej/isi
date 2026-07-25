from django.contrib import admin

from .models import Users, Prices, Request_data, Pay_data, Recipient,Wallets


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', "first_name", 'last_name', "ballance", "user_date")
    search_fields = ('user_id',  'user_name')


@admin.register(Prices)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name_standart', 'name_full', 'phone', 'passport', 'inn_fl', 'email', 'snils', 'avto', 'vin', 'inn', "scoring", "credit")


@admin.register(Request_data)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type_request')
    search_fields = ('user_id', )

@admin.register(Pay_data)
class Pay_dataAdmin(admin.ModelAdmin):
    list_display = ('order_id',)

@admin.register(Recipient)
class PRecipientAdmin(admin.ModelAdmin):
    list_display = ('user_id',"amount","status", "create_date")


@admin.register(Wallets)
class WalletsAdmin(admin.ModelAdmin):
    list_display = ('user_id',"address_usdt_trc20", "address_busd")
    search_fields = ('user_id',"address_usdt_trc20", "address_busd")
