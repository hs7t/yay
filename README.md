# `yay` 0.1

`yay` is a format for easily defining cross-platform scripts. It's
extremely easy to write and not that useful right now.

`yay` scripts are based on **instructions**. This is an example of a 
simple `yay` script:

```bash
% yay 0.1
% title "Example script"
% revision 1
% supports '*'

! print meta.title

! clone 'https://github.com/hs7t/yay.git'
! navto randomrepo
```

Let's walk through it.

These four instructions define a few `meta` values:
```bash
% yay 0.1
% title "Example script"
% revision 1
% supports "*"
```

That `%` is a **command**. All instructions start with a command,
and the Set Global/`%` command is used for definitions. `% yay 0.1` sets the
value of the `meta` property `yay` to a number, `0.1`. In
Javascript, that would be something like this:

```javascript
meta.yay = 0.1
```

Isn't that neat?

These values we just set are useful for the `yay` **trampoline** 
(in less silly words, *runner* - more on that [later](#the-trampoline)).
`meta.yay` sets the version of `yay` we're using (for compatibility
purposes). `meta.title` is the name of your script, `revision` is
the version of your script, and `supports` is the OS your script
supports. (I recommend setting `supports` to `"*"`, a wildcard for all OSes.
You probably shouldn't use any other values.)

Let's look at the next instruction:

```bash 
! print meta.title
```

This is another command! Run Action/`!` runs an action. It's the core
of this whole thing. Many commands are different in different shells.
`yay` makes supporting more platforms easier by abstracting the shell
away.

With `! print meta.title`, we're printing the value of the `meta`
property `title` to the user's console. Awesome!

The next instruction looks like this:
```bash
! clone 'https://github.com/hs7t/yay.git'
```

Which would be equivalent to writing...
```bash
$ git clone 'https://github.com/hs7t/yay.git'
```

Here's something fun - that line above is also a valid `yay`
instruction! So if you're for some reason using Mercurial, you
could do something like this:
```bash
! print "I'm a happy Mercurial user!"
$ hg clone 'hg clone https://www.mercurial-scm.org/repo/hg/'
```

That `$` command we're using is called Shell Run. When the instruction
`$ hg clone 'hg clone https://www.mercurial-scm.org/repo/hg/'` is run
the text `hg clone 'hg clone https://www.mercurial-scm.org/repo/hg/`
will be entered into the shell and run.

## The trampoline
The `yay` trampoline is multi-platform CLI that reads and runs `yay`
scripts. It's written in some very messy Python.
