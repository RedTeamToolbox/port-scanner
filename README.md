<p align="center">
    <a href="https://github.com/OffSecToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/offsectoolbox/black-and-white-circle-256.png" alt="OffSecToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/actions/workflows/cicd-pipeline-shared.yml">
        <img src="https://img.shields.io/github/workflow/status/OffSecToolbox/port-scanner/CICD%20Pipeline%20(Shared)/master?label=shared%20pipeline&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/actions/workflows/cicd-pipeline-custom.yml">
        <img src="https://img.shields.io/github/workflow/status/OffSecToolbox/port-scanner/CICD%20Pipeline%20(Custom)/master?label=custom%20pipeline&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://codecov.io/gh/OffSecToolbox/port-scanner">
        <img src="https://img.shields.io/codecov/c/gh/OffSecToolbox/port-scanner?label=code%20coverage&style=for-the-badge" alt="code coverage" />
    </a>
    <br />
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/threaded-portscanner/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

A multi-server mult-threaded multi-port scanner.

## Disclaimer

This tool has been designed and built with a number of specific people and purposes in mind:
1. To assist offensive security specialists to identify issues with systems they are `legally responsible for` to help in the timely remediation of security issues.
2. To insist system owners to identify issues with systems they are `legally responsible for` to help in the timely remediation of security issues.
3. For people interested in security to learn about different ways of testing a system `within the bounds of the law`.

The one thing tying all of these uses together is `legal ownership or responsibility`. Any system that you use as a `target` for this tool must be a system you have permission to target!

If you do not have permission then you are very likely committing a criminal offense in the jurisdiction where you reside as well as the jurisdiction where the targeted system resides. For example in the United Kingdom, this would be covered by the [`Police and Justice Act 2006: Section 36`](https://www.legislation.gov.uk/ukpga/2006/48/part/5/crossheading/computer-misuse)

Don't download this tool if you want to use it for nefarious purposes. In short:

<br />
<p align="center"><img src="https://cdn.wolfsoftware.com/assets/images/misc/dbad.png" alt="Don't be a dick" /></p>

## Usage

```text
usage: port-scan [-h] [-q] [-v] [-4] [-6] [-A] [-c] [-d] [-j] [-s] [-r] [-t TARGETS] [-b BATCH_SIZE] [-B BATCH_DELAY] [-D DELAY_TIME] [-p INCLUDE_PORTS] [-e EXCLUDE_PORTS] [-T THREADS] [-f FILENAME]

Check for open port(s) on target host(s)

flags:
  -h, --help            show this help message and exit
  -q, --quiet           Do not show the results on the screen (default: False)
  -v, --verbose         Verbose output - show scan results as they come in (default: False)
  -4, --ipv4-only       Scan IPv4 addresses only (default: False)
  -6, --ipv6-only       Scan IPv6 addresses only (default: False)
  -A, --all-results     Show or save all results (default is to list open ports only) (default: False)
  -c, --csv             Save the results as a csv formatted file (default: False)
  -d, --delay           Add a random delay to each thread (default: False)
  -j, --json            Save the results as a json formatted file (default: False)
  -s, --shuffle         Randomise the scanning order (default: False)
  -r, --list-rules      List the available rules (default: False)

required arguments:
  -t TARGETS, --targets TARGETS
                        A comma separated list of targets to scan (default: None)

optional arguments:
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        The size of the batch to use when splitting larger scan sets (0 = no batching) (default: 0)
  -B BATCH_DELAY, --batch-delay BATCH_DELAY
                        The amount of time to wait between batches in seconds (default: 60)
  -D DELAY_TIME, --delay-time DELAY_TIME
                        Random delay to use if --delay is given (default: 3)
  -p INCLUDE_PORTS, --include-ports INCLUDE_PORTS
                        The ports you want to scan (default: 1-1024)
  -e EXCLUDE_PORTS, --exclude-ports EXCLUDE_PORTS
                        The ports you want to exclude from a scan (default: None)
  -T THREADS, --threads THREADS
                        The number of threads to use (default: 40)
  -f FILENAME, --filename FILENAME
                        The filename to save the results to (default: portscan-results)

For more detailed documentation please refer to: https://github.com/OffSecToolbox/port-scanner
```
> The default number of threads is calculated based on your server. (default_threads = multiprocessing.cpu_count() * 5). However if the number of ports you are testing is less than the default then the default is lowered to the number of checks.

There are a number of ways to specify which ports to scan: service names, port numbers, port ranges and rulsets:

##### Service names
* Names: ssh or http or any other valid service name (see /etc/services)

##### Port numbers
* Numbers: 22, 443 or any other valid port number

##### Port ranges
* Ranges: start-end OR start:end

##### Rulesets
* Rulesets: ruleset:rule-set-name 
> Use -r or --list-rules to see the predefined ruleset names and associated ports

You can use any combination of the above with the -p (or --include-ports) and the -e (--exclude-ports) to create the required port set.

#### Example
```text
port-scanner.pt -t localhost -p 22,ruleset:file-transfer,http,8000-9000
```

You can also use file:filename and specify a file (or multiple files with the same logic as rulesets) to load port settings from a file. The rules can be on multiple lines or the same line (comma separated) or both and they are formatted exactly the same as the -p (and -e) parameter, so files can contain rulesets, port numbers and names.

#### Example
```text
port-scanner.pt -t localhost -p filename:rules.txt,ruleset:file-transfer,http,8000-9000
```

Finally, there is not limit to the number of times you can specify rulesets or files, so you can change multiple files and rulesets together to make a completed port set. 

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
