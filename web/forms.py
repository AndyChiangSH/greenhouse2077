from django import forms
from django.utils import timezone

class TimeRangeForm(forms.Form):
    # start_time = forms.DateTimeField(label="Start time", initial=timezone.now)
    # end_time = forms.DateTimeField(label="End time", initial=timezone.now)
    start_time = forms.DateTimeField(label="Start time", input_formats="%Y-%m-%d %H:%M", initial=timezone.now().strftime("%Y-%m-%d"), widget=forms.TextInput(attrs={'type':'date'}))
    end_time = forms.DateTimeField(label="End time", input_formats="%Y-%m-%d %H:%M", initial=timezone.now().strftime("%Y-%m-%d"), widget=forms.TextInput(attrs={'type':'date'}))