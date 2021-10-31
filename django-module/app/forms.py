from django import forms


class AddTicketForm(forms.Form):
    addTicketField = forms.CharField()
