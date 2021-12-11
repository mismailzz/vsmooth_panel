# vSmooth

Problem Statement:

	• Execute linux commands patch on running Linux Virtual Machines over VMware Hypervisor  
	• Create the log files of running commands on each Virtual Machines for diagnoses purpose 
  
Input:

	• VMware Hypervisor login credentials 
	• Select running virtual machines on which patch has been executed 
	• Write the patch on the text area or input a file contain commands
	• Get the name of VM for which you want to see the logs

Output: 

	• Fetch the Ansible logs console on the Web
	• Status of the executed commands on each host in logs file

Constraints:

	• Credentials for Virtual Machines should be same
	• The commands will be executed with the user having sudo privileges but its not being tested as we are doing with root privileges 
	
Flexibility:

	• Running the patch on virtual machines parallelly but how we would show the output of patch on the VMs

Best practices: 

	• All things should be dynamic in nature
	• Check the python cache files
	• Remove all the credentials files and logs file - using the reset button {other solutions highly recommended}

Progress:

	• CLI version for the VMs on the hypervisor has been created 
	• Djnago base template has been setup and tested against the output files of the cli version of it
	• Multiple branches has been setup on GIT sync with GITHUB
	• VM patch panel has been setup and tested 
	• Ansible console has been setup by using nodejs written frontail application - nodjs has also been setup on it
	• Get the vms logs file panel
	• Created  the docker environment of the application with network
	• Rebuild the application in docker environment 
	• Make the configuration consistent by making the Dockerfile and tested it along by building the image
	• Dockerhub setup for the images
	• Moving towards the docker compose
