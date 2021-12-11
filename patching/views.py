from django.shortcuts import render
from . import forms
from patching.forms import HypervisorInfo_Form, VirtualMachineInfo_Form
import scripts.patching.vmfilter as ansible_vminfo
import scripts.patching.controller as ansible_controller
import json
import os
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'patching/index.html')

def ansible_console_page(request):
    return render(request, 'patching/ansible_console.html')

def ansible_console_run():
    os.system("frontail/bin/frontail temp/patching/ansible_output.log &")

def get_report(request):

    #print(request.POST.get("vlogs"))
    if request.POST.get("vlogs"):
      myfile = "temp/patching/logs/" +  str(request.POST.get("vlogs"))
      f = open(myfile, 'r')
      file_content = f.read()
      f.close()
      return HttpResponse(file_content, content_type="text/plain")

    #Get the information of log files
    onlyfiles = [f for f in os.listdir("temp/patching/logs") if os.path.isfile(os.path.join("temp/patching/logs", f))]
    vm_logs_dict = {'vm_logFiles': onlyfiles}
    vmware_hypervisor = ansible_controller.VMwareHypervisorVariables()
    vmware_hypervisor.fetchVMlogfile()
    return render(request,'patching/vm_logs.html', vm_logs_dict)

def connect_select_patch(request):
    hypervisorForm = HypervisorInfo_Form()
    virtualMachineForm = VirtualMachineInfo_Form()

    ansible_playbookPath = "playbook/patching/"

    virtual_machine_dict = {}

    if 'connectHypervisorInfo' in request.POST:

        hypervisorForm = HypervisorInfo_Form(request.POST)

        if hypervisorForm.is_valid():
            print("Validation")
            vhostname = hypervisorForm.cleaned_data['esxi_hostname']
            vusername = hypervisorForm.cleaned_data['esxi_username']
            vpassword = hypervisorForm.cleaned_data['esxi_password']
            if vhostname != "" and vusername != "" and vpassword != "":
                vmware_hypervisor = ansible_controller.VMwareHypervisorVariables(vhostname, vusername, vpassword, ansible_playbookPath)
                vmware_hypervisor.getvmInfo()
                vm_resultjson()
                #form.save(commit=True)
                #return index(request)
                virtual_machine_dict = vm_readJson()
                ansible_console_run()
        else:
            print('ERROR FORM INVALID')

    elif 'selectVMname' in request.POST:

        if request.POST.get('vm_names'):
            selected_vms = request.POST.get('vm_names');
            print("Virtual Machines Selected:", selected_vms)
            vmware_hypervisor = ansible_controller.VMwareHypervisorVariables()
            vmware_hypervisor.vmSelectedInfo(selected_vms, ansible_playbookPath)

    elif 'executevmbutton' in request.POST:
        virtualMachineForm = VirtualMachineInfo_Form(request.POST)
        vmware_hypervisor = ansible_controller.VMwareHypervisorVariables()

        if virtualMachineForm.is_valid():
            #GET THE CREDENTIONALS INFORMATION OF THE VIRTUAL MACHINES
            vm_username = virtualMachineForm.cleaned_data['vm_username']
            vm_password = virtualMachineForm.cleaned_data['vm_password']
            vmware_hypervisor.vmCredentialsInfo(vm_username, vm_password, ansible_playbookPath)
        #GET THE PATCH COMMANDS INFORMATION FROM THE TEXTAREA AND SAVE TO FILE
        if request.POST.get('vmpatch'):
            vm_patchCommands = request.POST.get('vmpatch')
            print(vm_patchCommands)
            vmware_hypervisor.vm_patchCommands(vm_patchCommands, ansible_playbookPath)
            vmware_hypervisor.vmstartPatch()

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
