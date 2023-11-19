# Guide on how to setup and properly link a submodule

1. First we want to create the nested repository on githubs website and give it a name.
2. Then we want to navigate to the folder in the repository where we want to create it and run this command to clone it:
```
git clone --recurse-submodules https://github.com/Anton-Ca/name.git name
```
3. We need to add a symbolic link:
```
git submodule add absolute-path/name
```
4. Update and initialize the submodule:
```
git submodule update --init
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
