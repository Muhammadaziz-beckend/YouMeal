from datetime import datetime

from django.db import models
from account.models import User

STATUS = (
    'Pending',
    'In Progress',
    'Delivered',
    'Cancelled',
)

class Order(models.Model):
    PENDING = 'Pending'  #
    IN_PROGRESS = 'In Progress'  #
    DELIVERED = 'Delivered'  #
    CANCELLED = 'Cancelled'  #

    STATUS_CHOICES = [
        (PENDING, 'Ожидание'),
        (IN_PROGRESS, 'В процессе'),
        (DELIVERED, 'Доставлен'),
        (CANCELLED, 'Отменен'),
    ]

    product = models.ForeignKey('main.Product',models.CASCADE,related_name='orders',verbose_name='Продукт')
    user = models.ForeignKey(User,models.CASCADE,related_name='orders',verbose_name='Пользователь')
    count = models.PositiveIntegerField('Количество продукта',)
    status = models.CharField(max_length=20,verbose_name='Статус заказа', choices=STATUS_CHOICES,default=PENDING)
    total_price = models.DecimalField('Общяя сумма',max_digits=10, decimal_places=2,default=0.0)
    date_create = models.DateField('Дата добавления',auto_now_add=True)
    date_update = models.DateField('Дата обнавления',auto_now=True)
    promo_code = models.ForeignKey('PromotionalCode',models.CASCADE,'promo_code',verbose_name='Промокод' ,blank=True,null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(
        self,
        *args,
        **kwargs
    ):
        self.total_price = self.product.price * self.count
        self.total_price = self.final_prise_is_have_promo_code()

        return super().save( *args,
        **kwargs)

    def final_prise_is_have_promo_code(self):
        self.promo_code:PromotionalCode
        if self.promo_code and self.promo_code.is_active:
            if self.promo_code.discount_type == 'percentage':
                total_minus_prise = (self.total_price * self.promo_code.subtraction_from_the_amount) / 100
            else:
                total_minus_prise = self.promo_code.subtraction_from_the_amount

            final_prise = self.total_price - total_minus_prise

            return  max(final_prise,0)

        return  self.total_price

    def __str__(self):
        return  f'{self.pk} {self.status}'

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