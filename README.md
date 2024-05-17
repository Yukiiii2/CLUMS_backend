# How to Download and run

## Cloning

```
  -git clone https://github.com/Yukiiii2/CLUMS_backend)
```

## Files to download
```
-Miniconda
-Python
```
### Backend (using miniconda
```
  -Create new db named clums then
  Import the clums.sql to phpmyadmin
```

### Setup
```
  -cd backend
  -conda create -n clums python=3.9
  -conda activate clums
  -pip install uvicorn mysql-connector-python python multipart bcrypt
```

### To Run
```
-cd backend
-conda activate clums
-uvicorn main:app --reload
```
### To run in Vscode
```
  ctrl+shift+p then search python select interpreter  
  select clums then new terminal (cmd)
```
```
  -cd backend
  -uvicorn main:app --reload
```
