#! /usr/bin/python3.6
import argparse
import os
import getpass

def scriptEndExecution():
 os.system("rm -f variablefile")
 os.system("rm -f vmInventory")


##-----------------------------MAIN FUNCTION----------------------------------

class VMwareHypervisorVariables:


    def __init__(self, esxi_hostname=None, esxi_username=None, esxi_password=None, ansible_playbookPath=None):

        """
        OURLOAD CONSTRUCTOR BY DEFAULT VALUES TO OPERATE FOR BOTH SCENERIOS WITH/WITOUT
        ARGUMENTS. BECAUSE WE DON'T WANT TO REINITIALIZE OR CREATE THE VARIABLE FILE
        FOR THE HYPERVISOR IN CASE OF VIRTUAL MACHINE
        """
        if esxi_hostname and esxi_username and esxi_password and ansible_playbookPath:
            """
            THIS IS THE CONSTRUCTOR THAT WILL MAKE/CONFIGURE THE FILES FOR THE HYPERVISOR
            THAT ARE FUNDAMENTAL FOR BUILDING THE CONNECTION
            """
            #ENTER SERVER INFORMATION IF VARIABLE FILE FOR ANSIBLE PLAYBOOK
            server_hostname = " esxi_hostname: \"" + esxi_hostname + "\"\n"
            server_username = " esxi_username: \"" + esxi_username + "\"\n"
            server_password = " esxi_password: \"" + esxi_password + "\"\n"

            #To empty variable file
            variableFilePath = ansible_playbookPath + "hypvariablefile"
            temp_command = ">" + variableFilePath
            os.system(temp_command) #empty file

            variablefile = open(variableFilePath,"a")
            variablefile.write(server_hostname)
            variablefile.write(server_username)
            variablefile.write(server_password)
            variablefile.close()
            #---------------------------------------------------------------
            # READY THE ANSIBLE CONFIGURATION FILE
            ansibe_cfgPath = ansible_playbookPath + "ansible.cfg"
            temp_command = ">" + ansibe_cfgPath
            os.system(temp_command)
            ansible_cfg = open(ansibe_cfgPath,"a")
            ansible_cfg.write("[defaults]\n")
            ansible_cfg.write("host_key_checking = False \n")
            ansible_cfg.write("inventory = inventory.ini \n")
            ansible_cfg.close()
            #---------------------------------------------------------------
            # READY THE ANSIBLE INVENTORY FILE
            ansible_inventoryPath = ansible_playbookPath + "inventory.ini"
            temp_command = ">" + ansible_inventoryPath
            os.system(temp_command)
            inventoryfile = open(ansible_inventoryPath,"a")
            inventoryfile.write("[local]\n")
            inventoryfile.write( esxi_hostname + "\n")
            inventoryfile.close()
            #---------------------------------------------------------------
        else:
            print("Without parameters")

    def vmSelectedInfo(self, vm_toPatched, ansible_playbookPath):
        print("VM select function")
        #ENTER VM INFORMATION TO BE PATCHED IN SEPARATE VMS FILE
        if vm_toPatched != "":
            vmListvariable = '["'+ vm_toPatched.replace(',','","') + '"]'
            vmguest_topatch_string= ' vm_toPatched: ' + vmListvariable + '\n'

            #To empty variable file
            variableFilePath = ansible_playbookPath + "vm_patchvariablefile"
            temp_command = ">" + variableFilePath
            os.system(temp_command) #empty file

            variablefile = open(variableFilePath,"a")
            variablefile.write(vmguest_topatch_string)
            variablefile.close()

        else:
            print("NO VM SELECTED")

    def vmCredentialsInfo(self, vm_username, vm_password, ansible_playbookPath):
        """
        SIMILAR PATTERN WILL BE FOLLOWED AS ABOVE FOR APPENDING INFORMATION
        FOR THE VM BUT IN THIS CASE WE WILL BUILD SEPARATE FILE FROM variable
        OF THE HYPERVISOR BECAUSE WE HAVE TWO SEPARATE PORTION FORMS OF
        HYPERVISOR AND VM, DUE TO WHICH IF THE USER ENTER THE VM CREDENTIONAL
        INFO REPEATEDLY THEN THE APPEND MODE IN THE HYPERVISOR HAVE MANY
        ENTERIES OF VM CREDENTIONALS IN THE VARAIABLE FILE OF HYPERVISOR. IN
        SEPARATE WE CAN CREATE NEW EVERY TIME
        """
        print("VM credential section")
        #ENTER VM INFORMATION IF VARIABLE FILE FOR ANSIBLE PLAYBOOK
        guestvm_username = " guestvm_username: \"" + vm_username + "\"\n"
        guestvm_password = " guestvm_password: \"" + vm_password + "\"\n"

        #To empty variable file
        variableFilePath = ansible_playbookPath + "vmvariablefile"
        temp_command = ">" + variableFilePath
        os.system(temp_command) #empty file

        variablefile = open(variableFilePath,"a")
        variablefile.write(guestvm_username)
        variablefile.write(guestvm_password)
        variablefile.close()

        #GET VM INFORMATION
        getvmInfo()

    def vm_patchCommands(self, patch_commands, ansible_playbookPath):

        print("VM patch commands info")
        cmd_arr_name = "run_commands:\n"
        #To empty variable file

        patchfilePath = ansible_playbookPath + "patchCommand.yml"
        temp_command = ">" + patchfilePath
        os.system(temp_command) #empty file

        patchfile = open(patchfilePath,"a")
        patch_commandlist = patch_commands.split('\n')

        patchfile.write(cmd_arr_name)
        for command in patch_commandlist:
            temp_cmd = command.replace('\r', '')
            patchfile.write(' - "' + temp_cmd + ' 2>&1 | tee -a out.log "\n')
        patchfile.close()

        #START PATCH
        vmstartPatch()

    #ANSIBLE PLAYBOOK EXECUTION COMMANDS FUNCTIOIN
    def getvmInfo(self):
        os.system("> temp/patching/ansible_output.log")
        command_toexe = "ansible-playbook -i playbook/patching/inventory.ini playbook/patching/vmInfo.yml -e 'ansible_python_interpreter=/usr/bin/python3' 2>&1 | tee -a out.log"
        os.system(command_toexe)

    def vmstartPatch(self):
        startpatch()
        os.system("> temp/patching/ansible_output.log")
        command_toexe = "ansible-playbook -i playbook/patching/inventory.ini playbook/patching/vmpatch.yml  -e 'ansible_python_interpreter=/usr/bin/python3' 2>&1 | tee -a out.log"
        os.system(command_toexe)
        os.system(command_toexe)
