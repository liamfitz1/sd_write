import machine
import vfs
import time
import sdcard


class SDManager:
    def __init__(
        self,
        spi_id=1,
        sck=10,
        mosi=11,
        miso=12,
        cs=13,
        baudrate=1_000_000
        ):
        self.spi = machine.SPI(
            spi_id,
            baudrate,
            polarity=0,
            phase=0,
            sck=machine.Pin(sck),
            mosi=machine.Pin(mosi),
            miso=machine.Pin(miso)
        )
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.sd_card = None
        self.vfs = None
        self.mount_point = "/new"
        self.is_mounted = False

    def mount_sd(self):
        if not self.is_mounted:
            try:
                self.sd_card = sdcard.SDCard(self.spi, self.cs)
                self.vfs = vfs.VfsFat(self.sd_card)
                vfs.mount(self.vfs, self.mount_point)
                self.is_mounted = True
            except OSError as e:
                print(f"Unable to mount {self.mount_point}: {e}")
        else:
            print("Card is already mounted.")

    def unmount_sd(self):
        if self.is_mounted:
            try:
                vfs.umount(self.mount_point)
                self.sd_card = None
                self.vfs = None
                self.is_mounted = False
            except OSError as e:
                print(f"Unable to unmount: {e}")
        else:
            print("Card is not mounted.")

    def write_sd(self, data):
        if not self.is_mounted:
            print("Card is not mounted.")
            return

        filename = f"{self.mount_point}/outfile.txt"

        try:
            with open(filename, "a") as f:
                f.write(data + "\n")
        except Exception as e:
            print(f"Error writing file: {e}")
        else:
            print("Wrote data.")
