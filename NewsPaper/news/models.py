from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    author=models.OneToOneField(User, on_delete=models.CASCADE)
    rating=models.IntegerField(default=0)
    users=models.IntegerField(default=0)

    def update_rating(self):
        comment_rating = Comments.objects.filter(user_id=self.users.id).aggregate(models.Sum('rating'))['rating__sum']
        posts_rating = Posts.objects.filter(author_id=self).aggregate(models.Sum('rating'))
        post_id = Posts.objects.filter(author_id=self).values_list('id', flat=True)
        rating_comment_to_posts = Comments.objects.filter(post_id__in=post_id).aggregate(models.Sum('rating'))[
            'rating__sum']
        self.user_rating = (int(posts_rating['rating__sum']) * 3) + int(comment_rating) + int(rating_comment_to_posts)
        self.save()



class Category(models.Model):
    category_name=models.CharField(max_length=255,unique=True)


class Posts(models.Model):
    news='N'
    artickle='A'
    CHOOSE=[(artickle,'статья'),(news,'новость')]
    type=models.CharField(max_length=1,choices=CHOOSE,default=news)
    posts_author=models.ForeignKey(Author, on_delete=models.CASCADE)
    when=models.DateField(auto_now_add=True)
    category_postcat=models.ManyToManyField(Category, through='PostCategory')
    title=models.CharField(max_length=255)
    text_of_posts= models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text_of_posts[0:124]+'...'

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()


class PostCategory(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    categories=models.ForeignKey(Category, on_delete=models.CASCADE)

class Comments(models.Model):
    post_connect=models.ForeignKey(Posts,on_delete=models.CASCADE)
    user_conkat=models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text=models.TextField()
    comment_make_time=models.DateField(auto_now_add=True)
    comment_rating=models.FloatField(default=0.0)

    def like(self):
        self.comment_rating+=1
        self.save()

    def dislike(self):
        self.comment_rating-=1
        self.save()



