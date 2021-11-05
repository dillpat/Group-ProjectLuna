from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect


""" class ProfileView(TemplateView):
    template_name = 'my_profile.html'

    def get(self, request):
        form = HomeForm()
        users = User.objects.all()
        return render(request, self.template_name, {'form': form})

    def post(self, request) """
