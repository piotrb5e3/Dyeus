from django.db import models


class Appliance(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('users.DyeusUser', on_delete=models.CASCADE,
                              related_name='appliances')

    class Meta:
        unique_together = ('name', 'owner')


class Reading(models.Model):
    appliance = models.ForeignKey(Appliance, related_name='readings',
                                  null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
