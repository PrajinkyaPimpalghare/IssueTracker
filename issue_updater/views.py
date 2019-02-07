from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from datetime import datetime
from difflib import SequenceMatcher
from .forms import SignUpForm
from .models import ReportPost


JOB_TYPE = ["FULLBUILD","NORMAL","NIGHTLY","OTHER"]
BUILD_TYPE = ["SWC","CPS","PRJ","ADMIN"]
PRIORITY = ["HIGH","MEDIUM","LOW"]
STATUS = ["YELLOW","GREEN","RED"]
HEADINGS = ["BUILD NAME","JOB TYPE","FAILED AT","REPORTED BY","REPORTED TO","PRIORITY","REASON"]
TEAM = ["CI","TOOLING","FDT","OTHER"]
FAILED_AT = ["ARXML","CG","RTE","CMP","CMT","CC","OTHER"]

def contact(request):
    try:
        return render(request, "issue_updater/template/contact.html", {})
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception":error})

def issue_history(request):
    try:
        if request.user.is_authenticated:
            filter = request.GET.get('filter')
            publish_data = ReportPost.objects.all()
            table_data = {}
            if not filter:
                for elements in publish_data:
                    table_data[elements.issue_number] = [[elements.job_type, elements.failed_at,
                                                         elements.reported_by, elements.reported_to+"/"+elements.responsible_team , elements.priority,
                                                         elements.reason[0:30]],elements.build_type]
            else:
                for elements in publish_data:
                    if filter == elements.responsible_team or filter in elements.reported_to or filter in elements.reported_by:
                        table_data[elements.issue_number] = [[elements.job_type, elements.failed_at,
                                                             elements.reported_by,elements.reported_to + "/" + elements.responsible_team,elements.priority,elements.reason[0:30]],elements.build_type]
            return render(request, "issue_updater/template/issue_history.html",
                          {"table_heading": HEADINGS, "table_data": table_data})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def issue_report(request):
    try:
        if request.user.is_authenticated:
           if request.method == 'POST':
                #match,issue_number = search_engine(request.POST.get('REASON'))
                match = False
                issue_number = None
                if not match:
                    post = ReportPost()
                    post.responsible_team = request.POST.get('TEAM')
                    post.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    post.job_type = request.POST.get('JOB TYPE')
                    post.build_type = request.POST.get('BUILD TYPE')
                    post.failed_at = request.POST.get('FAILED AT')
                    post.issue_number = issue_creator(post.job_type + "_" + post.build_type + "_" + post.failed_at)
                    post.status = request.POST.get('STATUS')
                    post.reported_by = request.user.username
                    post.reported_to = request.POST.get('REPORTED TO')
                    post.priority = request.POST.get('PRIORITY')
                    post.final_comment = request.POST.get('FINAL COMMENT')
                    post.reason = request.POST.get('REASON')
                    post.solution = request.POST.get('SOLUTION')
                    post.save()
                    return redirect('/dashboard/')
                else:
                    return render(request, "issue_updater/template/wrong_turn.html", {"exception": "Similar Issue Already Exists With Issue Number {0},Please Search It Again".format(issue_number)})

           else:
                users = User.objects.all()
                return render(request, "issue_updater/template/issue_report.html", {"job_type":JOB_TYPE,"build_type":BUILD_TYPE,"priority":PRIORITY,"status":STATUS,"users":users,"team":TEAM,"failed_at":FAILED_AT})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def dashboard(request):
    try:
        if request.user.is_authenticated:
            publish_data = ReportPost.objects.all()
            table_data = {}
            for index,elements in zip(range(0,10),list(reversed(publish_data))):
                table_data[elements.issue_number]=[[elements.job_type,elements.failed_at,elements.reported_by,elements.reported_to+"/"+elements.responsible_team,elements.priority,elements.reason[0:30]],elements.build_type]
            return render(request, "issue_updater/template/dashboard.html", {"table_heading":HEADINGS,"table_data":table_data})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def index(request):
    try:
        if request.user.is_authenticated:
            return render(request, "issue_updater/template/index.html", {})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def issue_page(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                return redirect('/dashboard/')
            else:
                issue_number = request.GET.get('issue_number')
                users = User.objects.all()
                page_data = get_issue_data(issue_number)
                if page_data:
                    return render(request, "issue_updater/template/issue_page.html",page_data)
                else:
                    return redirect('/dashboard/')
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def issue_update(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                update_issue_data(request,request.GET.get('issue_number'))
                return redirect('/dashboard/')
            else:
                issue_number = request.GET.get('issue_number')
                users = User.objects.all()
                dynamic_data = get_issue_data(issue_number)
                #match, present_number = search_engine(dynamic_data["reason"])
                static_data = {"job_type":JOB_TYPE,"build_type":BUILD_TYPE,"priority":PRIORITY,"status":STATUS,"users":users,"team":TEAM,"failed_at":FAILED_AT}
                return render(request, "issue_updater/template/issue_update.html", {"dynamic_data":dynamic_data,"static_data":static_data})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def issue_search(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                publish_data = ReportPost.objects.all()
                table_data = {}
                job_type = request.POST.get('JOB TYPE')
                build_type = request.POST.get('BUILD TYPE')
                failed_at = request.POST.get('FAILED AT')
                status = request.POST.get('STATUS')
                for elements in publish_data:
                    if job_type in [elements.job_type,"ALL" ]and elements.build_type.strip() == build_type.strip() and failed_at in [elements.failed_at,"ALL" ] and status in [elements.status,"ALL" ]:
                        table_data[elements.issue_number] = [[elements.job_type, elements.failed_at, elements.reported_by,
                                                          elements.reported_to + "/" + elements.responsible_team,
                                                          elements.priority, elements.reason[0:30]],
                                                         elements.build_type]
                return render(request, "issue_updater/template/issue_search.html",
                              {"job_type": JOB_TYPE + ["ALL"], "build_type":BUILD_TYPE, "status": STATUS,"buildname":build_type, "failed_at": FAILED_AT + ["ALL"], "table_heading": HEADINGS,"table_data":table_data}                              )
            if request.method == 'GET':
                return render(request,"issue_updater/template/issue_search.html",{"job_type":JOB_TYPE + ["ALL"],"build_type":BUILD_TYPE,"status":STATUS + [
                    "ALL"],"failed_at":FAILED_AT + ["ALL"],"table_heading":HEADINGS,"buildname":"SWC/CPS/PRJ NAME"})
        else:
            return redirect("/accounts/login/")
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def signup(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'issue_updater/template/registration/signup.html', {'form': form})
    except Exception as error:
        return render(request, "issue_updater/template/wrong_turn.html", {"exception": error})

def custom_exception(request):
    if request.user.is_authenticated:
        return render(request, "issue_updater/template/wrong_turn.html", {})
    else:
        return redirect("/accounts/login/")

def issue_creator(issue):
    publish_data = ReportPost.objects.all()
    number = 0
    table_data = []
    return_issue = issue + str(number)
    for elements in publish_data:
        table_data.append(elements.issue_number)
    while return_issue in table_data:
        return_issue = issue + str(number)
        number += 1
    return return_issue

def get_issue_data(issue_number):
    publish_data = ReportPost.objects.all()
    for elements in publish_data:
        if elements.issue_number == issue_number:
            return {"job_type": elements.job_type, "build_type": elements.build_type, "priority": elements.priority, "status": elements.status,"failed_at":elements.failed_at,
                    "issue_number":issue_number,"reported_by":elements.reported_by,"reported_to":elements.reported_to+"/"+elements.responsible_team,"reason":elements.reason,"final_comment":elements.final_comment,"solution":elements.solution}

def update_issue_data(request,issue_number):
    post = ReportPost.objects.get(issue_number=issue_number)
    post.responsible_team = request.POST.get('TEAM')
    post.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post.job_type = request.POST.get('JOB TYPE')
    post.build_type = request.POST.get('BUILD TYPE')
    post.failed_at = request.POST.get('FAILED AT')
    post.status = request.POST.get('STATUS')
    post.reported_to = request.POST.get('REPORTED TO')
    post.priority = request.POST.get('PRIORITY')
    post.final_comment = request.POST.get('FINAL COMMENT')
    post.reason = request.POST.get('REASON')
    post.solution = request.POST.get('SOLUTION')
    post.save()

def search_engine(string):
    result = (False,"")
    for elements in ReportPost.objects.all():
        ratio = SequenceMatcher(None, elements.reason, string).ratio()
        if ratio >= 0.8:
            result = (True,elements.issue_number)
    return result



