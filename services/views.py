from django.shortcuts import render,redirect
from .models import Url
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
import random,string
def getAlias():
    return "".join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(8)])

def dashboard(request):
    if request.method == "POST":
        URL = request.POST["URL"]
        alias = request.POST.get("alias",None)
        if not alias:
            alias = getAlias()

        try:
            # request.user.url_set(target_url-url)
            Url.objects.create(user=request.user,target_url=URL,alias=alias).save()
            messages.success(request,"shorted seccessfully.")
            return redirect("dashboard")
        except: 
            messages.error(request,"Alias already in used.")
            return render(request,"dashboard.html",{"url":URL,"alias":alias})
        
    site = get_current_site(request)
    return render(request,"dashboard.html",{"domain":site})


def redirect_to_target_page(request,alias):
    obj = Url.objects.get(alias=alias)
    URL = obj.target_url
    return redirect(URL)