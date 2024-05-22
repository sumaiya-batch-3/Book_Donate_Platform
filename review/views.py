from django.shortcuts import render,redirect
from django.views import View
from .models import  PlatformComment
from .forms import PlatformCommentForm
# Create your views here.

class PlatformCommentView(View):
    template_name='platform_comments.html'

    def get(self,request,*args,**kwargs):
        comments=PlatformComment.objects.all()
        form=PlatformCommentForm()
        return render(request,self.template_name,{'comments':comments,'form':form})
    
    def post(self,request,*args,**kwargs):
        form=PlatformCommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user=request.user
            new_comment.save()
        return redirect('platform_comments')
        