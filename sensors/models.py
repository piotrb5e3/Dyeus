from django.db import models


class Sensor(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    appliance = models.ForeignKey('appliances.Appliance',
                                  related_name='sensors',
                                  null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = [('name', 'appliance'), ('code', 'appliance')]


class SensorValue(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.PROTECT,
                               related_name='sensor_values')
    reading = models.ForeignKey('appliances.Reading', related_name='values')
    value = models.CharField(max_length=30)

    class Meta:
        unique_together = ('sensor', 'reading')
