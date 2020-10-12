from datetime import date

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)


# -------------------------------------------------------------
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline


# -------------------------------------------------------------
class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)


# -------------------------------------------------------------

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    test_int = models.IntegerField(null=True)


class Place2(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    test_int = models.IntegerField(null=True)


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)


class Supplier(Place):
    # 상속을 이용해 ForeignKey 또는 ManyToMany를 설정할 경우 반드시 related_name을 설정하라
    # 상속은 부모와 자식관계를 OneToOne으로 설정함(migrations에서 확인 가능)
    cusomters = models.ManyToManyField(Place2, related_name='provider')
    supplier_name = models.CharField(max_length=50)


# ------------------------------------------------------------
class RoleChoices(models.TextChoices):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    NORMAL = 'Normal'


class GenderChoices(models.TextChoices):
    UNKNOWN = 'Unknown'
    MALE = 'Male'
    FEMALE = 'Female'


class Profile(models.Model):
    gender = models.CharField(max_length=7, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN)
    favorite = models.CharField(max_length=100, null=True, blank=True)


class Accounts(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField(default=1)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class NormalUser(Accounts):
    role = models.CharField(max_length=6, default=RoleChoices.NORMAL, editable=False)

    def is_normal(self):
        return self.role == self.role.NORMAL


class StaffUser(Accounts):
    role = models.CharField(max_length=6, default=RoleChoices.STAFF, editable=False)

    def is_staff(self):
        return self.role == self.role.STAFF


class CommonInfo(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Person1(models.Model):
    location = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Student(CommonInfo):
    home_group = models.CharField(max_length=10)
