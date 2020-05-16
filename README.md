# Gomogo

## Developing
```
# Run the UI
nvm use 14.2.0
npm install
npm start

# Run the backend
cd data
pipenv --python 2.7
pipenv install
pipenv shell
python myserver.py
```

Now visit http://localhost:5000 and you should see the site.

Note: The form itself never contributed anything to the decision made at the end, and it seems like whatever the backend was doing is now broken (even the hardcoded postcode stuff), so the map doesn't show a particular point or display any useful information. You could get it working pretty easily if you wanted to.

## Deployment
The server and UI run on ports 5000 and 5001 respectively internally. Here I run them such that ports 10010 and 10011 are bound to these ports on the host.
```
docker build . -t gomogo
docker run -p 10010:5000 -p 10011:5001 -it gomogo --name gomogo
```
