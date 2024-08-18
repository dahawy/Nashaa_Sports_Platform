from django import forms

class ReplyForm(forms.Form):
    subject = forms.CharField(
        max_length=128,
        label='العنوان',  # Custom label
        widget=forms.TextInput(attrs={
            'class': 'form-input block w-full px-4 py-3 mb-3 border border-gray-300 rounded-lg'
        })
    )
    message = forms.CharField(
        label='الرسالة',  # Custom label
        widget=forms.Textarea(attrs={
            'class': 'form-textarea block w-full px-4 py-3 mb-3 border border-gray-300 rounded-lg',
            'rows': 5
        })
    )