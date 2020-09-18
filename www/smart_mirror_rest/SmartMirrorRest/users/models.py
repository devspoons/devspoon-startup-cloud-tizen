from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=8,verbose_name='name')
    email = models.EmailField(verbose_name='email')
    password = models.CharField(max_length=128, verbose_name='password')
    image = models.ImageField(upload_to="%Y/%m/%d",null = True)
    level = models.CharField(max_length=8, verbose_name='level',
        choices=(
            ('admin', 'admin'),
            ('manager', 'manager'),
            ('user', 'user')
        )) #choices가 어떤 옵션인지 확인할 필요가 있음 (값,어떻게 보여질지), 이경우 default 값이 없으므로 마이그레이션시 default 값을 요구함
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'smart_mirror_user'
        verbose_name = 'smart_mirror_user'
        verbose_name_plural = 'smart_mirror_users'
