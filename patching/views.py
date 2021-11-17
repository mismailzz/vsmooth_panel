from django.shortcuts import render
from . import forms
from patching.forms import HypervisorInfo_Form
import scripts.patching.vmfilter as ansible_vminfo
import scripts.patching.controller as ansible_controller
import json
import os



# Create your views here.
def index(request):
    return render(request, 'patching/index.html')



def connect_select_patch(request):
    hypervisorForm = HypervisorInfo_Form()

    virtual_machine_dict = {}

    if 'connectHypervisorInfo' in request.POST:

        hypervisorForm = HypervisorInfo_Form(request.POST)

        if hypervisorForm.is_valid():
            print("Validation")
            #print("IP: ", hypervisorForm.cleaned_data['esxi_hostname'])
            #print("User: ", hypervisorForm.cleaned_data['esxi_username'])
            #print("Password: ", hypervisorForm.cleaned_data['esxi_password'])
            vhostname = hypervisorForm.cleaned_data['esxi_hostname']
            vusername = hypervisorForm.cleaned_data['esxi_username']
            vpassword = hypervisorForm.cleaned_data['esxi_password']
            ansible_varfile = "playbook/patching/variablefile"
            vmware_hypervisor = ansible_controller.VMwareHypervisorVariables(vhostname, vusername, vpassword, ansible_varfile)
            #vm_resultjson()
            #vm_readJson()
            #form.save(commit=True)
            #return index(request)
            #my_dict_vms = {'virtual_machines': vm_readJson()}
            #return render(request, 'patching/patch_panel.html', context=my_dict_vms)
            virtual_machine_dict = vm_readJson()
        else:
            print('ERROR FORM INVALID')

    elif 'selectVMname' in request.POST:

        if request.POST.get('vm_names'):
            selected_vms = request.POST.get('vm_names');
            print("Virtual Machines Selected:", selected_vms)

    #return render(request,'patching/patch_panel.html',{'form1':hypervisorForm, 'form2': selectVMForm, 'virtual_machines': virtual_machine_dict})
    return render(request,'patching/patch_panel.html',{'form1':hypervisorForm, 'virtual_machines': virtual_machine_dict})


def vm_resultjson():
    vmInfoDict = ansible_vminfo.getVmInfo('temp/patching/ansible_vmresult')
    print(vmInfoDict)
    os.system("> temp/patching/vmresult.json")
    with open('temp/patching/vmresult.json', 'w') as fp:
        json.dump(vmInfoDict, fp)


def vm_readJson():
    openJsonfile = open('temp/patching/vmresult.json')
    loadJson = json.load(openJsonfile)

    print(type(loadJson))
    print(loadJson)
    # Closing file
    openJsonfile.close()
    return loadJson
