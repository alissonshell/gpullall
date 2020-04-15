**gpullall**
============================

Pull all your *git* repositories.

**Installation**

``pip install -e .``

**Usage**

``--directory -D``  Enter a directory manually

``--confirmall -Y`` Confirm to pull every single founded repository automatically.

``--fullscan -F`` Search git repositories in your disk.

``--ignore -I`` Ignore repositories. eg: "--ignore repo1,repo2,repo3..."

``--commit, -C`` Commit changes on your repositories. (**May** not be used with --stash)

``--stash, -S`` Stash changes on your repositories before pull. (**May** not be used with --commit)
