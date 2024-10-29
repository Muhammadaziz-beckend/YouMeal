from django.db.models.signals import post_save
from django.dispatch import receiver

from carts.models import Cart
from orders.models import Order


@receiver(post_save, sender=Order)
def update_total_price(sender, instance, created, **kwargs):
    if created:
        carts = Cart.objects.filter(user=instance.user,is_see_user=True)

        total_price = 0

        if carts:
            for i in carts:
                total_price += i.final_tootle_prise
                i.is_see_user = False
                i.save()

        instance.cart.set(list(carts))  # Устанавливаем объединённые корзин

        instance.total_price = total_price
        instance.total_price = instance.final_prise_is_have_promo_code()  # Передаем total_price в функцию
        instance.save()

    if created and instance.total_price == 0.00:
        instance.delete()