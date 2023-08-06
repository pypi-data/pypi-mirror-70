"""Definitions for the `Diagonal` class."""
from math import isnan

import numpy as np

from mosfit.modules.arrays.array import Array
from mosfit.utils import flux_density_unit


# Important: Only define one ``Module`` class per file.


class Diagonal(Array):
    """Calculate the diagonal/residuals for a model kernel."""

    MIN_COV_TERM = 1.0e-30

    def __init__(self, **kwargs):
        """Initialize module."""
        super(Diagonal, self).__init__(**kwargs)
        self._observation_types = np.array([])

    def process(self, **kwargs):
        """Process module."""
        self.preprocess(**kwargs)
        self._model_observations = np.copy(kwargs['model_observations'])
        self._model_observations = self._model_observations[self._observed]

        ret = {}

        allowed_otypes = ['countrate', 'magnitude', 'fluxdensity', 'magcount']

        if np.any([x not in allowed_otypes for x in self._o_types]):
            print([x for x in self._o_types if x not in allowed_otypes])
            raise ValueError('Unrecognized observation type.')

        # Calculate (model - obs) residuals.
        residuals = np.array([
            (abs(x - ct) if (not u and ct is not None) or (
                not isnan(x) and ct is not None and x < ct) else 0.0)
            if (t == 'countrate' or t == 'magcount') else
            ((abs(x - y) if (not u and y is not None) or (
                not isnan(x) and y is not None and x < y) else 0.0)
             if t == 'magnitude' else
             ((abs(x - fd) if (not u and fd is not None) or (
                 not isnan(x) and fd is not None and x > fd) else 0.0)
              if t == 'fluxdensity' else None))
            for x, y, ct, fd, u, t in zip(
                self._model_observations, self._mags, self._cts, self._fds,
                self._upper_limits, self._o_types)
        ])

        if np.any(residuals == None):  # noqa: E711
            raise ValueError('Null residual.')

        # Observational errors to be put in diagonal of error matrix.
        diag = [
            ((ctel if (ct is not None and x > ct) else cteu))
            if (t == 'countrate' or t == 'magcount') else
            ((el if (y is None or x > y) else eu))
            if t == 'magnitude' else
            ((fdel if (fd is not None and x > fd) else fdeu))
            if t == 'fluxdensity' else None
            for x, y, eu, el, fd, fdeu, fdel, ct, ctel, cteu, t in zip(
                self._model_observations, self._mags,
                self._e_u_mags, self._e_l_mags, self._fds, self._e_u_fds,
                self._e_l_fds, self._cts, self._e_l_cts, self._e_u_cts,
                self._o_types)
        ]
        diag = [0.0 if x is None else x for x in diag]
        diag = np.array(diag) ** 2

        if np.any(diag == None):  # noqa: E711
            raise ValueError('Null error.')

        ret['kdiagonal'] = diag
        ret['kresiduals'] = residuals

        return ret

    def preprocess(self, **kwargs):
        """Construct arrays of observations based on data keys."""
        otypes = np.array(kwargs.get('observation_types', []))
        if np.array_equiv(
                otypes, self._observation_types) and self._preprocessed:
            return
        self._observation_types = otypes
        self._mags = np.array(kwargs.get('magnitudes', []))
        self._fds = np.array(kwargs.get('fluxdensities', []))
        self._cts = np.array(kwargs.get('countrates', []))
        self._e_u_mags = kwargs.get('e_upper_magnitudes', [])
        self._e_l_mags = kwargs.get('e_lower_magnitudes', [])
        self._e_mags = kwargs.get('e_magnitudes', [])
        self._e_u_fds = kwargs.get('e_upper_fluxdensities', [])
        self._e_l_fds = kwargs.get('e_lower_fluxdensities', [])
        self._e_fds = kwargs.get('e_fluxdensities', [])
        self._u_fds = kwargs.get('u_fluxdensities', [])
        self._e_u_cts = kwargs.get('e_upper_countrates', [])
        self._e_l_cts = kwargs.get('e_lower_countrates', [])
        self._e_cts = kwargs.get('e_countrates', [])
        self._u_cts = kwargs.get('u_countrates', [])
        self._upper_limits = np.array(kwargs.get('upperlimits', []),
                                      dtype=bool)
        self._observed = np.array(kwargs.get('observed', []), dtype=bool)
        self._o_types = self._observation_types[self._observed]

        # Magnitudes first
        # Note: Upper limits (censored data) currently treated as a
        # half-Gaussian, this is very approximate and can be improved upon.
        self._e_u_mags = [
            kwargs['default_upper_limit_error']
            if (e is None and eu is None and self._upper_limits[i]) else
            (kwargs['default_no_error_bar_error']
             if (e is None and eu is None) else (e if eu is None else eu))
            for i, (e, eu) in enumerate(zip(self._e_mags, self._e_u_mags))
        ]
        self._e_l_mags = [
            kwargs['default_upper_limit_error']
            if (e is None and el is None and self._upper_limits[i]) else
            (kwargs['default_no_error_bar_error']
             if (e is None and el is None) else (e if el is None else el))
            for i, (e, el) in enumerate(zip(self._e_mags, self._e_l_mags))
        ]

        # Ignore upperlimits for countrate if magnitude is present.
        self._upper_limits[self._observation_types[
            self._observed] == 'magcount'] = False
        self._e_u_cts = [
            c if (e is None and eu is None) else
            e if eu is None else eu
            for i, (c, e, eu) in enumerate(zip(
                self._cts, self._e_cts, self._e_u_cts))
        ]
        self._e_l_cts = [
            c if (e is None and el is None) else
            e if el is None else el
            for i, (c, e, el) in enumerate(zip(
                self._cts, self._e_cts, self._e_l_cts))
        ]

        # Now flux densities
        self._e_u_fds = [
            v if (e is None and eu is None and self._upper_limits[i]) else
            (v if (e is None and eu is None) else (e if eu is None else eu))
            for i, (e, eu, v) in enumerate(
                zip(self._e_fds, self._e_u_fds, self._fds))
        ]
        self._e_l_fds = [
            0.0 if self._upper_limits[i] else (
                v if (e is None and el is None) else (e if el is None else el))
            for i, (e, el, v) in enumerate(
                zip(self._e_fds, self._e_l_fds, self._fds))
        ]
        self._fds = np.array([
            x / flux_density_unit(y) if x is not None else None
            for x, y in zip(self._fds, self._u_fds)
        ])
        self._e_u_fds = [
            x / flux_density_unit(y) if x is not None else None
            for x, y in zip(self._e_u_fds, self._u_fds)
        ]
        self._e_l_fds = [
            x / flux_density_unit(y) if x is not None else None
            for x, y in zip(self._e_l_fds, self._u_fds)
        ]

        self._preprocessed = True
