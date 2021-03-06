from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from . import models
import uuid
import json

# Create your views here.

#def index(request):
#    return render(request, 'mmw/index.html', {})


class IndexView(TemplateView):
    template_name = "mmw/index.html"


class LoginView(TemplateView):
    template_name = "mmw/whoiam.html"

    def get(self, request):
        if request.user and request.user.username:
            return super(LoginView, self).get(request)
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        print("you already upload details")
        print("username" + request.POST["name"])
        print("email" + request.POST["email"])
        name = request.POST["name"]
        email = request.POST['email']
        instance = models.UserInfo.objects.filter(email=email).first()
        if email == '' or name == '':
            return render(request, "mmw/index.html", {"emailusernamenone": True})
        if instance:
            if instance.name == name:
                print("correct username and email")
                user = instance.user
            else:
                print("wrong username")
                return render(request, "mmw/index.html", {"error": True})
        else:
            return render(request, "mmw/index.html", {"email_no_exist": True})
            print("you are new user")
            user = User.objects.create_user(username=uuid.uuid4().hex[0:10])
            print("user created")
            instance = models.UserInfo.objects.create(user=user, name=name, email=email)
            print("info has been saved id: %d" %instance.id)
        instance2 = models.WhoIAm.objects.filter(user=user).first()
        login(request, user)
        return render(request, "mmw/whoiam.html", {"whoiam": instance2, "userinfo": instance})


class RegisterView(TemplateView):
    template_name = "mmw/index.html"

    def post(self, request):
        print("you uploaded username and email")
        print("username" + request.POST["name"])
        print("email" + request.POST["email"])
        name = request.POST["name"]
        email = request.POST["email"]
        if email == '' or name == "":
            return render(request, "mmw/index.html", {"emailnone": True})
        instance = models.UserInfo.objects.filter(email=email).first()
        if instance:
            print("this email has been registered")
            return render(request, "mmw/index.html", {"registered": True})
        else:
            print("allow to use this email")
            user = User.objects.create_user(username=uuid.uuid4().hex[0:10])
            print("user created")
            instance = models.UserInfo.objects.create(user=user, name=name, email=email)
            print("information has been saved id: %d" %instance.id)
            return render(request, "mmw/index.html", {"success": True})


class UserInfoView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/userinfo.html"
    login_url = "/"


class WhoIAmView(LoginRequiredMixin, TemplateView):
    login_url = "/"
    template_name = "mmw/whoiam.html"

    def get(self, request):
        whoiam, created = models.WhoIAm.objects.get_or_create(user=request.user)
        print(whoiam.text1)
        return render(request, "mmw/whoiam.html", {"whoiam": whoiam})

    def post(self, request):
        print("you upload the info")
        text1 = request.POST["text1"]
        text2 = request.POST["text2"]
        text3 = request.POST["text3"]
        text4 = request.POST["text4"]
        print(text1)
        instance = models.WhoIAm.objects.filter(user=request.user).first()
        if instance is not None:
            #record the whoiam info
            whoiamhistory = models.WhoIAmHistory.objects.create(user=request.user)
            whoiamhistory.text1 = instance.text1
            whoiamhistory.text2 = instance.text2
            whoiamhistory.text3 = instance.text3
            whoiamhistory.text4 = instance.text4
            whoiamhistory.save()

            instance.text1 = text1
            instance.text2 = text2
            instance.text3 = text3
            instance.text4 = text4
            instance.save()

            instance2 = models.Communication.objects.filter(user=request.user).first()
            return HttpResponseRedirect('/MMW/communication/')
            # return render(request, "mmw/communication.html", {"communication": instance2})
        else:
            whoiam = models.WhoIAm.objects.create(user=request.user, text1=text1, text2=text2, text3=text3, text4=text4)
            whoiam.save()
            instance2 = models.Communication.objects.filter(user=request.user).first()
            return HttpResponseRedirect('/MMW/communication/')
            # return render(request, "mmw/communication.html", {"communication": instance2})


class ImportanceView(LoginRequiredMixin, TemplateView):
    login_url = "/"
    template_name = "mmw/importance.html"

    def get(self, request):
        importance, created = models.Importance.objects.get_or_create(user=request.user)
        print(importance.my_family)
        return render(request, "mmw/importance.html", {"importance": importance})

    def post(self, request):
        print("your already upload your information")
        text1 = request.POST["my-family"]
        text2 = request.POST["work-school"]
        text3 = request.POST["very-close-top"]
        text4 = request.POST["very-close-bottom"]
        text5 = request.POST["very-close-left"]
        text6 = request.POST["very-close-right"]
        text7 = request.POST["friends"]
        text8 = request.POST["home-supporters"]
        print(text1)
        instance = models.Importance.objects.filter(user=request.user).first()
        if instance is not None:
            instance.my_family = text1
            instance.work_school = text2
            instance.very_close_top = text3
            instance.very_close_bottom = text4
            instance.very_close_left = text5
            instance.very_close_right = text6
            instance.friends = text7
            instance.home_supporters = text8
            instance.save()
            return HttpResponseRedirect("/MMW/myhome/")
        else:
            whoiam = models.WhoIAm.objects.create(user=request.user, text1=text1, text2=text2, text3=text3, text4=text4, text5=text5, text6=text6, text7=text7, text8=text8)
            whoiam.save()
            return HttpResponseRedirect("/MMW/myhome/")


