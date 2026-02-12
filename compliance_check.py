from extras.scripts import Script, MultiObjectVar
from dcim.models import Device, Site


class DeviceComplianceCheckBySite(Script):

    class Meta:
        name = "Device Compliance Check (By Site)"
        description = "Checks device compliance for selected site(s)"

    sites = MultiObjectVar(
        model=Site,
        description="Select one or more sites"
    )

    def run(self, data, commit):

        devices = Device.objects.filter(site__in=data["sites"])

        if not devices.exists():
            self.log_info("No devices found in selected site(s)")
            return

        non_compliant = 0

        for device in devices:

            issues = []

            if not device.primary_ip:
                issues.append("missing primary IP")

            if not device.platform:
                issues.append("missing platform")

            if not device.tenant:
                issues.append("missing tenant")

            if issues:
                non_compliant += 1
                self.log_warning(
                    f"{device.name} ({device.site.name}): {', '.join(issues)}"
                )

        self.log_success(
            f"Compliance check completed. "
            f"Non-compliant devices: {non_compliant} / {devices.count()}"
        )
