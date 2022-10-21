<p align="center">
    <a href="https://github.com/SecOpsToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/secopstoolbox/black-and-white-circle-256.png" alt="SecOpsToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/actions/workflows/cicd-pipeline-shared.yml">
        <img src="https://img.shields.io/github/workflow/status/SecOpsToolbox/threaded-portscanner/CICD%20Pipeline%20(Shared)/master?label=shared%20pipeline&style=for-the-badge" alt="Github Build Status">
    </a>
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/actions/workflows/cicd-pipeline-custom.yml">
        <img src="https://img.shields.io/github/workflow/status/SecOpsToolbox/threaded-portscanner/CICD%20Pipeline%20(Custom)/master?label=custom%20pipeline&style=for-the-badge" alt="Github Build Status">
    </a>
    <br />
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/SecOpsToolbox/threaded-portscanner/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

A multi-server mult-threaded port scanner.

## Disclaimer

This tool hs been designed and built to assist offensive security specialists to identify and remediate issues within the bounds of the law, e.g. `consent from the owner the the BASE MINIMUM`.

If you download it and do something stupid (illegal) with it then you are on your own!

## Usage

```text
usage: portscan [-h] [-q] [-v] [-D DELAY_TIME] [-p PORTS] -t TARGETS [-T THREADS] [-a] [-c] [-d] [-f FILENAME] [-j] [-r]

Check for open ports on target host

flags:
  -h, --help            show this help message and exit
  -q, --quiet           Do not show the results on the screen (default: False)
  -v, --verbose         Verbose output (default: False)

required arguments:
  -D DELAY_TIME, --delay-time DELAY_TIME
                        Random delay to use if --delay is given (default: 3)
  -p PORTS, --ports PORTS
                        The search regex (default: 1-1024)
  -t TARGETS, --targets TARGETS
                        A comma separated list of targets to scan (default: None)
  -T THREADS, --threads THREADS
                        The number of threads to use (default: 1024)

optional arguments:
  -a, --all-results     Show all results (default is to list open ports only) (default: False)
  -c, --csv             Save the results as a csv formatted file (default: False)
  -d, --delay           Add a random delay to each thread (default: False)
  -f FILENAME, --filename FILENAME
                        The filename to save the results to (default: portscan-results)
  -j, --json            Save the results as a json formatted file (default: False)
  -r, --random          Randomise the scanning order (default: False)

Port options: port range e.g. 1-1024 or 1:1024, port number e.g. 22, service name e.g. ssh
```

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
