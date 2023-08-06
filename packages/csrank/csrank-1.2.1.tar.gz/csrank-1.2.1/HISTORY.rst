=======
History
=======

Unreleased
------------------

No changes yet.

1.2.1 (2020-06-08)
------------------

* Make all our optional dependencies mandatory to work around a bug in our
  optional imports code. Without this, an exception is raised on import.
  A proper fix will follow.

1.2.0 (2020-06-05)
------------------

* Change public interface of the learners to be more in line with the
  scikit-learn interface (ongoing). As part of these changes, it is no longer
  required to explicitly pass the data dimensionality to the learners on
  initialization.
* Rewrite and document normalized discounted cumulative gain (ndcg) metric to
  fix numerical issues.
  See `#32 <https://github.com/kiudee/cs-ranking/issues/32>`__ for details.
* Fix passing fit keyword arguments on to the core network in
  ``FATEChoiceFunction``.
* Fix arguments for ``AllPositive`` baseline.
* Raise ValueError rather than silently using a default value for unknown
  passed arguments.
* Internal efforts to increase code quality and make use of linting
  (``black``, ``flake8``, ``doc8``).
* Remove old experimental code.

1.1.0 (2020-03-19)
------------------

* Add the expected reciprocal rank (ERR) metric.
* Fix bug in callbacks causing the wrong learning rate schedule to be applied.
* Make csrank easier to install by making some dependencies optional.
* Add guidelines for how to contribute to the project.

1.0.2 (2020-02-12)
------------------

* Fix deployment to GH-pages

1.0.1 (2020-02-03)
------------------

* Add ``HISTORY.rst`` file to track changes over time
* Set up travis-ci for deployment to PyPi

1.0.0 (2018-03-05)
------------------

* Initial release
