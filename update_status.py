from extras.scripts import Script, ObjectVar, ChoiceVar
from dcim.models import Device, DeviceType
from dcim.choices import DeviceStatusChoices
from django.utils.text import slugify

class UpdateDeviceStatusByType(Script):
    class Meta:
        name = "Update Device Status by Type"
        description = "Update the status of all devices belonging to a specific Device Type"
        commit_default = False

    # Dropdown to select the Device Type
    device_type = ObjectVar(
        model=DeviceType,
        display_field='display',
        label="Device Type"
    )

    # Dropdown to select the new Status
    new_status = ChoiceVar(
        choices=DeviceStatusChoices,
        label="New Status"
    )

    def run(self, data, commit):
        device_type = data['device_type']
        new_status = data['new_status']
        
        # Filter devices by the selected type
        devices = Device.objects.filter(device_type=device_type)
        
        if not devices.exists():
            self.log_warning(f"No devices found for type: {device_type}")
            return

        self.log_info(f"Updating {devices.count()} devices to status: {new_status}")

        for device in devices:
            old_status = device.status
            device.status = new_status
            device.save()
            self.log_success(f"Updated {device.name or device.id}: {old_status} -> {new_status}")

        if commit:
            self.log_info("Changes committed to the database.")
        else:
            self.log_info("Dry run complete. No changes were saved.")