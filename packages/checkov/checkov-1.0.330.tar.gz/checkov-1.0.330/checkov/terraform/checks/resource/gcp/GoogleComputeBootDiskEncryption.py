from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckResult, CheckCategories


class GoogleComputeBootDiskEncryption(BaseResourceCheck):
    def __init__(self):
        name = "Ensure VM disks for critical VMs are encrypted with CustomerSupplied Encryption Keys (CSEK)"
        id = "CKV_GCP_38"
        supported_resources = ['google_compute_instance']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'boot_disk' in conf.keys():
            if 'disk_encryption_key_raw' in conf['boot_disk'][0] or 'kms_key_self_link' in conf['boot_disk'][0]:
                return CheckResult.PASSED
        return CheckResult.FAILED



check = GoogleComputeBootDiskEncryption()
