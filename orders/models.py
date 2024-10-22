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

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(
        self,
        *args,
        **kwargs
    ):
        self.total_price = self.product.price * self.count

        return super().save( *args,
        **kwargs)

    def __str__(self):
        return  f'{self.pk} {self.status}'