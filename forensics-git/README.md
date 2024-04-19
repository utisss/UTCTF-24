# A Very Professional Website

* **Event:** UTCTF 2024
* **Problem Type:** Forensics
* **Tools Required / Used:** .git directory downloader

## Steps​

### Step 1

First, we can look around the website and see that it is pretty bare bones. Since all of the links refer to locations out of scope of the CTF, this is a sign to look for something that is not directly accessible.

### Step 2

One mistake that a website owner could make is accidentally allowing people to access the `.git` directory. First, we can try to access `./.git`, however directory listing is disabled so we just get a 403 page, but this does at least suggest that there is a git repository in the current directory (we just can't get to it like this). Next, we can try to access a file that would be found in any `.git` directory, such as the `HEAD` file. When we go to `./.git/HEAD`, the web browser downloads the file, meaning that we do have access to the contents of `.git`.

### Step 3

Now, we need to figure out a way to get as much of the `.git` directory as we can. There are many tools that can be used for this - I used [git-dumper](https://github.com/arthaud/git-dumper), which allowed me to download the reachable objects from `.git`, in addition to the static website content.

### Step 4

Once we have a local copy of the repository, we need to try to find the flag within it. The way I did this was by running `git reflog` and noticing that there is a `secrets` branch, on which a commit `bba6392` was created. So we can run `git checkout bba6392` and see that it created a file `secrets.html`, which contains the flag `utflag{gitR3fl0g}`.
