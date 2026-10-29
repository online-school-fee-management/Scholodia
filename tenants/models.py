from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class School(models.Model):
    """One school = one tenant. Identified by subdomain."""

    name = models.CharField(max_length=200)
    subdomain = models.SlugField(max_length=63, unique=True)
    eiin = models.CharField("EIIN", max_length=20, blank=True)
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.subdomain})"


class SchoolOwnedModel(models.Model):
    """
    Base class for every tenant-specific table (classes, students, fees...).
    Always filter with: Model.objects.filter(school=request.school)
    """

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True


class SchoolWebsite(models.Model):
    """Editable content for a school's public home page."""

    school = models.OneToOneField(
        School, on_delete=models.CASCADE, related_name="website"
    )
    logo = models.ImageField(
        upload_to="schools/website/", blank=True,
        help_text="Square or horizontal logo. PNG with transparency works best.",
    )
    hero_image = models.ImageField(
        upload_to="schools/website/", blank=True,
        help_text="Wide photo shown behind the welcome message.",
    )
    primary_color = models.CharField(
        max_length=7,
        default="#0d6b57",
        validators=[
            RegexValidator(
                regex=r"^#[0-9a-fA-F]{6}$",
                message="Enter a colour in the format #0d6b57.",
            )
        ],
    )
    hero_eyebrow = models.CharField(
        max_length=120, default="A community of curious minds"
    )
    hero_title = models.CharField(
        max_length=180, default="Learning today, leading tomorrow."
    )
    hero_subtitle = models.TextField(
        default=(
            "A caring school community where curiosity, character and confidence "
            "grow together."
        )
    )
    about_title = models.CharField(
        max_length=160, default="A place where every learner belongs"
    )
    about_text = models.TextField(
        default=(
            "Our teachers, families and staff work together to create a safe, "
            "welcoming environment where students are encouraged to ask questions, "
            "think independently and do their best."
        )
    )
    principal_name = models.CharField(max_length=150, blank=True)
    principal_title = models.CharField(
        max_length=120, default="Principal", blank=True
    )
    principal_message = models.TextField(blank=True)
    principal_photo = models.ImageField(
        upload_to="schools/website/", blank=True
    )
    admissions_open = models.BooleanField(
        default=True, verbose_name="Show admissions callout"
    )
    admissions_title = models.CharField(
        max_length=160, default="Admissions are open"
    )
    admissions_text = models.TextField(
        default=(
            "Visit the school office or contact us to learn about available classes, "
            "requirements and the next steps."
        )
    )
    footer_note = models.CharField(
        max_length=240,
        default="Learning with purpose, growing with confidence.",
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Website content - {self.school.name}"


class Notice(SchoolOwnedModel):
    title = models.CharField(max_length=180)
    content = models.TextField()
    published_on = models.DateField(default=timezone.localdate)
    is_important = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_important", "-published_on", "-created_at"]

    def __str__(self):
        return self.title


class GalleryImage(SchoolOwnedModel):
    title = models.CharField(max_length=160, blank=True)
    caption = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to="schools/gallery/")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title or f"Gallery image {self.pk}"


class TeacherProfile(SchoolOwnedModel):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=120)
    qualification = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="schools/teachers/", blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} - {self.designation}"
