from sd_manager import SDManager

sd_card = SDManager()

sd_card.mount_sd()

sd_card.write_sd("Test")

sd_card.unmount_sd()
