
from django.shortcuts import render
from django.http import HttpResponse
from scipy.fft import fht
from .models import Post, postComment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, logout
from django.contrib import messages
from django.shortcuts import redirect
from .models import Post
from .forms import ImageForm
# Create your views here.


def home(request):
    data1 = Post.objects.all().order_by('-id')[:6]
    data = Post.objects.all().order_by('-id')[:4]
    data = reversed(Post.objects.filter(pk__in=data))
    view=[]
    
    for postview in Post.objects.all():
        view.append(postview.view)
    view.sort()
    view.reverse()
    popposts=[]
    for pop in view:
        poppost=Post.objects.filter(view=pop).first()
        if poppost not in popposts:
            popposts.append(poppost)
    # print(view)
    # print(popposts)
    
    return render(request, 'index.html', {'data': data, 'posts': popposts})


def post(request):
    data = Post.objects.all()
    data = reversed(Post.objects.filter(pk__in=data))

    return render(request, 'post.html', {'data': data})


def blogpost(request, slug):
    data1 = Post.objects.all().order_by('-id')[:3]
    data = Post.objects.filter(title=slug).first()
    data.view =data.view + 1
    data.save()
    comment = postComment.objects.filter(post=data,parent=None)
    comment = reversed(postComment.objects.filter(pk__in=comment))
    replies = postComment.objects.filter(post=data).exclude(parent=None)
    replyDict={}
    for reply in replies:

        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    
    # print(replyDict)

    maindict= {'slug': data, 'data1': data1, 'comments': comment,'replyDict': replyDict}
    # maindict= replyDict
    return render(request, 'blogpost.html' ,maindict)



def search(request):
    if request.method == 'GET':
        data = Post.objects.all()
        lists = []
        for index, i in enumerate(data):
            data = Post.objects.all()[index].title
            lists.append(data)

        query = request.GET.get('search')
        query = query.lower()
        results = []
        for i in lists:
            if query in i:
                results.append(i)
            if query not in i:
                q = query.split()
                if 2 == len(q):
                    if query in q:
                        results.append(i)
        else:
            results.append('data not found')
    result = []
    for index, i in enumerate(results):
        result.append(Post.objects.filter(title=results[index]).first())
    return render(request, 'search.html', {'data': result})


def login(request):
    if request.method == 'POST':
        loginUserName = request.POST['loginUserName']
        loginPassword = request.POST['loginpassword']
        user = authenticate(username=loginUserName, password=loginPassword)
        if user is not None:
            login_user(request, user)
            messages.success(request, 'succefully logged in')
            return redirect('/')
        else:
            messages.error(request, 'user is not found')
            return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, f'user successfully logout')
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName')
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        Cpassword = request.POST.get('cpassword')
        name=Name.split(' ')
        if UserName.isnumeric():
            messages.error(request, 'please enter a valid username')
            return redirect('signup')
        if Password != Cpassword:
            messages.error(request, 'Password is not match')
            return redirect('signup')
        try:
            myuser = User.objects.create_user(UserName, Email, Password,first_name=name[0],last_name=name[1])
            myuser.first_name = Name
            messages.success(request, f'user {UserName} successfully created')
            user = authenticate(username=UserName, password=Password)
            login_user(request, user)
            return redirect('/')
        except Exception as e:
            messages.error(request, 'user already exists')
            return redirect('signup')
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')


def editor(request):
    # form=ImageForm(request.POST,request.FILES)
    # form.save()
    if request.method == 'POST':
        Name = request.user.first_name + ' ' + request.user.last_name
        user = request.user
        Title = request.POST['title']
        Decs = request.POST['decs']
        image=request.FILES.get('image')
        print(image)
        data = Post(name=Name,user=user ,title=Title, description=Decs,image=image)
        data.save()
        messages.success(request, f'your Post uploaded')
    return render(request, 'editor.html')


def comment(request):
    if request.method == 'POST':
        postcomment = request.POST.get('comment')
        user = request.user
        posttitle = request.POST.get('posttitle')
        post = Post.objects.get(title=posttitle)
        parentm=request.POST.get('parentm')
        parentsno= request.POST.get('parentsno')
        if parentm=="":
            if 2 < len(postcomment):
                comment = postComment(comment=postcomment, user=user, post=post)
                comment.save()
                print('hahah')
            else:
                messages.error(request, f'please enter long comment')
        else:
            parent=postComment.objects.get(sno=parentsno)
            reply = request.POST.get('reply')
            comment=postComment( comment=reply,user=user,post=post,parent=parent)
            comment.save()
    return redirect(f'blogpost/{post.title}')