class communication(LoginRequiredMixin, TemplateView):
    template_name = "mmw/communication.html"
    login_url = "/"

    def get(self, request):
        communication, created = models.Communication.objects.get_or_create(user=request.user)
        return render(request, "mmw/communication.html", {"communication": communication})

    def post(self, request):
        print("you already your information")
        text1 = request.POST["text1"]
        text2 = request.POST["text2"]
        text3 = request.POST["text3"]
        text4 = request.POST["text4"]
        print(text1)
        instance = models.Communication.objects.filter(user=request.user).first()
        if instance is not None:
            # record the communication content history
            communicationhistory = models.CommunicationHistory.objects.create(user=request.user)
            communicationhistory.text1 = instance.text1
            communicationhistory.text2 = instance.text2
            communicationhistory.text3 = instance.text3
            communicationhistory.text4 = instance.text4
            communicationhistory.save()

            instance.text1 = text1
            instance.text2 = text2
            instance.text3 = text3
            instance.text4 = text4
            instance.save()
            return HttpResponseRedirect('/MMW/importance/')
        else:
            communication = models.Communication.objects.create(user=request.user, text1=text1, text2=text2, text3=text3, text4=text4)
            communication.save()
            return HttpResponseRedirect('/MMW/importance/')


class DailyactivityView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/dailyactivity.html"
    login_url = '/'

    def get(self, request):
        instance, created = models.Activity.objects.get_or_create(user=request.user)
        context = {}
        context = json.loads(instance.data)
        context['do'] = instance.do
        context['havenotdo'] = instance.havenotdo
        return render(request, 'mmw/dailyactivity.html', context)

    def post(self, request):
        data = json.loads(request.body.decode('utf8'))
        instance, created = models.Activity.objects.get_or_create(user=request.user)
        instance.data = json.dumps(data, indent=4)
        instance.do = data['do']
        instance.havenotdo = data['havenotdo']
        instance.save()
        return HttpResponse("save successfully")


class FellingView(TemplateView):
    template_name = "mmw/whoiam.html"


class LogoutView(TemplateView):
    template_name = "mmw/index.html"

    def get(self, request):
        logout(request)
        return render(request, "mmw/index.html", {"logout": True})


class MyHomeView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/myhome.html"
    login_url = '/'

    def get(self, request):
        myhome, created = models.MyHome.objects.get_or_create(user=request.user)
        return render(request, "mmw/myhome.html", {"myhome": myhome})

    def post(self, request):
        text1 = request.POST["text1"]
        text2 = request.POST["text2"]
        text3 = request.POST["text3"]
        text4 = request.POST["text4"]
        text5 = request.POST["text5"]
        instance = models.MyHome.objects.filter(user=request.user).first()
        if instance is not None:
            instance.text1 = text1
            instance.text2 = text2
            instance.text3 = text3
            instance.text4 = text4
            instance.text5 = text5
            instance.save()
            return HttpResponseRedirect('/MMW/dailyactivity/')
        else:
            myhome = models.MyHome.objects.create(user=request.user, text1=text1, text2=text2, text3=text3, text4=text4, text5=text5)
            myhome.save()
            return HttpResponseRedirect('/MMW/dailyactivity/')


class ShortTermView(LoginRequiredMixin, TemplateView):
    template_name = 'mmw/short_term_dream.html'
    login_url = "/"

    def get(self, request):
        instance, created = models.Short_term.objects.get_or_create(user=request.user)
        return render(request, "mmw/short_term_dream.html", {"instance": instance})


    def post(self, request):
        text = request.POST['text']
        instance = models.Short_term.objects.filter(user=request.user).first()
        if instance is not None:
            instance.text = text
            instance.save()
            return HttpResponseRedirect('/MMW/long_term/')
        else:
            short_term = models.Short_term.objects.create(user=request.user, text=text)
            short_term.save()
            return HttpResponseRedirect('/MMW/long_term/')


class LongTermView(LoginRequiredMixin, TemplateView):
    template_name = 'mmw/long_term_dream.html'
    login_url = "/"

    def get(self, request):
        instance, created = models.Long_term.objects.get_or_create(user=request.user)
        return render(request, "mmw/long_term_dream.html", {"instance": instance})

    def post(self, request):
        text = request.POST['text']
        instance = models.Long_term.objects.filter(user=request.user).first()
        if instance is not None:
            instance.text = text
            instance.save()
            return HttpResponseRedirect('/MMW/bucket_list/')
        else:
            long_term = models.Long_term.objects.create(user=request.user, text=text)
            long_term.save()
            return HttpResponseRedirect('/MMW/bucket_list/')


