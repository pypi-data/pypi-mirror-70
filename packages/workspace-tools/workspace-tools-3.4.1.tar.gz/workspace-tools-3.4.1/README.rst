workspace-tools
===============

Tools to simplify working with multiple Python repositories by seamlessly integrating git and tox,
where you can simply run one command instead of many native commands individually to do common tasks.

It is mostly a wrapper on top of existing tools with the end goal of providing a simple, seamless,
and less repetive experience when working with one or more repositories. Feature support is mostly
limited to what the author uses as, currently, it is foremost a personal tool to enhance the
author's own productivity, but sharing it as others might find it useful.


Overview
========

* One tool to seamlessly manage / integrate all workspace tools, from setup to publish.
* Simplified command execution for common workflow - just run one command, instead of many individual native ones.
* Command execution is also smart / optimized - e.g. test command auto detects requirement changes to redevelop.
* Path aware context commands that run across all checkouts - e.g. see status / diff for all repos.
* Get the most out of other products by easily updating your dependencies to the latest
* Templates included to setup new product quickly
* Support for multiple branches with child/parent relationship.
* Cool and sensible shortcut aliases to help you do more by typing less - you will love "tv" [if you know ag]!


Quick Start Tutorial
====================

First, install it with::

    sudo pip3 install autopip
    app install workspace-tools

Second, optionally setup environment with bash functions/aliases:

.. code-block:: console

    $ cd ~/workspace

    $ wst setup --commands-with-aliases

    [INFO] Added "ws" bash function with workspace directory set to ~/workspace
    [INFO] Added bash functions: bump, checkout, clean, commit, log, publish, push, status, test, update
    [INFO] Added aliases: co=checkout, ci=commit, di=diff, st=status, up=update
    [INFO] Added special aliases: a='activate', d='deactivate',
           tv='open_files_from_last_command'  # from ag/ack/grep/find/which [t]o [v]im
    [INFO] To use, run "source ~/.wstrc" or open a new shell.

    $ source ~/.wstrc

Then witness the awesome power of workspace-tools:

.. code-block:: console

    $ ws
    # Runs `cd ~/workspace && ls`
    aiohttp-requests               localconfig              python-examples
    ansible-hostmanager            pytest-fixtures          utils-core
    ...

    $ cd localconfig
    # Use your favorite editor to make some changes

    $ ci -tp 'This adds/commits all files, runs style check/tests with coverage, and then pushes to all remotes!'
    Checking style
    Running tests
    ...........................
    ----------- coverage: platform linux, python 3.6.5-final-0 -----------
    Name                      Stmts   Miss  Cover
    ---------------------------------------------
    localconfig/__init__.py       2      0   100%
    localconfig/manager.py      215     14    93%
    localconfig/utils.py         20      0   100%
    ---------------------------------------------
    TOTAL                       237     14    94%
    Required test coverage of 80% reached. Total coverage: 81.90%
    ==================  22 passed in 0.82 seconds  =======================
    cover: OK
    style: OK
    [master d5f6e6b] This adds/commits all files, runs style check/tests with coverage, ...
     1 file changed, 78 insertions(+), 38 deletions(-)
    Pushing master

The remaining tutorial will assume `wst setup -a` was not run for the sake of clarity, though setup is
recommended as there are many useful aliases provided.

To checkout a repo:

.. code-block:: console

    $ wst checkout maxzheng/workspace-tools       # Exact match from Github
    $ wst checkout requests                       # Best match from Github
    $ wst checkout https://github.com/maxzheng/aiohttp-requests.git

To update all repos in your workspace concurrently:

.. code-block:: console

    $ wst update

    Updating aiohttp-requests
    Updating ansible-hostmanager
    ...

Make a commit and create a new branch for it:

.. code-block:: console

    $ cd workspace-tools
    # vi README.rst and make some changes

    $ wst commit "Updated README.rst"

    [updated-readme@master 0af8850] Updated README.rst
     1 file changed, 1 deletion(-)

    # The commit created the branch 'updated-readme@master', added all files, and then committed change.
    # Notice the "@master" that indicates the parent branch. The parent branch will be used
    # during push with --merge and when updating the branch (updates parent and rebases branch on top).
    # To create a branch without parent relationship, use --branch option with any name that you like.

To install your test environment and run all tests (via tox/pytest):

