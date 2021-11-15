import json
import os

def getVmInfo(jsonHypFactsFile):

    main_virtual_machine = {} #Primary dictionary
    with open(jsonHypFactsFile) as json_file:
        data = json.load(json_file)
        for p in data['virtual_machines']: #ITERATE OF VIRTUAL MACHINE ATTRIBUTE ONE BY ONE

            temp_vmName = p['guest_name'] #VM NAME USED AS A KEY
            temp_vmOSname = p['guest_fullname']
            main_virtual_machine[temp_vmName] = {'name': temp_vmName, 'os': temp_vmOSname, 'ip':[]}

            temp = p['vm_network'] #ALL MAC ADDRESS OF A SELECTED VM

            for i in temp:
                try:
                    temp_ipaddress = str(p['vm_network'][i]['ipv4'][0])
                    main_virtual_machine[temp_vmName]['ip'].append(temp_ipaddress)

                except:
                    main_virtual_machine[temp_vmName]['ip'].append("No NIC Attached")
            if main_virtual_machine[temp_vmName]['ip'] == []:
                main_virtual_machine[temp_vmName]['ip'].append("Unable to Fetch Info")

    return main_virtual_machine



'''
DESIRIED DICTIONARY BUILD ON JSON IMPORTED
DATA FROM THE ANSIBLE PLAYBOOK
virtual_machines = {
    "VM-1": { name: vm1, os: rhel, ip: [ip1, ip2]}
    "VM-2": { name: vm2, os: rhel, ip: [ip1, ip2]}
}
'''
'''------------------- MAIN
vmInfoDict = getVmInfo('temp/patching/ansible_vmresult')
print(vmInfoDict)
os.system("> temp/patching/vmresult.json")
with open('temp/patching/vmresult.json', 'w') as fp:
    json.dump(vmInfoDict, fp)
'''
