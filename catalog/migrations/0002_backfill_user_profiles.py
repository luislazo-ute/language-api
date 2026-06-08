from django.db import migrations


def crear_perfiles_faltantes(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('catalog', 'UserProfile')
    perfiles_existentes = set(
        UserProfile.objects.values_list('user_id', flat=True)
    )
    nuevos = [
        UserProfile(user_id=uid)
        for uid in User.objects.values_list('id', flat=True)
        if uid not in perfiles_existentes
    ]
    UserProfile.objects.bulk_create(nuevos)


def revertir(apps, schema_editor):
    # No se eliminan perfiles al revertir.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_perfiles_faltantes, revertir),
    ]
