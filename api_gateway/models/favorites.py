from django.db import models

class Favorite(models.Model):
    account_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100) 

    def __str__(self):
        return f"{self.account_id} - {self.user_id}"
    
    @staticmethod
    def get_favorite_user_uuids(user_id):
        return Favorite.objects.filter(account_id=user_id).values_list('user_id', flat=True)
