# Guide on how to setup and properly link a submodule

First we want to create the nested repository on githubs website and give it a name.

1. Then we want to navigate to the folder in the repository where we want to create it and run this command to clone it:
```
git clone --recurse-submodules https://github.com/Anton-Ca/name.git name
```
2. We need to add a symbolic link:
```
git submodule add absolute-path/name
```
3. Update and initialize the submodule:
```
git submodule update --init
```
4. The url will likely be wrong so copy the url from the nested repository on github and replace the line that says:
```
url = absolute-path/name
```
With the copied url:
```
url = https://github.com/Anton-Ca/name.git
```
5. You might also need to synchronize it with remote:
```
git submodule sync
```
6. Push to remote:
```
git add .
git commit -m "Submodule added"
git push
```
