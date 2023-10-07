from django.shortcuts import render
from django.views.generic.edit import FormView
from useraccess.models import SelectedPackages
import collections
from useraccess.models import Packages
from .forms import MessageForm
from .bulksms2 import process_sms
from useraccess.models import CustomUser
from django.views.generic.base import TemplateView
# Create your views here.

class AdminDashboardView(FormView):
    template_name = "admindash.html"
    form_class = MessageForm
    success_url = '/admindash/'

    def get(self, request):
        form = self.form_class()
        bundle_id = SelectedPackages.objects.values("bundle_id")
        bundle_id_dict_list = [items for items in bundle_id]
        bundle_id_list = [items["bundle_id"] for items in bundle_id_dict_list]

        bundle_id_and_freq = dict(collections.Counter(bundle_id_list))
        package_freq_list = []

        for keys, values in bundle_id_and_freq.items():
            package = [
                items for items in Packages.objects.filter(
                    id=keys).values("bundle", "bundle_length", "bundle_price")
            ]
            count = values
            bundle_freqs = {"packages": package, "count": count}
            package_freq_list.append(bundle_freqs)

        return render(request, "admindash.html", {
            "bundle_freqs": package_freq_list,
            "form": form
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.data.get("message")
            recipients = get_recipients()
            process_sms(message, recipients)
            return render(request, "admindash.html",
                          {"context": "message sent"})
            return render(request, "admindash.html",
                          {"context": "message not sent"})


def get_recipients():
    # get list of all client numbers in the database
    phonenumbers = CustomUser.objects.all().values("phonenumber")
    phonenumbers = [items['phonenumber'] for items in phonenumbers]
    return clean_phonenumbers(phonenumbers)


def clean_phonenumbers(phonenumbers):
    numbers = []
    for items in phonenumbers:
        number = "+254" + items[1:]
        numbers.append(number)
    return numbers


class OnlineUsersView(TemplateView):
    template_name = "online_users.html"
