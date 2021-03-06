# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models

# User = get_user_model()
# User = None

#
# # Create your models here.
# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title
#
#
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     comment = models.CharField(max_length=255)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.post)
#
#
# # -------------------------------------------------------------
# class Person(models.Model):
#     name = models.CharField(max_length=128)
#
#     def __str__(self):  # __unicode__ on Python 2
#         return self.name
#
#
# class Group(models.Model):
#     name = models.CharField(max_length=128)
#     members = models.ManyToManyField(Person, through='Membership')
#
#     def __str__(self):  # __unicode__ on Python 2
#         return self.name
#
#
# class Membership(models.Model):
#     person = models.ForeignKey(Person, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     date_joined = models.DateField()
#     invite_reason = models.CharField(max_length=64)
#
#
# # -------------------------------------------------------------
#
# class Place(models.Model):
#     name = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     test_int = models.IntegerField(null=True)
#
#
# class Place2(models.Model):
#     name = models.CharField(max_length=50)
#     address = models.CharField(max_length=50)
#     test_int = models.IntegerField(null=True)
#
#
# class Restaurant(Place):
#     serves_hot_dogs = models.BooleanField(default=False)
#     serves_pizza = models.BooleanField(default=False)
#
#
# class Supplier(Place):
#     # 상속을 이용해 ForeignKey 또는 ManyToMany를 설정할 경우 반드시 related_name을 설정하라
#     # 상속은 부모와 자식관계를 OneToOne으로 설정함(migrations에서 확인 가능)
#     cusomters = models.ManyToManyField(Place2, related_name='provider')
#     supplier_name = models.CharField(max_length=50)
#
#
# # ------------------------------------------------------------
# class RoleChoices(models.TextChoices):
#     ADMIN = 'Admin'
#     STAFF = 'Staff'
#     NORMAL = 'Normal'
#
#
# class GenderChoices(models.TextChoices):
#     UNKNOWN = 'Unknown'
#     MALE = 'Male'
#     FEMALE = 'Female'
#
#
# class Profile(models.Model):
#     gender = models.CharField(max_length=7, choices=GenderChoices.choices, default=GenderChoices.UNKNOWN)
#     favorite = models.CharField(max_length=100, null=True, blank=True)
#
#
# class Accounts(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     age = models.IntegerField(default=1)
#     address = models.CharField(max_length=255)
#     phone = models.CharField(max_length=14)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
#
#     class Meta:
#         abstract = True
#         ordering = ['-created_at']
#
#
# class NormalUser(Accounts):
#     role = models.CharField(max_length=6, default=RoleChoices.NORMAL, editable=False)
#
#     def is_normal(self):
#         return self.role == self.role.NORMAL
#
#
# class ForeignKeyUser(models.Model):
#     name = models.CharField(max_length=100)
#     is_staff = models.BooleanField(default=False)
#
#
# class StaffUser(Accounts):
#     f_user = models.ForeignKey(ForeignKeyUser, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
#     role = models.CharField(max_length=6, default=RoleChoices.STAFF, editable=False, db_index=True)
#
#     # def is_staff(self):
#     #     return self.role == self.role.STAFF
#
#
# # ----------------------------------------------------------------
#
# class CommonInfo(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     age = models.PositiveIntegerField(default=0)
#
#     class Meta:
#         abstract = True
#
#
# class Person1(models.Model):
#     location = models.CharField(max_length=200)
#
#     class Meta:
#         abstract = True
#         base_manager_name = 'objects'
#
#
# class Student(Person1):
#     home_group = models.CharField(max_length=10)
#
#
# # table space
#
# class TablespaceExample(models.Model):
#     name = models.CharField(max_length=30, db_index=True, db_tablespace="indexes")
#     data = models.CharField(max_length=255, db_index=True)
#     shortcut = models.CharField(max_length=7)
#     edges = models.ManyToManyField(to="self", db_tablespace="indexes")
#
#     class Meta:
#         db_tablespace = "tables"
#         indexes = [models.Index(fields=['shortcut'], db_tablespace='other_indexes')]
#
#
# # django doc - making queries
# from django.db import models
#
#
# class Blog(models.Model):
#     name = models.CharField(max_length=100)
#     tagline = models.TextField()
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#
#     def __str__(self):
#         return self.name
#
#
# class Entry(models.Model):
#     blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
#     headline = models.CharField(max_length=255)
#     body_text = models.TextField()
#     pub_date = models.DateField(blank=True, null=True)
#     mod_date = models.DateField(blank=True, null=True)
#     authors = models.ManyToManyField(Author)
#     number_of_comments = models.IntegerField(blank=True, null=True)
#     number_of_pingbacks = models.IntegerField(blank=True, null=True)
#     rating = models.IntegerField(blank=True, null=True)
#
#     def __str__(self):
#         return self.headline
from django.urls import reverse
from django.utils import timezone

