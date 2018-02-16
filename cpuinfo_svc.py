#! /usr/bin/python2.7


from collections import OrderedDict

class CPUInfo(object):

    def __init__(self, cpuinfo_path="/proc/cpuinfo", full=False):
        self.cpuinfo_path = cpuinfo_path
        self.full = full
        self.processors = dict()
        self.total = 0
        self.real = 0
        self.cores = 0
        self.load_cpuinfo()
        
    def load_cpuinfo(self):

        rename_keys = {
            "cpu_cores": "cores",
            "cpu_mhz": "mhz",
            "cpu_family": "family",
        }

        desired_keys = [
            "vendor_id",
            "family",
            "model",
            "model_name",
            "stepping",
            "mhz",
            "cache_size",
            "physical_id",
            "core_id",
            "cores",
            "flags",
        ]

        self.processors = dict()
        self.total = 0
        self.real = 0
        self.cores = 0


        with open(self.cpuinfo_path) as cpuinfo_fd:
            raw_cpuinfo = cpuinfo_fd.read()

        cpuinfo_segments = raw_cpuinfo.split("\n\n")

        for segment_id, segment in enumerate(cpuinfo_segments):
            # Note(chad): normally would use a regular dict, but I wanted
            #   the output to remain in the same order as it appears in the
            #   procfs/cpuinfo response string.
            new_cpu = OrderedDict()

            segment_lines = segment.splitlines()
            if not segment_lines:
                # Todo(chad): Ensure that the kernel is escaping newlines
                #   for the strings it gets via the pointers with cpuid.
                #   This is mainly a concern with certain hypervisors that are
                #   known to inject stuff into the strings. 
                #   For the code challenge I think it's a fair assumption that
                #   cpuid masking tricks aren't being played. So on an empty
                #   segment just consider it the end of the procfs/cpuinfo result.
                break

            for line in segment_lines:
                k,v = line.split(":")
                k,v = (k.strip().replace(" ", "_").lower(), v.strip())
                k = rename_keys.get(k,k)
                if k in ("bugs", "flags", "power_management"):
                    v = v.split()
                new_cpu[k] = v
                    
            self.processors[str(segment_id)] = new_cpu
                        
        
        # Note(chad) this is a niave approach. In reality some CPUs can be hot-plugged
        #   and I'm not 100% certain they'd show up as in profs/cpuinfo on x86/x86-64
        #   machines when they are in an off-line state. Since the test instructions 
        #   called for Vagrant I'm assuming they are all on-call
        #
        
        physical_cpus_processed = set()
        for cpu in self.processors.itervalues():
            if cpu['physical_id'] in physical_cpus_processed:
                continue
            physical_cpus_processed.add(cpu['physical_id'])
            self.total += int(cpu['siblings'])
            self.real += 1
            self.cores += int(cpu['cores'])

        # Clean processors so that they only contain values that are desired as per
        # test instruction's output

        if not self.full:
            for processor in self.processors.itervalues():
                for key in processor.keys():
                    if key not in desired_keys:
                        del processor[key]


    def to_dict(self):
        # Note(chad): Normally I'd use a regular dict, but since the example
        #   output had the tallies at the end I'm using OrderedDict to make
        #   sure that they are at the end of the result.
        result = OrderedDict()
        result.update(self.processors)
        result['total'] = self.total
        result['real'] = self.real
        result['cores'] = self.cores
        return result
    
    

if __name__ == "__main__":
    import cherrypy

    class CPUInfoService(object):
        @cherrypy.expose
        @cherrypy.tools.json_out()
        def index(self, full=False):
            cpu_info = CPUInfo(full=full)
            return cpu_info.to_dict()

    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                        })
    cherrypy.quickstart(CPUInfoService())
