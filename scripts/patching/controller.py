#! /usr/bin/python3.6
import argparse
import os
import getpass

def scriptEndExecution():
 os.system("rm -f variablefile")
 os.system("rm -f vmInventory")

def getVmInformation():
 os.system("ansible-playbook playbook/patching/vmInfo.yml -e 'ansible_python_interpreter=/usr/bin/python3'")

def seletectVM():
 readVmInfo = open("vmInventory", "r")
 vmList=":"
 checker = None

 for line in readVmInfo:
  #print(line)
  line = line.strip() ##Remove newline character
  prompt= line + " [ Do you want to patch it (y/n) ] - "
  user_vmSeletection = input(prompt)
  if(user_vmSeletection == "y"):
   vm_name = line.split(":")
   vmList = vmList + ", " + vm_name[1]
   checker = True
  elif(user_vmSeletection == "n"):
   print(line + "- Skipped")
  else:
   print("INVALID OPTION SELECTION")
   exit()

 readVmInfo.close()
 if (checker == True):
  vmList = vmList.replace(':,','')
  vmList = vmList.replace(' ,  ','", "')
  vmList = "[\"" + vmList + "\" ]"
  vmList = vmList.replace(" ","")
  return vmList
 else:
  print("NO VM SELECTED")
  exit()

def vmPatch_variable():
 vmguest_username=""
 vmguest_password=""
 #vmguest_shellcommand="/usr/bin/echo"
 vmguest_topatch=seletectVM()

 vmguest_username = input("Provide the username for VM: ")
 vmguest_password = getpass.getpass(prompt='VMware Esxi Host Guest VM Password? ')
 variablefile = open("variablefile","a")

 vmguest_username_string= " guestvm_username: \"" + vmguest_username + "\"\n"
 vmguest_password_string= " guestvm_password: \"" + vmguest_password + "\"\n"
 #vmguest_shellcommand_string= " vm_shellcommand_echo: \"" + vmguest_shellcommand + "\"\n"
 vmguest_topatch_string= " vm_toPatched: " + vmguest_topatch + "\n"

 variablefile.write(vmguest_username_string)
 variablefile.write(vmguest_password_string)
 #variablefile.write(vmguest_shellcommand_string)
 variablefile.write(vmguest_topatch_string)
 variablefile.close()

def startpatch():
 os.system("ansible-playbook vmpatch.yml  -e 'ansible_python_interpreter=/usr/bin/python3'")

##-----------------------------MAIN FUNCTION----------------------------------

class VMwareHypervisorVariables:


    def __init__(self, esxi_hostname, esxi_username, esxi_password, ansible_variablefile):
        server_hostname = " esxi_hostname: \"" + esxi_hostname + "\"\n"
        server_username = " esxi_username: \"" + esxi_username + "\"\n"
        server_password = " esxi_password: \"" + esxi_password + "\"\n"

        #To empty variable file
        temp_command = ">" + ansible_variablefile
        os.system(temp_command) #empty file

        variablefile = open(ansible_variablefile,"a")
        variablefile.write(server_hostname)
        variablefile.write(server_username)
        variablefile.write(server_password)
        variablefile.close()

        temp_command = ">" + "playbook/patching/ansible.cfg"
        os.system(temp_command)
        inventoryfile = open("playbook/patching/ansible.cfg","a")
        inventoryfile.write("[defaults]\n")
        inventoryfile.write("host_key_checking = False \n")
        inventoryfile.write("inventory = inventory.ini \n")
        inventoryfile.close()

        temp_command = ">" + "playbook/patching/inventory.ini"
        os.system(temp_command)
        inventoryfile = open("playbook/patching/inventory.ini","a")
        inventoryfile.write("[local]\n")
        inventoryfile.write( esxi_hostname + "\n")
        inventoryfile.close()

    def vmInfo(self):
        getVmInformation()
