from django.core.management.base import BaseCommand

from shop.models import Product

GUITARS = [
    ("Alder Standard Stratocaster", "STR-001", 1299, 6, "Double-cutaway electric with three single-coil pickups, a bright and articulate voice, and a comfortable contoured body."),
    ("Mahogany Single Cut", "SGC-002", 1899, 4, "Warm, sustaining electric with humbucking pickups and a carved maple top. Built for rhythm and lead alike."),
    ("Dreadnought Spruce D-28", "DRD-003", 2450, 3, "Solid Sitka spruce top over East Indian rosewood. A full, resonant acoustic with a strong low end."),
    ("Parlor Travel Acoustic", "PRL-004", 549, 10, "Small-bodied acoustic that is easy to carry and easy to play. Great for songwriting and the couch."),
    ("Hollow Body Jazz Archtop", "JZZ-005", 2199, 2, "Laminated maple archtop with a floating pickup. Round, smooth tone for jazz and blues."),
    ("Classical Nylon Cedar", "CLS-006", 689, 8, "Cedar top, nylon strings, and a wide neck for fingerstyle and classical repertoire."),
    ("Offset Surf Electric", "OFS-007", 999, 5, "Offset-waist electric with a spring-loaded tremolo and a clear, jangly tone."),
    ("Short Scale Bass", "BSS-008", 749, 7, "Four-string bass with a short scale for easy reach and a deep, round sound."),
]


class Command(BaseCommand):
    help = "Add sample guitars to the shop."

    def handle(self, *args, **options):
        for name, sku, price, stock, description in GUITARS:
            Product.objects.update_or_create(
                sku=sku,
                defaults={"name": name, "price": price, "stock": stock, "description": description},
            )
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(GUITARS)} guitars."))
