![The yay logo](assets/yay.svg)

# `yay` 0.1

`yay` is a format for easily defining cross-platform scripts. It's
extremely easy to write and not that useful right now.

[![asciicast](https://asciinema.org/a/OSiEvhDNa8ckVGT5iu5CWq9ks.svg)](https://asciinema.org/a/OSiEvhDNa8ckVGT5iu5CWq9ks)

`yay` scripts are based on **instructions**. This is an example of a
simple `yay` script:

```bash
% yay 0.1
% title "Example script"
% revision 1
% supports '*'

! print "Hello, world!"

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
JavaScript, that would be something like this:

```javascript
meta.yay = 0.1;
```

Isn't that neat?

These values we just set are useful for the `yay` **trampoline**
(in less silly words, _runner_ - more on that [later](#the-trampoline)).
`meta.yay` sets the version of `yay` we're using (for compatibility
purposes). `meta.title` is the name of your script, `revision` is
the version of your script, and `supports` is the OS your script
supports. (I recommend setting `supports` to `"*"`, a wildcard for all OSes.
You probably shouldn't use any other values.)

Let's look at the next instruction:

```bash
! print "Hello, world!"
```

This is another command! Run Action/`!` runs an action. It's the core
of this whole thing. Many commands are different in different shells.
`yay` makes supporting more platforms easier by abstracting the shell
away.

With `! print "Hello, world!"`, we're printing the string "Hello, world!" 
to the user's console. Awesome!

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
`$ hg clone "https://www.mercurial-scm.org/repo/hg/"` is run,
`hg clone "https://www.mercurial-scm.org/repo/hg/"` will be passed to
the shell. Nice!

## The trampoline

The `yay` trampoline is multi-platform CLI that reads and runs `yay`
scripts. It's written in some very messy Python.

It currently supports:

- PowerShell 5.1+
- Bash
- Windows Command Prompt
- POSIX shell
- Z shell


### Hop on! 

#### Downloading a binary
Grab yourself a binary from the [Releases](https://github.com/hs7t/yay/releases/latest/) 
tab. They're available:

- for Linux (x86-64 / arm64): `trampoline-linux-[x86_64 or arm64]`
- for macOS: `trampoline-macos-[arm64 or x86_64]`
- for Windows: `trampoline-windows-[x86_64 or arm64].exe`

> [!TIP]
> Not sure what you need? If you're running Windows or Linux, your
  device is most likely to work with the x86_64 version (unless you're
  using a Snapdragon processor or something). If you're on an Apple Silicon 
  (M1, M2, M3...) Mac, choose the arm64 binary.

##### Linux and Mac
Before you can run the binary you just downloaded on Linux or your Mac, 
you have to mark it as an executable. From your terminal, run this command:
```bash
chmod +x binary     # for example, chmod +x trampoline-macos-arm64
```

#### Optional: Update your PATH
Follow these steps:

1. Move the binary into its own folder (wherever you want - not Downloads!)
2. Run a command appropriate for your OS:
    - macOS (zsh):
        ```bash
        export PATH="$PATH:/path/to/folder"
        source ~/.zshrc
        ```
    - Linux (bash):
        ```bash
        export PATH="$PATH:/path/to/folder"
        source ~/.bashrc    # or ~/.profile, depending on your shell
        ```
    - Windows (PowerShell)
        ```powershell
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\path\to\folder", "User")
        ```
> [!TIP]
> Try renaming the binary to `yay` (or `yay.exe` on Windows)
  to use it by just typing `yay`!
