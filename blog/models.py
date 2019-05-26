from django.db import models
from users.models import  User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length= 100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length= 100)
    def __str__(self):
        return self.name

class Post(models.Model):
    views = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank = True)
    author = models.ForeignKey(User)
    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(
                extensions=['markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            ]
            )
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)
    def __str__(self):
        return self.title
    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])
    def get_absolute_url(self):
        # reverse 去寻找detail名字的url，根据正则反解URL
        return reverse('blog:detail',kwargs={'pk':self.pk})
    class Meta:
        ordering = ['-created_time']



