from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import User
import requests
from .baseurl import url as BaseURL
from tags.models import CustomTag
import json
from django.views import View

class Register(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'frontend/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'frontend/login.html',
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')

class HomePageView(TemplateView):
    template_name = "frontend/index.html"
    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView,
                        self).get_context_data(*args, **kwargs)
        response = requests.get(BaseURL+'/api/v1/questions/top-three/')
        context['search_url'] = BaseURL+'api/v1/questions/search-question/?q='
        context['topthree'] = response.json()
        return context

class SearchPageView(TemplateView):
    template_name = "frontend/search.html"
    def get_context_data(self, *args, **kwargs):
        if self.request.GET.get('query'):
            query = self.request.GET.get('query')
        else:
            query = ''
        context = super(SearchPageView,
                        self).get_context_data(*args, **kwargs)
        response = requests.get(BaseURL+'/api/v1/questions/search-question/?q='+query)
        response1 = requests.get(BaseURL+'/api/v1/questions/top-three/')
        context['alltags'] = CustomTag.objects.all()[:10]
        print(response.json())
        context['results'] = response.json()
        context['topthree'] = response1.json()
        context['searched_tag'] = query
        return context

class AddQuestionView(View):
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        context = {}
        context['alltags'] = CustomTag.objects.all()[:10]
        return render(request, "frontend/ask_questions.html", context)
