<p align="center">
    <a href="https://github.com/OffSecToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/offsectoolbox/black-and-white-circle-256.png" alt="OffSecToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/OffSecToolbox/port-scanner/actions/workflows/cicd-pipeline-shared.yml">
        <img src="https://img.shields.io/github/workflow/status/OffSecToolbox/port-scanner/CICD%20Pipeline%20(Shared)/master?label=shared%20pipeline&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/OffSecToolbox/port-scanner/actions/workflows/cicd-pipeline-custom.yml">
        <img src="https://img.shields.io/github/workflow/status/OffSecToolbox/port-scanner/CICD%20Pipeline%20(Custom)/master?label=custom%20pipeline&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://codecov.io/gh/OffSecToolbox/port-scanner">
        <img src="https://img.shields.io/codecov/c/gh/OffSecToolbox/port-scanner?label=code%20coverage&style=for-the-badge" alt="code coverage" />
    </a>
    <br />
    <a href="https://github.com/OffSecToolbox/port-scanner/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/port-scanner/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/port-scanner/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/OffSecToolbox/port-scanner/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

A multi-server mult-threaded multi-port scanner.


## Usage

```text
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