.. code-block:: console

    $ wst test
    ...
    cover: OK
    style: OK

    # To setup a new project with tox test, cover, and style environments:
    $ cd new-product
    $ wst setup --product

    # To check style or generate coverage report:
    $ wst test style
    $ wst test cover

    # To run a specific test only:
    $ wst test -k test_filter

To see status for a single repo or all of your repos:

.. code-block:: console

    $ wst status
    # Branches: updated-readme@master master

    $ cd ..

    $ wst status

    [ bumper-lib ]
    On branch master
    Your branch is up-to-date with 'origin/master'.
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

            modified:   src/bumper/cars.py

    no changes added to commit (use "git add" and/or "git commit -a")

    [ clicast ]
    # Branches: master display-changes@master fix-download@master

    [ workspace-tools ]
    # Branches: updated-readme@master master


To amend a change and push:

.. code-block:: console

    $ cd workspace-tools
    # vi README.rst and make more changes

    $ wst commit --amend --push

    [updated-readme@master 738f659] Updated README.rst
    1 file changed, 2 insertions(+), 1 deletion(-)
    Pushing updated-readme@master

    # It will fail at push as you are not a committer, but the change was committed to branch,
    # and then merged into its parent branch (master).

Or simply push the change in your current branch:

.. code-block:: console

    $ wst push --merge

    # This will update its parent branch (master), rebase branch with parent branch and merge into
    # parent branch if on child branch (child@parent) and then push.
    # Upon success, it will remove the local and remote branch if pushing from child branch.

If you have multiple upstream branches (defined by merge config in ~/.config/workspace.cfg) that you need to merge
your change into, use auto merge:

.. code-block:: console

    # Assuming you are currently on 3.2.x branch and have these branches: 3.3.x, master
    $ wst merge --all

    [INFO] Merging 3.2.x into 3.3.x
    [INFO] Pushing 3.3.x
    [INFO] Merging 3.3.x into master
    [INFO] Pushing master

If you have pinned your dependency requirements and want to update to latest version:

.. code-block:: console

    $ wst bump

    [INFO] Updating workspace-tools
    [INFO] Checking bumper-lib
    ...
    [INFO] Checking requests
    [bump ac06160] Require remoteconfig==0.2.4, requests==2.6.0
     1 file changed, 2 insertions(+), 2 deletions(-)

    # To bump to a specific version (why not just vi? This validates the version for you and pulls in the changelog)
    $ wst bump requests==2.5.1

To bump version, update changelog, and release to PyPI:

.. code-block:: console

    $ publish
    PyPI Password:
    Updating master
    Building source/built distribution
    Uploading to PyPI
    [master a58b001] Publish version 1.0.7
     2 files changed, 8 insertions(+), 2 deletions(-)
    Pushing master

Now you are ready to try out the other commands yourself:

.. code-block:: console

    $ wst -h

    usage: wst [-h] [-v] [--debug] <sub-command> ...

    optional arguments:

      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      --debug               Turn on debug mode

    sub-commands:
      {bump,checkout,co,clean,commit,ci,diff,di,log,publish,push,setup,status,st,test,update,up}
                            List of sub-commands
        bump                Bump dependency versions in requirements.txt,
                            pinned.txt, or any specified file.
        checkout (co)       Checkout products (repo urls) or revert files.
        clean               Clean workspace by removing build, dist, and .pyc
                            files
        commit (ci)         Commit all changes locally, including new files.
        diff (di)           Show diff on current product or all products in
                            workspace
        log                 Show commit logs
        merge               Merge changes from branch to current branch
        publish             Bumps version in setup.py (defaults to patch), writes
                            out changelog, builds a source distribution, and
                            uploads with twine.
        push                Push changes for branch
        setup               Optional (refer to setup --help). Setup workspace
                            environment. Run from primary workspace directory.
        status (st)         Show status on current product or all products in
                            workspace
        test                Run tests and manage test environments for product.
        update (up)         Update current product or all products in workspace

To configure wst, refer to Configuration_ doc.


Links & Contact Info
====================

| Documentation: http://workspace-tools.readthedocs.org
|
| PyPI Package: https://pypi.python.org/pypi/workspace-tools
| GitHub Source: https://github.com/maxzheng/workspace-tools
| Report Issues/Bugs: https://github.com/maxzheng/workspace-tools/issues
|
| Follow: https://twitter.com/MaxZhengX
| Connect: https://www.linkedin.com/in/maxzheng
| Contact: maxzheng.os @t gmail.com

.. _Configuration: http://workspace-tools.readthedocs.org/en/latest/api/config.html
