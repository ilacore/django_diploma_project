from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Post, Item
from .forms import PostForm
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html', )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 10
    themes = Post.objects.filter(parent__isnull=True).reverse()
    context_object_name = 'themes'

    def get_queryset(self):
        return self.themes

    """def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['themes'] = self.themes
        return context"""


class PostDetailView(generic.DetailView):
    model = Post
    form = PostForm()

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                obj = form.save(commit=False)
                obj.author = request.user
                obj.parent = self.get_object()
                obj.save()
                form = PostForm()
                messages.success(request, "Successfully created!")
                return redirect(self.get_object().get_absolute_url())

    def get_replies(primary, *args, **kwargs):
        replies = Post.objects.filter(parent__pk=primary)
        return replies

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        replies = Post.objects.filter(parent=self.object)
        reply_count = []
        for i in replies:
            reply_count.append(Post.objects.filter(parent=i).count())
        print(reply_count)
        reply_dict = zip(replies, reply_count)
        print(reply_dict)
        context['replies'] = reply_dict
        context['form'] = self.form
        return context


def create_parent_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            form = PostForm()
            messages.success(request, "Successfully created!")
            return redirect('posts')
    return render(request, 'form.html', {'form': form})


def render_lab_live(request):
    obj = Item.objects.all()[:6]
    return render(request, 'lab_live.html', {'obj':obj})
