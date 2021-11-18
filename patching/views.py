from django.shortcuts import render
from . import forms
from patching.forms import HypervisorInfo_Form, VirtualMachineInfo_Form
import scripts.patching.vmfilter as ansible_vminfo
import scripts.patching.controller as ansible_controller
import json
import os



# Create your views here.
def index(request):
    return render(request, 'patching/index.html')


def connect_select_patch(request):
    hypervisorForm = HypervisorInfo_Form()
    virtualMachineForm = VirtualMachineInfo_Form()

    vhostname = ""
    vusername = ""
    vpassword = ""
    vm_username = ""
    vm_password = ""
    ansible_playbookPath = "playbook/patching/"

    virtual_machine_dict = {}

    if 'connectHypervisorInfo' in request.POST:

        hypervisorForm = HypervisorInfo_Form(request.POST)

        if hypervisorForm.is_valid():
            print("Validation")
            vhostname = hypervisorForm.cleaned_data['esxi_hostname']
            vusername = hypervisorForm.cleaned_data['esxi_username']
            vpassword = hypervisorForm.cleaned_data['esxi_password']
            vmware_hypervisor = ansible_controller.VMwareHypervisorVariables(vhostname, vusername, vpassword, ansible_playbookPath)
            vmware_hypervisor.vmInfo()
            vm_resultjson()
            #form.save(commit=True)
            #return index(request)
            virtual_machine_dict = vm_readJson()
        else:
            print('ERROR FORM INVALID')

    elif 'selectVMname' in request.POST:

        if request.POST.get('vm_names'):
            selected_vms = request.POST.get('vm_names');
            print("Virtual Machines Selected:", selected_vms)
    elif 'executevmbutton' in request.POST:
        if virtualMachineForm.is_valid():
            vm_username = virtualMachineForm.cleaned_data['vm_username']
            vm_password = virtualMachineForm.cleaned_date['vm_password']
            vmware_hypervisor = ansible_controller.VMwareHypervisorVariables()
            vmware_hypervisor.vmCredentialsInfo(vm_username, vm_password, ansible_playbookPath)


    return render(request,'patching/patch_panel.html',{'form1':hypervisorForm, 'virtual_machines': virtual_machine_dict, 'form2':virtualMachineForm,})


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
