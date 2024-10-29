from math import trunc
from django.db import transaction
from django.db import models
from account.models import User

STATUS = (
    'Pending',
    'In Progress',
    'Delivered',
    'Cancelled',
)
from django.db.models import F, Sum

class Order(models.Model):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Ожидание'),
        (IN_PROGRESS, 'В процессе'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменен'),
    ]

    Pickup = 'Pickup'
    Delivery = 'Delivery'

    TYPE_ORDER = [
        (Pickup, 'Самовывоз'),
        (Delivery, 'Доставка')
    ]

    cart = models.ManyToManyField('carts.Cart', related_name='orders', verbose_name='Карзинка')
    user = models.ForeignKey(User, models.CASCADE, related_name='orders', verbose_name='Пользователь')
    address = models.ForeignKey('Address', models.SET_NULL, 'order', verbose_name='Адрес', null=True)
    type_order = models.CharField('Тип заказа', max_length=15, choices=TYPE_ORDER, default=Delivery)
    status = models.CharField(max_length=20, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField('Общяя сумма', max_digits=10, decimal_places=2, default=0.0)
    date_create = models.DateField('Дата добавления', auto_now_add=True)
    date_update = models.DateField('Дата обнавления', auto_now=True)
    promo_code = models.ForeignKey('PromotionalCode', models.SET_NULL, 'promo_code', verbose_name='Промокод', blank=True, null=True)

    def final_prise_is_have_promo_code(self):
        self.promo_code: PromotionalCode
        if self.promo_code and self.promo_code.is_active:
            if self.promo_code.discount_type == 'percentage':
                total_minus_prise = (self.total_price * self.promo_code.subtraction_from_the_amount) / 100
            else:
                total_minus_prise = self.promo_code.subtraction_from_the_amount

            final_prise = self.total_price - total_minus_prise

            return max(final_prise, 0)

        return self.total_price

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.pk} {self.status}'

from django.utils import timezone

class PromotionalCode(models.Model):
    code = models.CharField('Название промокода',max_length=55)
    discount_type = models.CharField(
        max_length=10,
        choices=[
            ('percentage', 'Процент'),
            ('fixed', 'Фиксированная сумма'),
        ],
        verbose_name='Тип скидки'
    )
    subtraction_from_the_amount = models.DecimalField('Сколько вычесть из суммы породукта',max_digits=10, decimal_places=2)
    data_start = models.DateField(verbose_name='Дата началы',default=timezone.now)
    data_end = models.DateField(verbose_name='Дата окончании')
    is_active = models.BooleanField(verbose_name='Активен',)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return  self.code


class Address(models.Model):
    user = models.ForeignKey(User,models.CASCADE,'address',verbose_name="Пользователь")
    street = models.CharField('Улица',max_length=35,null=True)
    house_number = models.CharField('Дом',max_length=10,null=True)
    apartment = models.CharField('Квартира',null=True,blank=True,max_length=10)
    floor = models.PositiveIntegerField('Этаж',null=True,blank=True,)
    intercom = models.CharField('Дамафон',null=True,blank=True,max_length=10)
    create_data = models.DateTimeField('Дата создания',auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.street}, дом {self.house_number}, кв. {self.apartment} ({self.user.get_full_name})"

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'