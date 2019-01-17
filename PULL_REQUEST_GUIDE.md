<p align="center">

<img src=https://camo.githubusercontent.com/98ac5a9047bbf6a063e667a933cc056ea3e627a6/68747470733a2f2f6d617863646e2e69636f6e73382e636f6d2f416e64726f69645f4c2f504e472f3531322f50726f6772616d6d696e672f70756c6c5f726571756573742d3531322e706e67 width=50>
<br>
<h1 align="center">Pull Request Guide</h1>
</p>
<br>

Welcome back! Congrats on getting to this point!
<br>
<br>
We will assume that you've read the Contributing guide and that you are ready to create your first Pull Request, if not, head over to the Contributing guide to get started.

## Quick Check

Before making a Pull request try to make sure you've checked off the quick check boxes:

* Commits start with capitals
* You didn't forget a #TODO inside your code
* You followed the [PEP8](https://www.python.org/dev/peps/pep-0008) or equivalent for the language your programming in styleguide
* Your code passes the unit tests
* Test your code locally (See below)
* Your code contains a new unit test (for your new addition) that passes
* If you've added a new remote import (not builtin) you've included that import in its proper dependencies file (example: dependencies.pip)

## Adding a new file
If your PR requires a new file to be added please make sure it begins with the header

Don't forget to update the filename

```python
###***********************************###
'''
Grade Notifier
File: <filename>.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman, 
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
```

## Testing code locally
To test the website locally navigate into the top-level directory

Then run `bash ./src/tests/run-local.sh`

Once the localhost server is running visit `http://localhost:8000` to view the website.

## Making the Pull Request 

When you make your pull request you must give the pull request a summary. Make sure the summary is informative and explains what is being fixed. If your PR is fixing an issue make sure it label that issue as follows:
<br>

Fixes #< ISSUE_NUMBER >
<br>
Example: Fixes #2
<br>

Additionally, if your PR is a work in progress, make sure the title contains [WIP]. Danger will automatically add the WIP tag in that case. 

If your PR is big, Danger will warn you. It's not a big deal unless the PR could have been smaller. As a rule of thumb 1 PR per feature/issue. If a PR contains changes unrelated to its main focus it will recieve a "Request Changes" status 

Assuming the PR passes our Unit Test and CUNY-Bot doesn't complain about anything to drastic the PR will get merged and you will have made your first (of hopefully many) contributions!

Again, thank you for your help and feel free to reach out with questions!





