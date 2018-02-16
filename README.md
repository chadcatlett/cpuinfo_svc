# cpuinfo_svc

cpuinfo_svc provides a simple http endpoint that returns a limited json version of /proc/cpuinfo

## Original Problem Description

```
Create a Vagrant Centos 7 VM which runs a small web service on port 8080. This service should give the contents of the VMs cpuinfo as JSON. The web service should be written in one of Ruby, Python or Go.

Example:

$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'centos/7' is up to date...
...
$ curl http://localhost:8080/
{"0":{"vendor_id":"IngenuineEntel","family":"6","model":"58","model_name":"Entel(R) Core(TM) i6-2741QM CPU @ 8.70GHz","stepping":"9","mhz":"8693.860","cache_size":"6144 KB","physical_id":"0","core_id":"0","cores":"1","flags":["fpu","vme","de","pse","tsc","msr","pae","mce","cx8","apic","sep","mtrr","pge","mca","cmov","pat","pse36","clflush","mmx","fxsr","sse","sse2","syscall","nx","rdtscp","lm","constant_tsc","rep_good","nopl","xtopology","nonstop_tsc","pni","pclmulqdq","monitor","ssse3","cx16","sse4_1","popcnt","xsave","avx","rdrand","hypervisor","lahf_lm"]},"total":1,"real":1,"cores":1}

Bonus points: demonstrate use of configuration management with Vagrant.
```

### Assumptions made

To avoid having to ask for clarification on a few minor things I decided to make some assumptions and define those assumptions here. I apologize if my interpretation of the desired definition differs from the author of the test.

In the json there are three metadata fields: `total, real, cores`. The following assumptions were made about the meanings of these keys.

* total: total number of logical processors found in /proc/cpuinfo
* real: total number of physical socketed cpu packages
* cores: total number of silicon cores found in /proc/cpuinfo

## Getting started


To give cpuinfo_svc a spin, use the provided Vagrantfile.

Type `vagrant up` will fire up a VM, run ansible against it, and expose the web service at `http://127.0.0.1:8080/`. 

The ansible playbook also runs the unittest tests, if these fail then the whole playbook fails and the provisioning of the vm is considered a failure.

## Notes

### Dependencies

* Python 2.7.x
* CherryPy - the ansible playbook will install this.

### Requirements

* Vagrant 2.0.x
* An internet connection to pull down the CentOS 7 vagrant box.
* An internet connection to be able to install ansible and packages in the resulting CentOS 7 virtual machine.

### Alternative output

The original test instructions had a json response that had different key names than is typically found in `/proc/cpuinfo` as well as a more abridged set of values. The service renames the keys to match the output as described in the original test instructions. If a full unabridged output is desired appending `?full=1` to the url query string will result in it emitting all the data found in /proc/cpuinfo. Example url: `http://127.0.0.1:8080/?full=1`.


### Running basic CPUInfo unittests locally

While the webservice requires CherryPy to execute, the test_cpuinfo.py file can be ran on any sytem with python 2.7.x installed. To run the tests manually run `python test_cpuinfo.py -v`

### Misc.

I considered building a proper python packaging setup as well as rpm .spec for this, but due to the nature of the challenge I decided that just copying the source code into `/usr/local/bin` was sufficient.