from django.db import models


# Create your models here.
class Users(models.Model):
    class Meta:
        db_table = "storage_users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    user_id = models.BigIntegerField(verbose_name='Telegram ID', )
    user_name = models.TextField(verbose_name='Username', null=True, blank=True)
    first_name = models.TextField(verbose_name='Имя', )
    last_name = models.TextField(verbose_name='Фамилия', null=True, blank=True)
    ballance = models.FloatField(verbose_name='Балланс', null=True, blank=True)
    STATUS_FEED_BACK = ((1, 'Заблокирован'), (0, 'Нет блокировки'))
    ban = models.IntegerField(verbose_name='Бан', choices=STATUS_FEED_BACK)
    user_date = models.DateTimeField(verbose_name='Дата регистрации')

    def __str__(self):
        return f'{self.user_id}'


class Prices(models.Model):
    class Meta:
        db_table = "price"
        verbose_name = 'Тарифы'
        verbose_name_plural = 'Тарифы'

    name_standart = models.FloatField(verbose_name='Запрос по фио стандартный', null=True,blank=True)
    name_full = models.FloatField(verbose_name='Запрос по фио расширенный',null=True,blank=True)
    phone = models.FloatField(verbose_name='Запрос по номеру телефона',null=True,blank=True)
    passport = models.FloatField(verbose_name='Запрос по паспорту',null=True,blank=True)
    inn_fl = models.FloatField(verbose_name='Запрос по ИНН физ.лиза',null=True,blank=True)
    email = models.FloatField(verbose_name='Запрос по email',null=True,blank=True)
    snils = models.FloatField(verbose_name='Запрос по СНИЛС',null=True,blank=True)
    avto = models.FloatField(verbose_name='Запрос по номеру авто',null=True,blank=True)
    vin = models.FloatField(verbose_name='Запрос по VIN',null=True,blank=True)
    inn = models.FloatField(verbose_name='Запрос по ИНН',null=True,blank=True)
    scoring = models.FloatField(verbose_name='Скоринг',null=True,blank=True)
    credit = models.FloatField(verbose_name='Кредит',null=True,blank=True)
class Request_data(models.Model):
    class Meta:
        db_table = "request_storage"
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'
    user_id = models.BigIntegerField(verbose_name='Telegram ID', )
    type_request = models.TextField(verbose_name='Тип запроса', null=True,blank=True)
    data = models.TextField(verbose_name='Данные для запроса',null=True,blank=True)
    answer = models.TextField(verbose_name='Ответ',null=True,blank=True)





class Pay_data(models.Model):
    class Meta:
        db_table = "users_manage_pay_data"
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'
    order_id = models.BigIntegerField()
    pay_id = models.BigIntegerField()
    amount = models.FloatField()
    sign = models.TextField()
    us_key = models.TextField( null=True, blank=True)

class Recipient(models.Model):
    class Meta:
        db_table = "recipient"
        verbose_name = 'Пополнения фиат'
        verbose_name_plural = 'Пополнения фиат'
    user_id = models.BigIntegerField(verbose_name='Telegram ID', )
    amount = models.FloatField(verbose_name='Сумма',null=True,blank=True)
    hashmd5 = models.TextField(verbose_name='Хеш проверки',null=True,blank=True)
    status = models.TextField(verbose_name='Статус',)
    create_date = models.DateTimeField(verbose_name='Дата cоздания')


class Wallets(models.Model):
    class Meta:
        db_table = "wallets"
        verbose_name = "👛 Кошелёк"
        verbose_name_plural = "👛 Кошельки"

    user_id = models.BigIntegerField(verbose_name="Telegram ID", primary_key=True)
    address_usdt_trc20 = models.TextField(verbose_name="Адрес USDT TRC20", null=True, blank=True)
    primary_key_usdt_trc20 = models.TextField(verbose_name="Приватный ключ USDT TRC20", null=True, blank=True)
    address_busd = models.TextField(verbose_name="Адрес USDT BEP20", null=True, blank=True)
    primary_key_busd = models.TextField(verbose_name="Приватный ключ USDT BEP20", null=True, blank=True)

    def __str__(self):
        return f"{self.user_id}"