from datetime import datetime, timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

AUTH_MODEL_CHOICES = [
    ('token', 'Token'),
    ('gcm_aes', 'GCM + AES128'),
    ('sha_hmac', 'SHA256 HMAC')
]


class Appliance(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    authentication_model = models.CharField(max_length=16,
                                            choices=AUTH_MODEL_CHOICES)
    authentication_value = models.CharField(max_length=64, unique=True)
    owner = models.ForeignKey('users.DyeusUser', on_delete=models.CASCADE,
                              related_name='appliances')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Appliance, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'owner')


class Reading(models.Model):
    appliance = models.ForeignKey(Appliance, related_name='readings',
                                  null=True, on_delete=models.SET_NULL)
    year = models.IntegerField(
        validators=(MinValueValidator(2000), MaxValueValidator(9999)))
    month = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(12)))
    day = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(31)))
    hour = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(23)))
    minute = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(59)))
    second = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(59)))
    microsecond = models.IntegerField(
        validators=(MinValueValidator(0), MaxValueValidator(1000000 - 1)))

    timestamp = models.DateTimeField()

    def clean(self):
        expected_timestamp = datetime(self.year, self.month, self.day,
                                      self.hour, self.minute, self.second,
                                      self.microsecond, tzinfo=timezone.utc)
        if self.timestamp != expected_timestamp:
            raise ValidationError("Timestamp should match other time fields")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Reading, self).save(*args, **kwargs)