from blog.validators import validate_tasty


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self._default_set(**kwargs)
        self._add_permissions(user)
        return user

    def create_superuser(self, **kwargs):
        user = self._default_set(**kwargs)
        user.is_admin = True
        self._add_permissions(user, is_admin=True)
        return user

    def _default_set(self, **kwargs):
        user = self.model(**kwargs)
        password = kwargs.get('password', None)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def _add_permissions(self, obj, include_default=True, is_admin=False):
        content_type = ContentType.objects.get_for_model(obj.__class__)

        if include_default:  # 자동으로 생성된(add, change, delete, view) permissions 포함
            if is_admin:
                permissions = Permission.objects.all()
            else:
                permissions = Permission.objects.filter(content_type=content_type)

            for permission in permissions:
                obj.user_permissions.add(permission)
        else:  # Meta에 정의된 permissions
            for permission in self.Meta.permissions:
                pm = Permission.objects.get(codename=permission[0], content_type=content_type)
                obj.user_permissions.add(pm)


class ParentUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=15, unique=True)

    # is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # user_permissions = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        abstract = True


class ChildUser(ParentUser):
    class Meta:  # migrate 시점에 auth_permission db에 저장
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]

    # user_permissions = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True,
    #                                      related_name='user_permission')


class TaskModel(models.Model):
    user = models.CharField(max_length=100, default='')

    class Meta:
        permissions = [
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        ]


class TastyTitleAbstractModel(models.Model):
    title = models.CharField(max_length=255, validators=[validate_tasty])

    class Meta:
        abstract = True


class Flavor(TastyTitleAbstractModel):
    slug = models.SlugField()
    scoops_remaining = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("flavors:detail", kwargs={"slug": self.slug})


class IceCreamStore(models.Model):
    title = models.CharField(max_length=100)
    block_address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={'pk': self.pk})


# ---------------------------------------------------------------------------
class VoucherManager(models.Manager):
    def age_breakdown(self):
        age_brackets = []
        now = timezone.now()
        delta = now - relativedelta(years=18)
        count = self.model.objects.filter(birth_date__gt=delta).count()
        age_brackets.append(
            {'title': '0-17', 'count': count}
        )
        count = self.model.objects.filter(birth_date__lte=delta).count()
        age_brackets.append(
            {'title': '18+', 'count': count}
        )
        return age_brackets


class Voucher(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    birth_date = models.DateField(blank=True)
    sent = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)

    objects = VoucherManager()


from django.contrib.auth.models import AbstractUser
from django.db import models

#
# class KarmaUser(AbstractUser):
#     karma = models.PositiveIntegerField(verbose_name='karma', default=0, blank=True)


# settings.py
# AUTH_USER_MODEL = 'profiles.KarmaUser'

# class User(AbstractUser):
#     class Types(models.TextChoices):
#         EATER = "EATER", "Eater"
#         SCOOPER = "SCOOPER", "Scooper"
#         INVENTOR = "INVENTOR", "Inventor"
#
#     base_type = Types.EATER
#     # What type of user are we?
#     type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.EATER)
#
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.type = self.base_type
#         return super().save(*args, **kwargs)


# class InventorManager(models.Manager):
#
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(type=User.Types.INVENTOR)
#
#
# class Inventor(User):
#     objects = InventorManager()
#
#     class Meta:
#         proxy = True
#
#     def invent(self):
#         return "Delicious!"
#
#
# class Inventor(User):
#     inventorprofile = models.OneToOneField(...)
#     objects = InventorManager()
#
#     class Meta:
#         proxy = True
#
#     @property
#     def extra(self):
#         return self.inventorprofile
#
#
# class Scooper(User):
#     scooperprofile = models.OneToOneField(...)
#     objects = ScooperManager()
#
#     class Meta:
#         proxy = True
#
#     @property
#     def extra(self):
#         return self.scooperprofile
#
#
# class Eater(User):
#     eaterprofile = models.OneToOneField(...)
#     objects = EaterManager()
#
#     class Meta:
#         proxy = True
#
#     @property
#     def extra(self):
#         return self.eaterprofile

class MyModel(models.Model):
    title = models.CharField(max_length=100, default='test titel')
    value = models.IntegerField(default=100)

