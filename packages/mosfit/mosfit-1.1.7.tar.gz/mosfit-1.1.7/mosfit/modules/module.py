"""Definitions for the ``Module`` class."""
import json
from collections import OrderedDict

import numpy as np

from mosfit.printer import Printer


class Module(object):
    """Base ``Module`` class."""

    _REFERENCES = []

    def __init__(self, name, model, **kwargs):
        """Initialize module.

        This is where expensive calculations that only need to be evaluated
        once should be located.
        """
        self._name = name
        self._log = False
        self._model = model
        self._pool = model.pool()
        self._preprocessed = False
        self._wants_dense = False
        self._provide_dense = False
        self._replacements = OrderedDict()
        self._unset_recommended_keys = set()
        self._kinds_needed = set()
        if not model.printer():
            self._printer = Printer()
        else:
            self._printer = model.printer()

    def __repr__(self):
        """Return a string representation of self."""
        dict_copy = {}
        for key in self.__dict__.keys():
            # Ignore associated classes.
            if key in ['_model', '_pool', '_printer']:
                continue
            if isinstance(self.__dict__[key], set):
                dict_copy[key] = list(self.__dict__[key])
            else:
                dict_copy[key] = self.__dict__[key]
        return json.dumps(dict_copy)

    def process(self):
        """Process module, should always return a dictionary."""
        return OrderedDict()

    def reset_preprocessed(self, exceptions):
        """Reset preprocessed flag."""
        if self._name not in exceptions:
            self._preprocessed = False

    def send_request(self, request):
        """Send a request."""
        return []

    def name(self):
        """Return own name."""
        return self._name

    def receive_requests(self, **requests):
        """Receive requests from other ``Module`` objects."""

    def set_event_name(self, event_name):
        """Set the name of the event being modeled."""
        self._event_name = event_name

    def set_attributes(self, task):
        """Set key replacement dictionary."""
        self._replacements = task.get('replacements', OrderedDict())
        if 'wants_dense' in task:
            self._wants_dense = task['wants_dense']

    def get_bibcode(self):
        """Return any bibcodes associated with the present ``Module``."""
        return []

    def dense_key(self, key):
        """Manipulate output keys conditionally."""
        new_key = self.key(key)
        if self._provide_dense and not key.startswith('dense_'):
            return 'dense_' + new_key
        return new_key

    def key(self, key):
        """Substitute user-defined replacement key names for local names."""
        new_key = key
        for rep in self._replacements:
            if new_key == rep:
                new_key = self._replacements[rep]
                return new_key
            elif (new_key.startswith('dense') and
                  new_key.split('_')[-1] == rep):
                new_key = 'dense_' + self._replacements[rep]
                return new_key
        return new_key

    def prepare_input(self, key, **kwargs):
        """Prepare keys conditionally."""
        if key not in kwargs:
            if 'dense_' + key in kwargs:
                kwargs[key] = np.take(
                    np.array(kwargs['dense_' + key]),
                    np.array(kwargs['dense_indices']))
            else:
                raise RuntimeError(
                    'Expecting `dense_` version of `{}` to exist before '
                    'calling `{}` module.'.format(key, self._name))
        return kwargs

    def reset_unset_recommended_keys(self):
        """Null the list of unset recommended keys."""
        self._unset_recommended_keys = set()

    def get_unset_recommended_keys(self):
        """Return list of recommended keys that are not set."""
        return self._unset_recommended_keys
