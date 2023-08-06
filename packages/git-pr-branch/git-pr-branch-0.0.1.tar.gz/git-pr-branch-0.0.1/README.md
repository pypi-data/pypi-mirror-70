# GIT PR branch

`git-pr-branch` is a command line tool designed to manage the relationship between branches and
pull-requests.

At the moment it only supports Github, but other backends are possible.

You need to create a personal token in https://github.com/settings/tokens. When you start the
program for the first time, it will ask you for it and store it in a configuration file.

I suggest running `git config alias.pr '!git-pr-branch'` to simplify git integration. You will just
need to type `git pr` to run `git-pr-branch`, options and arguments will be forwarded. With this
alias, you can replace `git-pr-branch` with just `git pr` in the following examples.

## Checking out pull requests

`git-pr-branch checkout 42` will a pull request #42 in a local branch, creating a new branch each
time the command is run. Why, you ask? Because it is common for PR authors to amend their commits
after a review instead of adding more commits, and as a reviewer it's hard to see the differences
between the code you reviewed and the new code. By creating a new branch each time, you can just
diff with the previous branch.

If you have not checked out this PR before, it will create a branch for every existing review in the
PR's history. This way it'll be easy to see what's changed between earlier reviews even if you did
not run the command at that time.

## Displaying branches and pull requests

`git-pr-branch show` will list all your local branches and show you whether they are associated with
a pull request, whether that PR is still open or not, and the URL for that PR.

## Purging branches

`git-pr-branch purge` will delete the branches that are linked to a closed pull request (or multiple
pull requests that are all closed). This will let you keep your local repo tidy.
