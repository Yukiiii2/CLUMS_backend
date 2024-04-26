# what to install and run the backend
-download miniconda and python
#what commands to create a environment in miniconda

-conda create -n "env_name" pyhton=3.9
-pip install fastapi uvicorn mysql-connector-python
-pip install bcrypt
-pip install python-multipart

# to run the backend you use turn on the xampp and activate the apache and mysql
-uvicorn main:app --reload
