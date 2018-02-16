import os
import unittest

from cpuinfo_svc import CPUInfo


class TestCPUInfo(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        possible_paths = [
            os.path.dirname(os.path.realpath(__file__)),
            os.path.realpath("."),
            "/vagrant"
        ]
        test_filename = "multi-socket-multi-core-ht-enabled"
        # Attempt to locate test-fixture data directory

        for test_path in possible_paths:
            candidate_path = os.path.join(test_path, "test-fixtures")
            candidate_file = os.path.join(candidate_path, test_filename)
            if os.path.exists(candidate_file):
                self._test_fixture_path = candidate_path
                break
        else:
            raise Exception("Failed to find test fixtures!")

    def test_single_socket_single_core_no_hyperthreading(self):
        cpuinfo_file = "single-socket-single-core-ht-disabled"
        cpuinfo_path = os.path.join(self._test_fixture_path, cpuinfo_file)
        cpuinfo = CPUInfo(cpuinfo_path)
        valid_dict = {
            "0": {
                "family": "6",
                "core_id": "0",
                "vendor_id": "IngenuineEntel",
                "flags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc pni pclmulqdq monitor ssse3 cx16 sse4_1 popcnt xsave avx rdrand hypervisor lahf_lm".split(),  # noqa: E501
                "model_name": "Entel(R) Core(TM) i6-2741QM CPU @ 8.70GHz",
                "mhz": "8693.860",
                "stepping": "9",
                "cache_size": "6144 KB",
                "cores": "1",
                "model": "58",
                "physical_id": "0"},
            "total": 1,
            "real": 1,
            "cores": 1
        }

        # convert the OrderedDicts to regular dicts for easier diff'ing
        result_dict = dict(**cpuinfo.to_dict())
        self.assertEqual(len(result_dict), 4)
        self.assertDictEqual(dict(**result_dict["0"]), valid_dict["0"])
        self.assertEqual(result_dict["total"], valid_dict["total"])
        self.assertEqual(result_dict["real"], valid_dict["real"])
        self.assertEqual(result_dict["cores"], valid_dict["cores"])

    def test_single_socket_multi_core_with_hyperthreading(self):
        cpuinfo_file = "single-socket-multi-core-ht-enabled"
        cpuinfo_path = os.path.join(self._test_fixture_path, cpuinfo_file)
        cpuinfo = CPUInfo(cpuinfo_path)
        valid_dict = {
            "0": {
                "family": "6",
                "core_id": "0",
                "vendor_id": "GenuineIntel",
                "flags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb invpcid_single retpoline tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm rdseed adx smap intel_pt xsaveopt dtherm ida arat pln pts".split(),  # noqa: E501
                "model_name": "Intel(R) Core(TM) i7-5600U CPU @ 2.60GHz",
                "mhz": "1511.338",
                "stepping": "4",
                "cache_size": "4096 KB",
                "cores": "2",
                "model": "61",
                "physical_id": "0"},
            "total": 4,
            "real": 1,
            "cores": 2
        }

        # convert the OrderedDicts to regular dicts for easier diff'ing
        result_dict = dict(**cpuinfo.to_dict())
        self.assertEqual(len(result_dict), 7)
        self.assertDictEqual(dict(**result_dict["0"]), valid_dict["0"])
        self.assertEqual(result_dict["total"], valid_dict["total"])
        self.assertEqual(result_dict["real"], valid_dict["real"])
        self.assertEqual(result_dict["cores"], valid_dict["cores"])

    def test_multi_socket_multi_core_with_hyperthreading(self):

        cpuinfo_file = "multi-socket-multi-core-ht-enabled"
        cpuinfo_path = os.path.join(self._test_fixture_path, cpuinfo_file)
        cpuinfo = CPUInfo(cpuinfo_path)
        valid_dict = {
            "0": {
                "family": "6",
                "core_id": "0",
                "vendor_id": "GenuineIntel",
                "flags": "fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm ida arat epb pln pts dtherm tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid cqm xsaveopt cqm_llc cqm_occup_llc".split(),  # noqa: E501
                "model_name": "Intel(R) Xeon(R) CPU E5-2650 v3 @ 2.30GHz",
                "mhz": "2301.000",
                "stepping": "2",
                "cache_size": "25600 KB",
                "cores": "10",
                "model": "63",
                "physical_id": "0"},
            "total": 40,
            "real": 2,
            "cores": 20
        }
        valid_dict["vendor_id"] = 1
        # convert the OrderedDicts to regular dicts for easier diff'ing
        result_dict = dict(**cpuinfo.to_dict())
        self.assertEqual(len(result_dict), 43)
        self.assertDictEqual(dict(**result_dict["0"]), valid_dict["0"])
        self.assertEqual(result_dict["total"], valid_dict["total"])
        self.assertEqual(result_dict["real"], valid_dict["real"])
        self.assertEqual(result_dict["cores"], valid_dict["cores"])


if __name__ == "__main__":
    unittest.main()
