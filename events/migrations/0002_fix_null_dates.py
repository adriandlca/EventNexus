from django.db import migrations
from django.utils import timezone
from datetime import datetime


def fix_event_dates(apps, schema_editor):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(events_event);")
        cols = cursor.fetchall()
        date_col = next((c for c in cols if c[1] == 'date'), None)
        if date_col is None:
            return

        if date_col[2].lower() == 'text':
            return

        cursor.execute("SELECT id, date FROM events_event;")
        rows = cursor.fetchall()

        now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        fixed_rows = []
        for event_id, current_date in rows:
            date_str = str(current_date) if current_date is not None else ''
            try:
                if len(date_str) == 10:
                    date_str = f'{date_str} 00:00:00'
                datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                final_date = date_str
            except (ValueError, TypeError):
                final_date = now
            fixed_rows.append((event_id, final_date))

        cursor.execute("""
            CREATE TABLE events_event_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image varchar(100) NOT NULL,
                title varchar(256) NOT NULL,
                date TEXT NOT NULL,
                location varchar(256) NOT NULL,
                price REAL NOT NULL,
                user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
            );
        """)

        raw_cursor = connection.cursor()
        for event_id, final_date in fixed_rows:
            safe_date = final_date.replace("'", "''")
            raw_cursor.execute(
                "INSERT INTO events_event_new (id, image, title, date, location, price, user_id) "
                "SELECT id, image, title, '" + safe_date + "', location, price, user_id "
                "FROM events_event WHERE id = " + str(int(event_id)) + ";"
            )

        cursor.execute("DROP TABLE events_event;")
        cursor.execute("ALTER TABLE events_event_new RENAME TO events_event;")

        fixed_count = sum(1 for _, d in fixed_rows if d == now)
        if fixed_count:
            print(f'[fix_event_dates] {fixed_count} evento(s) con fecha inválida corregidos a {now}')


def reverse_fix_event_dates(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_event_dates, reverse_fix_event_dates),
    ]
