from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify

POST_CHOICES = (
    ("HighlySuggested",  "HighlySuggested"),
    ("Normal", "Normal")
)


class Category(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextUploadingField(blank=True, null=True)
    title_tag = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=100, default='coding')
    likes = models.ManyToManyField(
        User, related_name='blog_posts',  blank=True)
    snippet = models.CharField(max_length=255)
    header_image = models.ImageField(
        null=False, blank=False, upload_to="images/")
    isSuggested = models.CharField(
        max_length=30, choices=POST_CHOICES, default=0)

    slug = models.SlugField()

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')

    def get_total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        print("BEFORE SAVE")

        self.title_tag = self.title

        original_slug = slugify(self.title)
        queryset = Post.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug = original_slug
        while(queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Post.objects.all().filter(slug__iexact=slug).count()

        self.slug = slug

        super(Post, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile")
    instagram_url = models.CharField(max_length=300, blank=True)
    twitter_url = models.CharField(max_length=300, blank=True)
    facebook_url = models.CharField(max_length=300, blank=True)
    website_url = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name="comment_users", on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s ' % (self.post.title, self.name)
