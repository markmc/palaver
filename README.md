palaver
=======

This is a script to help members of openstack-stable-maint keep notes
about git commits on the master branch - e.g. whether to backport the
commit to stable, whether it has been backported and merged already
etc.

See also: http://wiki.openstack.org/StableBranch

Usage
-----

I want to keep some notes on the master branch of Nova since the
2012.1 release. (This range of commits is harcoded in the script
at the moment)

First, I need to decide where to keep these notes. I'm using the
refs/notes/essex-notes ref, so:

    $> cd ~/git/openstack/nova
    $> export GIT_NOTES_REF=refs/notes/essex-notes
    $> export PATH=$PATH:~/git/openstack/palaver/bin
    $> export PYTHONPATH=~/git/openstack/palaver/

Next, I want to review each of the commits on master since the
2012.1. To list them, simply do:

    $> palaver list

To look at only those I haven't already reviewed:

    $> palaver list none

Let's get reviewing!

    $> palaver review

Then to push your notes to github:

    $> git push markmc refs/notes/essex-notes:refs/notes/essex-notes

To pull someone else's notes:

    $> git remote add blaa-notes git://github.com/blaa/nova.git
    $> git config remote.blaa-notes.fetch +refs/notes/essex-notes:refs/notes/blaa/essex-notes
    $> git fetch blaa-notes
    $> export GIT_NOTES_REF=refs/notes/blaa/essex-notes
    $> palaver list

TODO
----

 - add a config file
 - add timestamps to comments
 - merging comments from multiple sources
 - cherry-pick convenience command
