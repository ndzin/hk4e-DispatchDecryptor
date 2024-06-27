# hk4e-Dispatch Decryptor
A Dispatch Response Decryptor for a <i>certain Anime Game.</i>


## Usage:
<h4 align="left"> Install dependencies: </h4>

```
pip install -r requirements.txt 
```
<h4 align="left"> How to run: </h4>

```
py hk4e-dispatch.py --args
```

Available arguments for now :

```
--baixiao True/False --url "<url>"
```
The result will be saved on a JSON file called based on the Game Version, for example <b>OSRELWin4.7.0.json</b>.

## To Do:
<h4 align="left">

- [ ] Add support for base64 only response. 
- [ ] Add support for dispatchSeed and Region decryption
</h4>