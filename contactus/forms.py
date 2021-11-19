from django import forms
from contactus.models import ContactUs


class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'title', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام کامل', 'class': 'form-control', 'max_length': 50}),
            'title': forms.TextInput(attrs={'placeholder': 'موضوع', 'class': 'form-control', 'max_length': 100}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل', 'class': 'form-control', 'max_length': 100}),
            'description': forms.Textarea(attrs={'placeholder': 'متن ...', 'class': 'form-control', 'cols': 80, 'rows': 20})
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise forms.ValidationError('نام نمی تواند بیشتر از 50 کاراکتر باشد.')
        return name

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError('موضوع نمی تواند بیشتر از 100 کاراکتر باشد.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 10:
            raise forms.ValidationError('متن شما نمی تواند کمتر از 10 کاراکتر باشد.')
        return description
