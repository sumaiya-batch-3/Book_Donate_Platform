from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class GiftBook(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='books/media/uploads',blank=True,null=True)
    buying_price=models.PositiveIntegerField(default=0)
    buyer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title
    

class RedeemBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(GiftBook,on_delete=models.CASCADE)

    def __str__(self):
        return f"Buy this: {self.book.title}"

    
