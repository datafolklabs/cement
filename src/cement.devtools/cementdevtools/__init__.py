
from pkg_resources import get_distribution

CEMENT_VERSION = get_distribution('cement').version

(base, major) = CEMENT_VERSION.split('.')[:2]
CEMENT_MAJOR_VERSION = '.'.join(CEMENT_VERSION.split('.')[:2])

if int(major)%2==0:
    CEMENT_NEXT_VERSION = float(CEMENT_MAJOR_VERSION) + 0.1
else:
    CEMENT_NEXT_VERSION = float(CEMENT_MAJOR_VERSION) + 0.2
