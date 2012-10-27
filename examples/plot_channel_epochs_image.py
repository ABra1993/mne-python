"""
=========================================
Visualize channel over epochs as an image
=========================================

This will produce what is sometimes called an event related
potential / field (ERP/ERF) image.

It is also demonstrated how to reorder the epochs using a 1d spectral
embedding as described in:

Graph-based variability estimation in single-trial event-related neural
responses A. Gramfort, R. Keriven, M. Clerc, 2010,
Biomedical Engineering, IEEE Trans. on, vol. 57 (5), 1051-1061
http://hal.inria.fr/inria-00497023
"""
print __doc__

# Authors: Alexandre Gramfort <gramfort@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

import numpy as np
import pylab as pl

import mne
from mne import fiff
from mne.datasets import sample
data_path = sample.data_path('.')

###############################################################################
# Set parameters
raw_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw.fif'
event_fname = data_path + '/MEG/sample/sample_audvis_filt-0-40_raw-eve.fif'
event_id, tmin, tmax = 1, -0.2, 0.5

# Setup for reading the raw data
raw = fiff.Raw(raw_fname)
events = mne.read_events(event_fname)

# Set up pick list: EEG + MEG - bad channels (modify to your needs)
raw.info['bads'] = ['MEG 2443', 'EEG 053']
picks = fiff.pick_types(raw.info, meg='grad', eeg=False, stim=True, eog=True,
                            exclude=raw.info['bads'])

# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                    picks=picks, baseline=(None, 0), preload=True,
                    reject=dict(grad=4000e-13, eog=150e-6))

###############################################################################
# Show event related fields images

# and order with spectral reordering
# If you don't have scikit-learn installed set order_func to None
from sklearn.cluster.spectral import spectral_embedding


def order_func(times, data):
    this_data = data[:, (times > 0.0) & (times < 0.350)]
    return np.argsort(spectral_embedding(np.corrcoef(this_data),
                      n_components=1, random_state=0)).ravel()

good_pick = 97  # channel with a clear evoked response
bad_pick = 98  # channel with no evoked response

pl.close('all')
mne.viz.plot_image_epochs(epochs, [good_pick, bad_pick], sigma=0.5, vmin=-100,
                    vmax=250, colorbar=True, order=order_func, show=True)
