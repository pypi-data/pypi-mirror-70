from . import filters
from . import masking
from . import structures
from . import visualization
from . import workflows

def get_version():
    """Get the version of the code from egg_info.
    Returns:
      the package version number
    """
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        version = get_distribution(__name__.split('.')[0]).version # pylint: disable=no-member
    except DistributionNotFound: # pragma: no cover
        version = "unknown, try running `python setup.py egg_info`"

    return version

__version__ = get_version()

__all__ = ['__version__',
           'filters',
           'masking',
           'structures',
           'visualization',
           'workflows']
