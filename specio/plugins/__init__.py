"""

Specio is plugin-based. Every supported format is provided with a
plugin. You can write your own plugins to make specio support
additional formats. And we would be interested in adding such code to the
specio codebase!


What is a plugin
----------------

In specio, a plugin provides one or more :class:`.Format` objects, and
corresponding :class:`.Reader` class.  Each Format object represents an
implementation to read a particular file format. Its Reader classes do the
actual reading.

The reader object has a ``request`` attribute that can be used to obtain
information about the read :class:`.Request`, such as user-provided keyword
arguments, as well get access to the raw image data.


Registering
-----------

Strictly speaking a format can be used stand alone. However, to allow
specio to automatically select it for a specific file, the format must
be registered using ``specio.formats.add_format()``.

Note that a plugin is not required to be part of the specio package; as
long as a format is registered, specio can use it. This makes specio very
easy to extend.


What methods to implement
--------------------------

Specio is designed such that plugins only need to implement a few
private methods. The public API is implemented by the base classes.
In effect, the public methods can be given a descent docstring which
does not have to be repeated at the plugins.

For the Format class, the following needs to be implemented/specified:

  * The format needs a short name, a description, and a list of file
    extensions that are common for the file-format in question.
    These ase set when instantiation the Format object.
  * Use a docstring to provide more detailed information about the
    format/plugin, such as parameters for reading and saving that the user
    can supply via keyword arguments.
  * Implement ``_can_read(request)``, return a bool.
    See also the :class:`.Request` class.

For the Format.Reader class:

  * Implement ``_open(**kwargs)`` to initialize the reader. Deal with the
    user-provided keyword arguments here.
  * Implement ``_close()`` to clean up.
  * Implement ``_get_length()`` to provide a suitable length based on what
    the user expects. Can be ``inf`` for streaming data.
  * Implement ``_get_data(index)`` to return an array and a meta-data dict.
  * Implement ``_get_meta_data(index)`` to return a meta-data dict. If index
    is None, it should return the 'global' meta-data.

"""

from . import csv
from . import example
from . import fsm
from . import mzml
from . import mzxml
from . import sp
from . import spc
