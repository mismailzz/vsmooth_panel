from django import forms
from django.core import validators
from patching.models import HypervisorInfo, VirtualMachineInfo


class HypervisorInfo_Form(forms.ModelForm):
    class Meta:
        model = HypervisorInfo
        #fields = '__all__'
        fields = ('esxi_hostname', 'esxi_username', 'esxi_password',)
        widgets = {
            'esxi_hostname': forms.TextInput(attrs={'class': 'mycssclass'}),
            'esxi_username': forms.TextInput(attrs={'class': 'mycssclass'}),
            'esxi_password': forms.PasswordInput(attrs={'class': 'mycssclass'}),
        }
        labels = {
            'esxi_hostname': ('ESXi Hostname'),
            'esxi_username': ('ESXi Username'),
            'esxi_password': ('ESXi Password'),
        }

class VirtualMachineInfo_Form(forms.ModelForm):
    class Meta:
        model = VirtualMachineInfo
        fields = ('vm_username', 'vm_password',)
        widgets = {
            'vm_username': forms.TextInput(attrs={'class': 'mycssclass'}),
            'vm_password': forms.PasswordInput(attrs={'class': 'mycssclass'}),
        }
        labels = {
            'vm_username': ('VM Username'),
            'vm_password': ('VM Password'),
        }
