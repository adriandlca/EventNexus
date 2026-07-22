import os
from datetime import timedelta
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw

from events.models import Event


PLACEHOLDER_COLORS = [
    ("#9019e6", "#ffffff"),
    ("#118ab2", "#ffffff"),
    ("#06d6a0", "#000000"),
    ("#ef476f", "#ffffff"),
    ("#ffd166", "#000000"),
]


def make_placeholder_png(label: str, bg: str, fg: str) -> ContentFile:
    img = Image.new("RGB", (1200, 630), bg)
    draw = ImageDraw.Draw(img)
    draw.text((40, 280), label, fill=fg)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue(), name=f"{label.lower().replace(' ', '_')}.png")


SAMPLE_EVENTS = [
    {"title": "Concierto de Rock", "days": 7, "location": "Auditorio Central", "price": 45.0},
    {"title": "Feria de Comida", "days": 14, "location": "Parque Norte", "price": 0.0},
    {"title": "Charla de Tecnologia", "days": 21, "location": "Coworking Lima", "price": 15.0},
    {"title": "Festival de Cine", "days": 30, "location": "Cineplanet", "price": 25.0},
    {"title": "Maraton Nocturna", "days": 45, "location": "Malecon de Miraflores", "price": 30.0},
]


class Command(BaseCommand):
    help = "Crea un usuario demo y eventos de muestra para portafolio."

    def handle(self, *args, **options):
        username = "demo"
        email = "demo@example.com"
        password = "demo12345"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario demo creado ({username}/{password})"))
        else:
            self.stdout.write(f"Usuario demo ya existe ({username})")

        if Event.objects.exists():
            self.stdout.write("Ya hay eventos cargados, omitiendo seed.")
            return

        now = timezone.now()
        for i, data in enumerate(SAMPLE_EVENTS):
            bg, fg = PLACEHOLDER_COLORS[i % len(PLACEHOLDER_COLORS)]
            image_file = make_placeholder_png(data["title"], bg, fg)
            event = Event(
                user=user,
                title=data["title"],
                date=now + timedelta(days=data["days"]),
                location=data["location"],
                price=data["price"],
            )
            event.image.save(image_file.name, image_file, save=False)
            event.save()
            self.stdout.write(self.style.SUCCESS(f"  - Evento creado: {event.title}"))

        self.stdout.write(self.style.SUCCESS("Seed completado."))
