__name__ = "muallef.onset"
__package__ = "muallef.onset"

from muallef.onset.detection_functions import onset_function
from muallef.onset.peak_picker import peak_pick
from muallef.onset.detect_onsets import detect_onsets as detect

__all__ = ['detect', 'onset_function', 'peak_pick']
