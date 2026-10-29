from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tenants", "0004_galleryimage_notice_schoolwebsite_teacherprofile"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SubscriptionPayment",
        ),
        migrations.RemoveField(
            model_name="school",
            name="plan",
        ),
        migrations.RemoveField(
            model_name="school",
            name="plan_expires_at",
        ),
    ]
