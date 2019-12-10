# How to Contribute

Here is how to setup your project for contributions.

## Fork on Github

1. Visit https://github.com/wuest-halle/wuestbot
2. Click the `Fork` button (top right) to create a personal fork.

## Clone fork locally

First make sure you have created an SSH key and uploaded it on Github via
**Profile** > **Settings** > **SSH and GPG keys**.

Set `user` to match your Github profile name:

```shell
export user="your github user name"
```

Create your clone:

```shell
git clone git@github.com:$user/wuestbot.git
# or: git clone https://github.com/$user/wuestbot.git

cd wuestbot
git remote add upstream git@github.com:wuest-halle/wuestbot.git
# or: git remote add upstream https://github.com/wuest-halle/wuestbot.git

# Never push to upstream/master
git remote set-url --push upstream no_push

# Confirm your remotes make sense
git remote -v
```

## Create a feature branch

Get your local `master` up to date:

```shell
cd wuestbot
git fetch upstream
git checkout master
git rebase upstream/master
```

Then create a feature branch from it:

```shell
git checkout -b my_feature
```

You can then edit the code on the `my_feature` branch.

## Keep your branch in sync

When changes have been merged into `upstream/master` while you were developing
on `my_feature`, you need to sync up your feature branch:

```shell
# While on my_feature branch
git fetch upstream
git rebase upstream/master
```

This way you can also sync the `master` branch of your local fork (`origin`)
with `upstream/master`.

## Commit

After you have added your changes to the staging directory, commit them:

```shell
git commit
```

Please write a [well-formed][commit_message] commit message.

## Push

When you're ready to review, push your branch to Github:

> You will need to force-push (`-f`) when you rebased your branch
> previously.

```shell
git push -f origin my_feature
```

## Create a Pull Request

1. Visit your for at `https://github.com/$user/wuestbot
2. Click the `Compare & Pull Request` button next to your `my_feature` branch.
3. Write a descriptive PR message.
4. Assign one (or more) of the [authors][authors] to review your PR.

[commit_message]: https://chris.beams.io/posts/git-commit/
[authors]: ./AUTHORS.md