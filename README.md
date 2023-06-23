# check-my-certs

Simple tool to check the certficate expiration dates for a set of web sites.

## Usage

```
Usage: check_my_certs [OPTIONS]

  Console script for check_my_certs.

Options:
  -f, --filename TEXT  File listing sites to check.  [default: sites.txt]
  -d, --days INTEGER   Days until expiry for warning.  [default: 14]
  --help               Show this message and exit.
```

## File format

The input file is a text file with one site per line.

Each site is a fully qualified domain name with an optional port,
i.e. `FQDN[:port]`.  If the port is not specified 443 is used.

### Examples

```
google.com
my.django.example.com:8080
```

## Example output

All valid within the expiration window.

```
% check_my_certs -f sites.txt -d 14
google.com:443            2023-08-21 08:16:16  ✅
yahoo.com:443             2023-10-25 23:59:59  ✅
```

One expiring within the window:

```
% check_my_certs -f sites.txt -d 60
google.com:443            2023-08-21 08:16:16  ❌
yahoo.com:443             2023-09-06 23:59:59  ✅
```

One site that times out.
```
% check_my_certs -f sites.txt -d 14
google.com:443            2023-08-21 08:16:16  ✅
yahoo.com:8443            N/A                  ❌⏰
```


# Credits


This package was created with [Cookiecutter][1] and the
[audreyr/cookiecutter-pypackage][2] template.

[1]: https://github.com/audreyr/cookiecutter
[2]: https://github.com/audreyr/cookiecutter-pypackage
