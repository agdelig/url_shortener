## Overview  
This appliction is used to shorten given url uing the [bit.ly](https://dev.bitly.com/) and [tinyurl.com](https://gist.github.com/MikeRogers0/2907534) API.

## Requirements  
 * Python 3.7
 * (optional) Docker 18.09.1  
 * Bitly account  

## Running the Application  
A Bitly OAuth token is required to run properly. 
One can be required [here](https://bitly.com/a/oauth_apps).  
More information regarding bitly Authentication can be found [here](https://dev.bitly.com/v4_documentation.html).  

 - Make an environment variable to store bitly token.  
    in linux  
    
    run: 
```buildoutcfg
export BITLY_TOKEN=<your_token>
```
### Running through terminal  
Install all requirement needed by running  
```buildoutcfg
pip install -r requirements.txt
```
Run the app by running
```buildoutcfg
python run.py
```

### Running using Docker  
First build the container and tag it appropriately.  
```buildoutcfg
docker build -t <tag_name> .
```
Run the container
```buildoutcfg
docker run -d -e BITLY_TOKEN=$BITLY_TOKEN -p 5000:5000 --name <container_name> <tag_name>
```
## Routes  
### /shorten
####POST
##### Request  
Body:  
```buildoutcfg
{
    "url": "string", 
    "provider": "string"
}
```
 * url is the url requested to be shortened.  
 * provider (optional) can be either "bitly" or "tinyurl"
 
 ##### Responses  
 ##### 200
 ```buildoutcfg
 {
     "url": "string", 
     "link":"string"
 }
 ```
   
 * url requested to be shortened  
 * link returned short url.  
 
 ##### 500
 ```buildoutcfg
 {
     "error": "Server error"
 }
 ```
 When a request to a provider responds with a 5xx an attempt will be made to the second one. 
 If the second request comes back with a 5xx, this response is returned.
 A request to bitly returns with a 403 Forbitten.  
 NOTE:  
    A request to bitly provider returning a 403 Forbidden will result in a 500 response 
    as there seems to be an issue with the OAuth token used.
 
 ##### 400
 ```buildoutcfg
 {
     "error": "Client error"
 }
 ```
 This response is returned when a certain provider is requested and that request 
 returns with a 4xx code.  
 NOTE:  
    A request to bitly provider returning a 403 Forbidden will result in a 500 
    responce as there seems to be an issue with the OAuth token used.  
 
 ## Testing  
 run
 ```buildoutcfg
pytest
```