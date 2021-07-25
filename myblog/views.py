
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForms, EditForms, AddCommentForms
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core import serializers
from collections import defaultdict
import random
from django.db.utils import OperationalError

# Create your views here.


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-date']
    # ordering = ['-id']

    def get_context_data(self, *args, **kwargs):

        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        post_items = Post.objects.all().order_by('-date')
        p = Paginator(post_items, 6)

        page_num = self.request.GET.get('page', 1)

        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        # Get the most posted 3 categories
        cat_dict = {}
        for each in cat_menu:
            cat_dict[each.name] = Post.objects.filter(category=each).count()
        sort_orders = sorted(
            cat_dict.items(), key=lambda x: x[1], reverse=True)[0:6]
        a = []
        for each in sort_orders:
            a.append(str([each[0]]))

        most_posted_cats = []
        for each in a:
            most_posted_cats.append(each[2:len(each)-2])

        latest_posts = post_items[0:5]

        # suggested post actions

        suggested_posts = Post.objects.filter(isSuggested="HighlySuggested")

        if len(suggested_posts) > 3:
            output_suggested_post = random.sample(list(suggested_posts), 4)

        else:

            output_suggested_post = random.sample(
                list(post_items), 4 - len(suggested_posts))

            output_suggested_post = list(
                output_suggested_post) + list(suggested_posts)

        # most liked posts

        most_liked_posts = []
        for each in post_items:

            obj = {"slug": each.slug,
                   "title": each.title,
                   "total_likes": each.get_total_likes(),
                   "author": each.author.first_name + " " + each.author.last_name,
                   "category": each.category,
                   }
            most_liked_posts.append(obj)

        most_liked_posts.sort(
            key=lambda x: x["total_likes"], reverse=True)

        context["latest_posts"] = latest_posts
        context["post_items"] = page
        context["most_posted_cats"] = most_posted_cats
        context["suggested_posts"] = output_suggested_post
        context["most_liked_posts"] = most_liked_posts

        return context


class DetailsView(DetailView):
    model = Post
    template_name = 'details.html'

    def get_context_data(self, *args, **kwargs):

        cat_menu = Category.objects.all()
        context = super(DetailsView, self).get_context_data(*args, **kwargs)
        current_post = get_object_or_404(Post, slug=self.kwargs['slug'])
        total_likes = current_post.get_total_likes()
        total_comment = Comment.objects.filter(post=current_post).count()

        comments = Comment.objects.filter(post=current_post).order_by('-id')
        paginator = Paginator(comments, 5)
        page_num = self.request.GET.get('page', 1)
        com_obj = paginator.get_page(page_num)

        liked = False
        if current_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["commentform"] = AddCommentForms()
        context["total_comment"] = total_comment
        context["first_comments"] = com_obj
        return context

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        form = AddCommentForms(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post
            obj.author = self.request.user
            obj.save()

            return redirect(reverse('article-detail', args=[slug]))
            # return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class AddPostView(CreateView):
    model = Post
    form_class = PostForms
    template_name = 'addPost.html'
    # fields = '__all__'
    # fields=('title', 'body')


class EditPostView(UpdateView):
    model = Post
    form_class = EditForms
    template_name = 'editPost.html'
    # fields = ['title', 'title_tag', 'body']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'deletePost.html'
    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    model = Category
    template_name = 'addCategory.html'
    fields = '__all__'
    # fields=('title', 'body')


def CategoryView(request, cats):
    category_posts = Post.objects.filter(
        category=(cats.replace('-', ' ')).title())

    return render(request, 'categories.html', {'cats': cats.replace('-', ' ').title(), 'category_posts': category_posts})


def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'categoryList.html', {'cat_menu_list': cat_menu_list})


def LikeView(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    print(request)
    print(post.id)
    print(request)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    current_post = get_object_or_404(Post, id=post.id)
    total_likes = current_post.get_total_likes()
    context = {
        "total_likes": total_likes,
        "liked": liked,
        "post": current_post
    }
    if request.is_ajax():
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})


def load_more(request):

    offset = int(request.POST['offset'])
    current_post_id = request.POST['post_id']
    current_post = get_object_or_404(Post, id=current_post_id)

    limit = 5
    comments = Comment.objects.filter(
        post=current_post).order_by('-id')[offset:offset + limit]

    totalData = Comment.objects.filter(post=current_post).count()

    data = {}
    comments_json = serializers.serialize('json', comments)
    first_name_list = []
    last_name_list = []
    for each in comments:
        first_name_list.append(each.user.first_name)
        last_name_list.append(each.user.last_name)

    return JsonResponse(data={
                        'comments': comments_json,
                        'totalResult': totalData,
                        'first_name_list': first_name_list,
                        'last_name_list': last_name_list

                        })


def suggested_post_view(request):

    posts = Post.objects.all().order_by('-date').filter(author=request.user)

    return render(request, 'suggested-posts.html', {'posts': posts})


def change_suggestion_view(request):

    user_posts = Post.objects.all().order_by(
        '-date').filter(author=request.user, isSuggested="HighlySuggested")

    post = get_object_or_404(Post, id=request.POST.get('id'))
    print(post)
    status = post.isSuggested
    if status == "Normal" and user_posts.count() < 2:  # allow only two posts
        post.isSuggested = "HighlySuggested"
        print("a")
        post.save()
    else:
        post.isSuggested = "Normal"
        print("b")
        post.save()

    print(post.isSuggested)
    context = {
        "status": post.isSuggested,
        "item": post
    }

    if request.is_ajax():
        html = render_to_string(
            'suggestion-change-section.html', context, request=request)

        return JsonResponse({'form': html})


def delete_comment(request, id):
    print("in delete comment")
    print(id)
    comment = get_object_or_404(Comment, id=id)

    post = get_object_or_404(Post, comments=comment)
    comment.delete()
    return HttpResponseRedirect(reverse('article-detail', args=[str(post.id)]))
