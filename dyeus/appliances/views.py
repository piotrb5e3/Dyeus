from cornice import Service
from .managers import get_all_appliances

appliances = Service(name='appliances', path='/appliances')


@appliances.get()
def get_appliances(request):
    return {
        'appliances': [
            {
                'id': appliance.id,
                'name': appliance.name,
            } for appliance in get_all_appliances()]
    }
