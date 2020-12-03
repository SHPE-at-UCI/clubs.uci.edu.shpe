# SHPE at UCI Member Portal

We will be using Flasks project tutorial found [here](http://flask.palletsprojects.com/en/1.1.x/tutorial/).

## Install & Run

#### 1) Install

###### ALL SYSTEMS
Download the ```.env``` file from slack and place it in the root directory of this cloned repo. Here is the [link](https://shpetechcommittee.slack.com/archives/C011D0TD154/p1586063096000300)

***IMPORTANT:*** When you download the file, rename it to ```.env```. For some reason, when you download the file it will get rid of the period.

Then execute the commands below depending on your system.

You must also have python 3.5 or higher installed on your machine. 


| Windows                         | Linux & Mac:             |
|:------------------------------- | -------------------------|
|```$ install-windows.bat ```     | ```$ ./install-linux```  |

> _⚠️ Windows Note: If you received an error during the installing script, try the following:_
> 1. Delete the ```venv``` folder
> 2. Follow the directions [here](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources-python-3-5-and-newer) to install C++ build tools onto your machine
> 3. Run the install-windows.bat script again


#### 2) Run Web App

On the root directory, run the following commands

| Windows                        | Linux & Mac:             |
|:-------------------------------| -------------------------|
|```$ runapp-windows.bat ```     | ```$ ./runapp```  |


### Contributing

We use a feature branch workflow.

Step 1: Create a new branch

```
git checkout -b <feature_milestone#>
Examples: git checkout -b Login_Feature_1.1
```

Step 2: Update, add, commit, and push changes

```
git status
git add <some-file> or git add .
git commit
```

Step 3: Push feature branch to remote

```
git push -u origin new-feature
Step 4: Create a pull request
```

## Development

Create a pull request(PR) on the master branch.
Once the PR is approved, the owner of the PR merges the pull request into master branch.
In the future we will have continuous deployments.

## Tutorial

Made by Guillermo Hernandez - SHPE Technical Program Manager
[Link](https://www.youtube.com/watch?v=T0Ml5WnQbJY&feature=youtu.be)

## Resources
http://flask.palletsprojects.com/en/1.1.x/tutorial/
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application


## License

[MIT](https://choosealicense.com/licenses/mit/)
