SWEN 261 - TeamD
HealthNet R2 Beta Release


Overview
=======================================================================
This README.txt file describles how to setup and run the HealhNet system.

It consists of the following sections:
	-Requirements 
	-Server Setup
	-System Setup
	-Contact Us



Requirements
=======================================================================
Here are the minimum requirements to run the server:
	- Python > 2.7
	- Django 1.6
	- Web browser (IE, Firefox, Chrome)

Here are the mimimum requirements to use the system:
	- 1 System Administrator Account (Super Account)
	- 1 Doctor account
	- 1 Nurse account


Server Setup
=======================================================================
From a web browser, enter the following url to download the source code.

	www.se.rit.edu/~s261-11d

Extract the healthnet.zip to your desired directory

From a command line  (CMD or Terminal), 
	1. Change the current directory to the healthnet folder.
		use "cd" on Mac or "dir" on Windows.

	2. Enter the command 

		python manage.py syncdb --all

		One the command is entered, it will prompt you to create a super account

		**Super Account will be used as System Administrator Account
		which allows to register HealthNet Employees such as Doctor, 
		Nurse and Receptionist

	3.	Follow the instructions, create a super account

	4. After create super account. Enter the command 

		python manage.py runserver

		By deafault, the server will be using Port 8080
		If port 8000 has been used, please enter a different port 
		ex: "python manage.py runserver 8080"

System Setup
=======================================================================

	1. Open a web browser, enter the following url

			localhost:8000 or 127.0.0.1:8000

			If you have run the server with a different port, 
			change 8000 to the port you have entered
			from Servet Setup - Step 4

	2. If you successfully connect to the server. 
		Either click "Login" or enter the following url to log-in

		127.0.0.1:8000/account/login/ or localhost:8000/account/login/

	3, Use the System Administrator Account (super account) from
		Server Up - Step 3 to log-in the sytem

	4. After successfully log-in the system
		Either click "Staff Registration" or enter the following url
		to create employee accounts

		127.0.0.1:8000/account/employee-register/  
		or
		localhost:8000/account/employee-register/

	5. Create at least one Doctor account and one Nurse account

		
Contact Us
=======================================================================

TeamD Email:











