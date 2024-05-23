from utils.functions import *

routes = {
    "Dev": os.getenv('DEV'),
    "Stage": os.getenv('STAGE')
    }


environment = os.getenv('ENVIRONMENT', "Dev")

base_url = routes[environment]
driver_default = get_config("driver", "default")
