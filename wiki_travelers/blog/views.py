from typing import Any
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Country, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse

# def home(request):
#     return render(request, 'home.html', {})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        liked = True
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']
    #ordering = ['-id'] #ordering by the newest post created to the latest, by this should be made by date to be more clear
    

def CountryView(request, countries):
    country_name = countries.replace('-', ' ').title().lower()

    country_posts = Post.objects.filter(country__name__iexact=country_name)

    return render(request, 'countries.html', {'countries': country_name, 'country_posts':country_posts})


def CountryListView(request):
    country_menu_list = Country.objects.all()
    return render(request, 'country_list.html', {'country_menu_list': country_menu_list})

    

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["country"] = stuff.country  # Asegúrate de agregar 'country' aquí en el contexto
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    #fields = '__all__'

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    #fields = ['title','title_tag','body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

class AddCountryView(CreateView):
    model = Country
    #form_class = PostForm
    template_name = 'add_country.html'
    fields = '__all__'