class BucketListView(LoginRequiredMixin, TemplateView):
    template_name = 'mmw/bucket_list.html'
    login_url = "/"

    def get(self, request):
        instance, created = models.Bulk_list.objects.get_or_create(user=request.user)
        return render(request, "mmw/bucket_list.html", {"instance": instance})

    def post(self, request):
        text = request.POST['text']
        instance = models.Bulk_list.objects.filter(user=request.user).first()
        if instance is not None:
            instance.text = text
            instance.save()
            return HttpResponseRedirect('/MMW/congratulations/')
        else:
            long_term = models.Bulk_list.objects.create(user=request.user, text=text)
            long_term.save()
            return HttpResponseRedirect('/MMW/congratulations/')


class CongratulationsView(LoginRequiredMixin, TemplateView):
    template_name = 'mmw/congratulations.html'
    login_url = "/"


class ActivityView(TemplateView):
    template_name = "mmw/activity.html"

    def get(self, request):
        instance = models.Activity.objects.filter(user=request.user).first()
        activity = json.loads(instance.data)
        data = {'instance': instance, 'activity': activity}
        return render(request, "mmw/activity.html", data)

    def post(self, request):
        data = json.loads(request.body.decode('utf8'))
        activity_obj, created = models.Activity.objects.get_or_create(user=request.user)
        activity_obj.data = json.dumps(data, indent=4)
        activity_obj.save()
        return HttpResponse("save successfully")


class MyDailyActivityView(TemplateView):
    template_name = "mmw/mydailyactivity.html"


class SupportsView(TemplateView):
    template_name = "mmw/supports.html"


class WeeklySupportView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/weeklysupport.html"
    login_url = '/'

    def get(self, request):
        print('weeklysupport')
        instance = models.WeeklySupport.objects.filter(user=request.user).first()
        data = []
        if instance is not None:
            data = json.loads(instance.text)
        print(data)
        return render(request, self.template_name, {'data': data})

    def post(self, request):
        print("上传weeklysupport")
        data = json.loads(request.body.decode('utf8'))
        instance, created = models.WeeklySupport.objects.get_or_create(user=request.user)
        print(data)
        instance.text = json.dumps(data, indent=4)
        instance.save()
        return HttpResponse("save successfully")


class BaseView(TemplateView):
    template_name = "base.html"


class ExtendView(TemplateView):
    template_name = "mmw/activity.html"


class HealthView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/health.html"
    login_url = '/'

    def get(self, request):
        instance = models.Health.objects.filter(user=request.user).first()
        data = []
        if instance is not None:
            data = json.loads(instance.text)
        print(data)
        return render(request, self.template_name, {'data': data})

    def post(self, request):
        data = json.loads(request.body.decode('utf8'))
        instance, created = models.Health.objects.get_or_create(user=request.user)
        instance.text = json.dumps(data, indent=4)
        instance.save()
        return HttpResponse("save successfully")


class ProgramView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/program.html"
    login_url = '/'

    def get(self, request):
        instance = models.Program.objects.filter(user=request.user).first()
        data = {'instance': instance}
        if instance is not None:
            data['textareas'] = json.loads(instance.data)
            data['textareas']['program_add'] = data['textareas']['program'][2:]
            data['textareas']['who_add'] = data['textareas']['who'][2:]
            data['textareas']['purpose_add'] = data['textareas']['purpose'][2:]
            data['textareas']['often_add'] = data['textareas']['often'][2:]
        return render(request, "mmw/program.html", data)

    def post(self, request):
        data = json.loads(request.body.decode('utf8'))
        prgoram_obj, created = models.Program.objects.get_or_create(user=request.user)
        prgoram_obj.data = json.dumps(data, indent=4)
        prgoram_obj.save()
        return HttpResponse("save successfully")


class EquipmentView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/equipment.html"
    login_url = '/'

    def get(self, request):
        instance = models.Equipment.objects.filter(user=request.user).first()
        data = {'instance': instance}
        if instance is not None:
            data['textareas'] = json.loads(instance.data)
            data['textareas']['program_add'] = data['textareas']['program'][2:]
            data['textareas']['who_add'] = data['textareas']['who'][2:]
            data['textareas']['purpose_add'] = data['textareas']['purpose'][2:]
            data['textareas']['often_add'] = data['textareas']['often'][2:]
        return render(request, "mmw/equipment.html", data)
    def post(self, request):
        data = json.loads(request.body.decode('utf8'))
        equipment_obj, created = models.Equipment.objects.get_or_create(user=request.user)
        equipment_obj.data = json.dumps(data, indent=4)
        equipment_obj.save()
        return HttpResponse("save successfully")


class MyDreamView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/mydream.html"
    login_url = '/'


class HowIWishView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/wish.html"
    login_url = '/'

    def get(self, request):
        context = {}
        instance = models.Wish.objects.filter(user=request.user).first()
        if instance:
            context = {'data': json.loads(instance.data)}
        return render(request, 'mmw/wish.html', context)

    def post(self, request):
        print("用户上传了他的数据")
        instance, created = models.Wish.objects.get_or_create(user=request.user)
        instance.data = request.body.decode('utf8')
        instance.save()
        return HttpResponse("发送成功")


class UserManualView(LoginRequiredMixin, TemplateView):
    template_name = "mmw/usermanual.html"
    login_url = '/'
