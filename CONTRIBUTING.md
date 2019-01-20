
<p align="center">

<img src=http://icons.iconarchive.com/icons/icons8/windows-8/512/Files-Add-File-icon.png width=50>
<br>
<h1 align="center">Contributing Guide</h1>
</p>
<br>


## Reporting A Problem

If your looking to report a problem first make sure you have a way of reproducing it. Sometimes a problem seems to occur but really resolves itself once you try it again. 

Onces you're sure a problem exists make sure you have down the steps required to reproduce it. 

Finally, head over to the repositories [issue section](https://github.com/Huddie/Grade-Notifier/issues) and create a new issue. Follow the Bug Report template and someone will respond as soon as possible.

## Making A Contribution

First off, thanks!

### Getting started

**Step 1** is setting up your personal forked version of the repository. To do this click the word "fork" at the top right of the screen

**Step 2** is cloning from your remote repository to your local machine. To do this, follow githubs guide: [How to clone](https://help.github.com/articles/cloning-a-repository/)

**Step 3:** The project is now setup on your machine but you need to install the dependencies. While inside the Grade-Notifier directory execute `bash Depfiles/depinstall.sh`  this should take care of installing all necessary dependencies for you. To check everything worked well try running the Unit Test suite. Again, while in the Grade-Notifier directory execute `python3 src/tests/tests.py`. If everything passes you should be good to go!

**Step 4:** Now its time to find an issue you want to help with. Head over to the [issues section](https://github.com/Huddie/Grade-Notifier/issues) of this repo to find one. If your a beginner we suggest finding one marked with the ["good-first-issue"](https://github.com/Huddie/Grade-Notifier/labels/good%20first%20issue) tag. 

Don't hesitate to reach out for help. Simply comment on the issue and someone will help you out.

**Step 5:** Once you think you've solved the issue and are ready to have your changes incorperated into the master, check out the [Pull Request guide](https://github.com/Huddie/Grade-Notifier/blob/master/PULL_REQUEST_GUIDE.md).

Again, if you have any questions, check out our FAQ [here](https://github.com/Grade-Notifier/GN-Core/blob/master/CONTRIBUTING_FAQ.md), if that does not answer your question feel free to reach out and thanks for your future contributions!

### Commit Rules

Generally try to follow the following format:
 
 - Each minor change should have its own commit attached to it for easy rollback
 - Commit messages should be informative

Our danger file has a few commit rules that will get Cuny-Bot to yell at you. Don't worry if he does, he gets upset by accedent sometimes. 
