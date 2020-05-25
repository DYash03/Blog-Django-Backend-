from django.shortcuts import render, redirect
from . models import Blog, Contact, URL_update, BlogComment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from content.templatetags import extras
from django.db.models import Max
# Create your views here.


def home(request):
    return render(request, 'content/home.html')


def blog_list(request):
    pol = Blog.objects.all().filter(category='Politics')
    food = Blog.objects.all().filter(category='Food')
    bus = Blog.objects.all().filter(category='Business')
    edu = Blog.objects.all().filter(category='Education')
    MaxView = Blog.objects.aggregate(Max('views_count'))['views_count__max']
    maxvw = Blog.objects.get(views_count=MaxView)
    blog = Blog.objects.all()
    update = URL_update.objects.last()
    blog = {"blog": blog, "edu": edu, "bus": bus,
            "pol": pol, "food": food, "update": update, "maxvw": maxvw}
    return render(request, 'content/blog_list.html', blog)


def blog_read(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.views_count = blog.views_count+1
    blog.save()
    comments = BlogComment.objects.filter(blog=blog, parent=None)
    replies = BlogComment.objects.filter(blog=blog).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    blog = {"blog": blog, "comments": comments,
            "user": request.user, "replyDict": replyDict}
    return render(request, 'content/blog_read.html', blog)


def search(request):
    search = request.GET['search']
    update = URL_update.objects.last()
    if len(search) > 50:
        blog = Blog.objects.none()
    else:
        name = Blog.objects.filter(blog_name__icontains=search)
        description_1 = Blog.objects.filter(
            blog_description_1__icontains=search)
        blog = name.union(description_1)
    blog = {"blog": blog, "search": search, "update": update}
    return render(request, 'content/search.html', blog)


def blog_category(request, category):
    blog = Blog.objects.all().filter(category=category)
    update = URL_update.objects.last()
    blog = {"blog": blog, "update": update}
    return render(request, 'content/category.html', blog)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['fpassword']
        pass2 = request.POST['cpassword']

        if len(username) > 15:
            messages.error(
                request, "Username must be less than 15  characters.")
            return redirect('/')
        if not username.isalnum():
            messages.error(
                request, "Username must only contain letters and numbers.")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('/')
        user = User.objects.create_user(username, email, pass1)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(
            request, 'Your account has been successfully created.')
        return redirect('/')
    else:
        return HttpResponse("404 - Not Found")


def handlelogin(request):
    if request.method == "POST":
        logusername = request.POST['logusername']
        logpassword = request.POST['logpassword']

        user = authenticate(username=logusername, password=logpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In.")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials, Please try again.")
            return redirect('/')
    else:
        return HttpResponse("404 - Not Found")


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out.")
    return redirect('/')


def Contactt(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        mob = request.POST.get('mob', '')
        textarea = request.POST.get('textarea', '')
        if len(name) < 2 or len(mob) < 10 or len(textarea) < 5:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              mob=mob, textarea=textarea)
            contact.save()
            messages.success(request, 'Your response is received.')
    return render(request, "content/Contact.html")


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Blog.objects.get(blg_id=postSno)
        ParentSno = request.POST.get("ParentSno")
        if ParentSno == "":
            comment = BlogComment(comment=comment, user=user, blog=post)
            comment.save()
            messages.success(
                request, "Your comment has been posted successfully.")
        else:
            parent = BlogComment.objects.get(sno=ParentSno)
            comment = BlogComment(
                comment=comment, user=user, blog=post, parent=parent)
            comment.save()
            messages.success(
                request, "Your reply has been posted successfully.")
    return redirect(f'/{post.slug}')
