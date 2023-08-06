vNEXT (2020-05-21)
------------------

Bugfixes - NEXT
~~~~~~~~~~~~~~~
- Fix coverage generation in CI - by :user:`gaborbernat`. (`#1551 <https://github.com/tox-dev/tox/issues/1551>`_)
- Fix the CI failures:

  - drop Python 3.5 support as it's not expected to get to a release before EOL,
  - fix test using ``\n`` instead of ``os.linesep``,
  - Windows Python 3.6 does not contain ``_overlapped.ReadFileInto``

  - by :user:`gaborbernat`. (`#1556 <https://github.com/tox-dev/tox/issues/1556>`_)

Improved Documentation - NEXT
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Add base documentation by merging virtualenv structure with tox 3 - by :user:`gaborbernat`. (`#1551 <https://github.com/tox-dev/tox/issues/1551>`_)

