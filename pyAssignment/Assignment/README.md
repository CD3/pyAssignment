The Assignment class is a container for storing assignments, and should be kept simple so that it can easily be reused.
Complex logic, or logic unique to a specific output format (i.e. writing to a LaTeX document) should not be put
into the classes used by an Assignment (i.e. any of the files in in or below this directory). Clients should extend or patch
these classes to support specific features/requirements.
