from django.shortcuts import get_object_or_404, render_to_response
from forums.models import *
from MAC_profile.forms import RegistrationForm, PassResetForm, NewPassForm, ProfileForm
from MAC_profile.models import Exec
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.

def view_profile(request, user=None):
    if user:
        user = get_object_or_404(User, pk = user)
        return render_to_response('accounts/profile.html',{'usr':user}, context_instance=RequestContext(request))
    elif request.user.is_authenticated():
        user = request.user
        return render_to_response('accounts/profile.html',{'usr':user}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/accounts/login/?next=%s' % request.path)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.Post, instance=request.user)
        form.save
        messages.add_message(request,messages.SUCCESS,'Profile Successfuly Changed')
        return HttpResponseRedirect('/accounts/profile/')
    else:
        form = ProfileForm(instance=request.user)
        return render_to_response('accounts/profile_edit.html',{'form':form}, context_instance=RequestContext(request))

def logoutview(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'Successfuly Logged Out')
    return HttpResponseRedirect('/')

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.cleaned_data['test'].upper() == "MCGILL":
            password = form.cleaned_data['password']
            if form.cleaned_data['passwordConfirm'] != password:
                return render_to_response('accounts/register.html',{'form':form}, context_instance=RequestContext(request))
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            user = User.objects.create_user(username,email,password)
            user.save()
            user.profile.gender=gender
            user.profile.save()
            messages.add_message(request,messages.SUCCESS,'Registration Complete')
            return HttpResponseRedirect('/accounts/login/')
        else:
            messages.add_message(request,messages.ERROR,'Registration error')
            return render_to_response('accounts/register.html',{'form':form}, context_instance=RequestContext(request))
    else:
        form = RegistrationForm()
        return render_to_response('accounts/register.html',{'form':form}, context_instance=RequestContext(request))

@login_required
def new_pass(request):
    if request.method == 'POST':
        form = NewPassForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['old_password']) and form.cleaned_data['password'] == form.cleaned_data['passwordConfirm']:
                request.user.set_password(form.cleaned_data['password'])
                request.user.save()
                messages.add_message(request,messages.SUCCESS,'Password changed successfuly')
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request,messages.ERROR,'Passwords do not match')
                return render_to_response('accounts/new_pass.html',{'form':form}, context_instance=RequestContext(request))
        else:
            messages.add_message(request,messages.ERROR,'An error was found in the submitted data')
            return render_to_response('accounts/new_pass.html',{'form':form}, context_instance=RequestContext(request))
    else:
        form = NewPassForm()
        return render_to_response('accounts/new_pass.html',{'form':form}, context_instance=RequestContext(request))

def exec_page(request):
    execs = Exec.objects.filter(active=True)
    return render_to_response('about/execs.html',{'execs':execs}, context_instance=RequestContext(request))
