from django.core.management.base import BaseCommand
from attendance.models import DeviceLog
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Add random DeviceLog entries with unique MAC addresses, names, and emails.'

    def handle(self, *args, **kwargs):
        names = [
            'Alpha Device', 'Beta Device', 'Gamma Device', 'Delta Device', 'Epsilon Device',
            'Zeta Device', 'Eta Device', 'Theta Device', 'Iota Device', 'Kappa Device'
        ]
        domains = ['cosmoscollege.edu.np', 'example.com']
        for i in range(10):
            mac = '02-00-00-%02x-%02x-%02x' % (
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )
            name = random.choice(names)
            email = f"{name.lower().replace(' ', '')}{i}@{random.choice(domains)}"
            ip = f"192.168.1.{random.randint(2, 254)}"
            DeviceLog.objects.create(
                mac_address=mac,
                ip_address=ip,
                is_known=False,
                first_seen=timezone.now(),
                last_seen=timezone.now(),
            )
        self.stdout.write(self.style.SUCCESS('Added 10 random DeviceLog entries.')) 