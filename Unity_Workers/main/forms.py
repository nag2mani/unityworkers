from django import forms
from .models import WorkerRegistration, WorkerType

# class WorkerRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = WorkerRegistration
#         fields = '__all__'
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#             'photo': forms.ClearableFileInput(),
#             'bank_passbook_pdf': forms.ClearableFileInput(),
#             'aadhar_card_pdf': forms.ClearableFileInput(),
#             'worker_type': forms.CheckboxSelectMultiple(),  # Enables multiple selection for WorkerType
#         }

#     # Optionally, if you want to customize the worker_type field label or query:
#     worker_type = forms.ModelMultipleChoiceField(
#         queryset=WorkerType.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )


from django import forms
from .models import WorkRequest

class WorkRequestForm(forms.ModelForm):
    class Meta:
        model = WorkRequest
        fields = [
            'worker_type', 'full_name', 'full_address', 'landmark',
            'pincode', 'contact_number', 'date_of_work', 
            'number_workers_required', 'work_location_link'
        ]
        widgets = {
            'date_of_work': forms.DateInput(attrs={'type': 'date'}),
            'work_location_link': forms.URLInput(),
        }

from django import forms
from .models import WorkerRegistration

class WorkerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False) # Add password field

    class Meta:
        model = WorkerRegistration
        fields = [
            'full_name', 'username', 'password', 'photo', 'full_address', 
            'gender', 'marital_status', 'worker_type', 'mobile_number',
            # Add other required fields here
        ]

    def save(self, commit=True):
        worker = super().save(commit=False)
        worker.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            worker.save()
            self.save_m2m()  # Save many-to-many relationships
        return worker
