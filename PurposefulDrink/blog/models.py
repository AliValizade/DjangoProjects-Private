from django.db import models
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='uposts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True , blank=True)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"pk": self.pk, 'slug': self.slug})
    

class Comment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'pcomments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='uvote')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user} liked {self.post.slug}'
    
class Gallery(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField()

    def __str__(self):
        return self.name