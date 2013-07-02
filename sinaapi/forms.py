from django import forms
from network.models import SNUser

from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple

import datetime

YEARS = [y for y in xrange(2000, int(datetime.datetime.now().year) + 1)]

class ConditionalStatusRequestForm(forms.Form):


    # user = forms.ModelMultipleChoiceField(queryset=SNUser.objects.all(), widget=CheckboxSelectMultiple(),to_field_name='idstr')
    user = forms.ModelMultipleChoiceField(queryset=SNUser.objects.all(),widget=FilteredSelectMultiple("verbose name", is_stacked=False),to_field_name='idstr')

    startDate = forms.DateTimeField(widget=SelectDateWidget(years=YEARS), initial=datetime.datetime.today())
    endDate = forms.DateTimeField(widget=SelectDateWidget(years=YEARS), initial=datetime.datetime.today())

