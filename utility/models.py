from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Table(models.Model):
    server = models.ForeignKey('auth.User', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def checker(self):
        #active = Order.objects.exclude(paid = True)
        active = Order.objects.filter(table = self.id, paid=False)
        if active.count()  == 0:
            return ""
        else:
            return "Active"


class Order(models.Model):
    paid = models.BooleanField(default=False)
    table = models.ForeignKey(Table)
    notes = models.CharField(max_length=255, null=True, blank=True)
    server = models.ForeignKey('auth.User')
    finished = models.BooleanField(default=False)
    food = models.ManyToManyField('utility.Food')

    @property
    def contents(self):
        return self.food.all()

    @property
    def food_tax(self):
        food_items = self.contents
        tax = 0
        for x in food_items:
            tax += (x.price*0.06)
        return round(tax, 3)

    @property
    def total_price(self):
        items = self.contents
        total = 0
        tax = 0
        for x in items:
            total += (x.price + (x.price*0.06))
        return round(total, 2)


    # @property
    # def contents(self):
    #     return [(food_obj.food, food_obj.description) for food_obj in self.food_set.all()]


    def __str__(self):
        return str(self.id)


class Food(models.Model):
    food = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return self.food

STATUS = [
    ('o', 'Owner'),
    ('c', 'Cook'),
    ('s', 'Server')
]

class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    status = models.CharField(max_length=1, choices=STATUS)

    @property
    def is_owner(self):
        return self.status == 'o'

    @property
    def is_server(self):
        return self.status == 's'

    def __str__(self):
        show = str(self.user) + " - " + str(self.status)
        return show
@receiver(post_save, sender=User)
def create(**kwargs):
    created = kwargs['created']
    instance = kwargs['instance']
    if created:
        Profile.objects.create(user=instance)
