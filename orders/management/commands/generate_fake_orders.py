from django.core.management.base import BaseCommand
from faker import Faker
from orders.models import Order
from customers.models import Customer
from products.models import Product
import random
from django.utils import timezone

class Command(BaseCommand):
    help = "Fake sipariş verisi oluşturur."

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100, help='Kaç tane sipariş oluşturulacak')

    def handle(self, *args, **kwargs):
        fake = Faker('tr_TR')
        count = kwargs['count']

        customers = list(Customer.objects.filter(is_active=True))
        products = list(Product.objects.all())
        statuses = ['pending', 'completed', 'cancelled']

        if not customers or not products:
            self.stdout.write(self.style.ERROR("Önce müşteri ve ürün verisi girilmelidir."))
            return

        for _ in range(count):
            customer = random.choice(customers)
            product = random.choice(products)
            quantity = random.randint(1, 10)
            price = random.uniform(10, 1000)

            Order.objects.create(
                customer=customer,
                product=product,
                quantity=quantity,
                price=round(price, 2),
                status=random.choice(statuses),
                order_date=fake.date_time_between(start_date='-6M', end_date='now', tzinfo=timezone.get_current_timezone())
            )

        self.stdout.write(self.style.SUCCESS(f"{count} adet sahte sipariş başarıyla oluşturuldu."))
