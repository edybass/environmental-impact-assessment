"""
Environmental Impact Assessment API
Professional REST API for EIA system

Author: Edy Bassil
Email: bassileddy@gmail.com
"""

from .app import app
from .endpoints import all_routers
from .schemas import *

__all__ = [
    'app',
    'all_routers'
]