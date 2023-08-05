# labscript-c-extensions
Contains code for the C extensions used in the labscript suite.

This ensures that developer installs of the main components don't depend on build tools as they can install the prebuilt wheel/conda package containing the extensions.
Only developers of these extensions need the build tools (for example [MSVC++ on Windows](https://wiki.python.org/moin/WindowsCompilers))
