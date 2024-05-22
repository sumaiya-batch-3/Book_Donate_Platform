from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    Name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,unique=True,null=True,blank=True)

    def __str__(self):
        return self.Name

class Book(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='books/media/uploads',blank=True,null=True)
    buying_price=models.DecimalField(max_length=100,decimal_places=2,max_digits=12)
    category=models.ManyToManyField(Category)
    buyer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return f"comments by {self.user.username}"



class BuyBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return f"Buy this: {self.book.title}"


class DonatedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} donated {self.book.title} (ID: {self.book.id}) on {self.donation_date}"