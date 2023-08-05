# Copyright 2017 Virgil Dupras

# This software is licensed under the "BSD" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.hardcoded.net/licenses/bsd_license

from __future__ import unicode_literals

from gi.repository import GObject, Gio
from .exceptions import TrashPermissionError

def send2trash(path):
    try:
        f = Gio.File.new_for_path(path)
        f.trash(cancellable=None)
    except GObject.GError as e:
        if e.code == Gio.IOErrorEnum.NOT_SUPPORTED:
            # We get here if we can't create a trash directory on the same
            # device. I don't know if other errors can result in NOT_SUPPORTED.
            raise TrashPermissionError('')
        raise OSError(e.message)
