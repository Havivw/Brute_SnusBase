SnusBase Brute 
=====

## Installation

clone the directory

```shell
$ cd SnusBase
$ pip3 install .

```


## Usage

```shell
$ snusbrute -h
Usage: snusbrute [OPTIONS]

  Run BruteForce on SnusBase using aa*@*domain*

Options:
  -u, --user TEXT      SnusBase user name.
  -p, --password TEXT  SnusBase password.
  -d, --domain TEXT    Domain name for BruteForce (without). search regex
                       (aa*@*domain*)
  -v, --verbose        Display run log in verbose mode.
  -h, --help           Show this message and exit.

```

### Run SnusBase Brute.

```shell
$ snusbrute -u <user> -p <password> -d <domain> -v
user@ubuntu:~$ cat SnusBrute.log
INFO     - SnusBrute -  Extract Cookies and CSRF_Token Details.
INFO     - SnusBrute -  Start BruteForce on SnusBase.
SUCCESS     - SnusBrute -  vk%@%<domain>%
FAIL     - SnusBrute -  gf Failed!

```



## Additional Info

* Need to buy SnusBase User

## Export Data to CSV FILE
```
$ cat Credentials_File_<domain>.csv
User Name, Domain Name, Hash,  Hash Type, Password, Dump
username,  domain.com, 8cb2237d0679ca88db6464eac60da96345513964, sha1, 12345, Collection1
```

## Contributions..

are always welcome...
