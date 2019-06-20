# prjScrapper
## Run
Download and extract zip file, put prjScrapper in Desktop

Open command prompt, change directory
```
cd C:\Users\<your user>\Desktop\prjScrapper-master
```
Start included python virtual environment by typing this to your cmd
```
"C:\Users\<your user>\Desktop\prjScrapper-master\pyvenv\Scripts\activate.bat"
```
Change directory by typing this from your current directory which is(C:\Users\<your user>\Desktop\prjScrapper-master)
```
cd pyapi
```
Run server
```
python manage.py runserver
```


## Use
After spin up server user can try to hit the API by typing this in browser
```
localhost:8000/<internet banking user id>/<internet banking password>
```


## About
* This is an API with ability to scrap user internet banking mutation(last 3 months) and account balance
* This API will not scrap other information except user internet banking mutation(last 3 months) and account balance
* Your user id and password passed through API parameter will not stored in any place
* Script will auto logging you out from internet banking after 
