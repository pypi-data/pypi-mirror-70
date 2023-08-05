Changelog
=========

master
------

v2.0.0rc2
---------

- (`!45 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/45>`_) Move from `<https://gitlab.com/znicholls/netcdf-scm>`_ to `<https://gitlab.com/netcdf-scm/netcdf-scm>`_
- (`!43 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/43>`_) Add normalisation method ``21-yr-running-mean-dedrift``
- (`!42 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/42>`_) Remove redundant test files (leftover from previous behaviour)
- (`!38 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/38>`_) Split out normalisation module: ``netcdf_scm.normalisation`` (closes `#31 <https://gitlab.com/netcdf-scm/netcdf-scm/-/issues/31>`_)
- (`!39 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/39>`_) Put basic license checking tools in new module: ``netcdf_scm.citing`` (closes `#30 <https://gitlab.com/netcdf-scm/netcdf-scm/-/issues/30>`_)
- (`!37 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/37>`_) Do not duplicate files into a ``flat`` directory when wrangling and stitching (closes `#33 <https://gitlab.com/netcdf-scm/netcdf-scm/-/issues/33>`_)
- (`!36 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/36>`_) Ensure areas are only calculated based on non-masked data (fixes bugs identified in `#35 <https://gitlab.com/netcdf-scm/netcdf-scm/-/issues/35>`_ and `#37 <https://gitlab.com/netcdf-scm/netcdf-scm/-/issues/37>`_)
- (`!34 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/34>`_) Add convenience ``.MAG`` reader (``netcdf_scm.io.load_mag_file``) which automatically fills in metadata. Also adds ``netcdf_scm.io.get_scmcube_helper`` to the 'public' API.
- (`!33 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/33>`_) Fix bug in ``stitching.get_branch_time`` where wrong time units were used when converting raw time to datetime
- (`!31 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/31>`_) Rename ``SCMCube``, it is now ``ScmCube``. Also use "netCDF" rather than "NetCDF" throughout.

v2.0.0rc1
---------

- (`!25 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/25>`_) Add regular test of conda installation
- (`!30 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/30>`_) Added scipy to dependencies to pip install works
- (`!28 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/28>`_) Move multiple stitching utility functions into the 'public' API
- (`!29 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/29>`_) Parallelise directory sorting when crunching
- (`!26 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/26>`_) Added 21-year running mean normalisation option
- (`!27 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/27>`_) Refactored stitching to module to make room for new normalisation method
- (`!22 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/22>`_) Allow user to choose weighting scheme in CLI
- (`!24 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/24>`_) Parallelise unit, integration and regression tests in CI to reduce run time
- (`!23 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/23>`_) Split ``netcdf_scm.cli`` into smaller parts
- (`!21 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/21>`_) Remove use of ``contourf`` in notebooks as it can give odd results
- (`!17 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/17>`_) Add :class:`netcdf_scm.weights.AreaWeightCalculator`
- (`!20 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/20>`_) Update weight retrieval so that non-area weights are normalised (fixes `#11 <https://gitlab.com/netcdf-scm/netcdf-scm/issues/11>`_)
- (`!19 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/19>`_) Update notebooks and refactor so cubes can have multiple weights calculators
- (`!18 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/18>`_) Hotfix tests
- (`!16 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/16>`_) Add CMIP5 stitching support
- (`!15 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/15>`_) Fixed but in unit conversion which caused it to fail for ``hfds``
- (`!14 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/14>`_) Fixed stitching when start year is 1 error (`#15 <https://gitlab.com/netcdf-scm/netcdf-scm/issues/15>`_)
- (`!13 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/13>`_) Make cube concatenation workaround small errors in raw data metadata
- (`!12 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/12>`_) Fixed stitched ``.MAG`` filename bug identified in (`#14 <https://gitlab.com/netcdf-scm/netcdf-scm/issues/14>`_)
- (`!10 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/10>`_) Add support for ``esm*`` experiments when stitching (fixes `#2 <https://gitlab.com/netcdf-scm/netcdf-scm/issues/2>`_)
- (`!11 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/11>`_) Add ability to read CanESM5 ocean data with depth and 'extra' co-ordinates. Also:

    - split regression testing into smaller pieces so memory requirements aren't so high

- (`!9 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/9>`_) Add ability to read CanESM5 ocean data, making handling of 'extra' co-ordinates more robust
- (`!8 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/8>`_) Add process id to logging calls (fixes `#13 <https://gitlab.com/netcdf-scm/netcdf-scm/issues/13>`_)
- (`!6 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/6>`_) Allow hfds crunching to work by handling extra ocean data coordinates properly
- (`!1 <https://gitlab.com/netcdf-scm/netcdf-scm/merge_requests/1>`_) Add ``netcdf-scm-stitch`` so e.g. historical and scenario files can be joined and also normalised against e.g. piControl

Before this point we were on GitHub, not GitLab

- (`#114 (github) <https://github.com/znicholls/netcdf-scm/pull/114>`_) Ensure that default sftlf file is included in wheel
- (`#111 (github) <https://github.com/znicholls/netcdf-scm/pull/111>`_) Write tuningstrucs with data in columns rather than rows
- (`#108 (github) <https://github.com/znicholls/netcdf-scm/pull/108>`_) Optimise wranglers and add regression tests
- (`#107 (github) <https://github.com/znicholls/netcdf-scm/pull/107>`_) Add wrangling options for average/point start/mid/end year time manipulations for ``.MAG`` and ``.IN`` files
- (`#106 (github) <https://github.com/znicholls/netcdf-scm/pull/106>`_) Upgrade to new Pymagicc release
- (`#105 (github) <https://github.com/znicholls/netcdf-scm/pull/105>`_) Upgrade to new Pylint release
- (`#104 (github) <https://github.com/znicholls/netcdf-scm/pull/104>`_) Allow wranglers to also handle unit conversions (see `#101 (github) <https://github.com/znicholls/netcdf-scm/pull/101>`_)
- (`#102 (github) <https://github.com/znicholls/netcdf-scm/pull/102>`_) Keep effective area as metadata when calculating SCM timeseries (see `#100 (github) <https://github.com/znicholls/netcdf-scm/pull/100>`_)
- (`#99 (github) <https://github.com/znicholls/netcdf-scm/pull/99>`_) Switch to BSD-3-Clause license
- (`#98 (github) <https://github.com/znicholls/netcdf-scm/pull/98>`_) Add support for reading CMIP6 concentration GMNHSH data
- (`#97 (github) <https://github.com/znicholls/netcdf-scm/pull/97>`_) Add support for tuningstruc data which has been transposed
- (`#95 (github) <https://github.com/znicholls/netcdf-scm/pull/95>`_) Add support for CO2 flux data (fgco2) reading, in the process simplifying crunching and improving lazy weights
- (`#92 (github) <https://github.com/znicholls/netcdf-scm/pull/92>`_) Shrink test files (having moved entire repository to use git lfs properly)
- (`#90 (github) <https://github.com/znicholls/netcdf-scm/pull/90>`_) Rely on iris for lazy crunching
- (`#89 (github) <https://github.com/znicholls/netcdf-scm/pull/89>`_) Change crunching thresholds to be based on data size rather than number of years
- (`#88 (github) <https://github.com/znicholls/netcdf-scm/pull/88>`_) Fix bug when reading more than one multi-dimensional file in a directory
- (`#87 (github) <https://github.com/znicholls/netcdf-scm/pull/87>`_) Add support for crunching data with a height co-ordinate
- (`#84 (github) <https://github.com/znicholls/netcdf-scm/pull/84>`_) Add ability to crunch land, ocean and atmosphere data separately (and sensibly)
- (`#82 (github) <https://github.com/znicholls/netcdf-scm/pull/82>`_) Prepare to add land data handling
- (`#81 (github) <https://github.com/znicholls/netcdf-scm/pull/81>`_) Refactor masks to use weighting instead of masking, doing all the renaming in the process
- (`#80 (github) <https://github.com/znicholls/netcdf-scm/pull/80>`_) Refactor to avoid ``import conftest`` in tests
- (`#77 (github) <https://github.com/znicholls/netcdf-scm/pull/77>`_) Refactor ``netcdf_scm.masks.get_area_mask`` logic to make multi-dimensional co-ordinate support easier
- (`#75 (github) <https://github.com/znicholls/netcdf-scm/pull/75>`_) Check ``land_mask_threshold`` is sensible when retrieving land mask (automatically update if not)
- (`#72 (github) <https://github.com/znicholls/netcdf-scm/pull/72>`_) Monkey patch iris to speed up crunching and go back to linear regridding of default sftlf mask
- (`#74 (github) <https://github.com/znicholls/netcdf-scm/pull/74>`_) Fix bug in mask generation
- (`#70 (github) <https://github.com/znicholls/netcdf-scm/pull/70>`_) Dynamically decide whether to handle data lazily (fix regression tests in process)
- (`#69 (github) <https://github.com/znicholls/netcdf-scm/pull/69>`_) Add El Nino 3.4 mask
- (`#67 (github) <https://github.com/znicholls/netcdf-scm/pull/67>`_) Fix crunching filenaming, tidy up more and add catch for IPSL ``time_origin`` time variable attribute
- (`#66 (github) <https://github.com/znicholls/netcdf-scm/pull/66>`_) Add devops tools and refactor to pass new standards
- (`#64 (github) <https://github.com/znicholls/netcdf-scm/pull/64>`_) Update logging to make post analysis easier and output clearer
- (`#63 (github) <https://github.com/znicholls/netcdf-scm/pull/63>`_) Switch to using cmor name for variable in SCM timeseries output and put standard name in standard_variable_name
- (`#62 (github) <https://github.com/znicholls/netcdf-scm/pull/62>`_) Add netcdf-scm format and crunch to this by default
- (`#61 (github) <https://github.com/znicholls/netcdf-scm/pull/61>`_) Add land fraction when crunching scm timeseries cubes
- (`#58 (github) <https://github.com/znicholls/netcdf-scm/pull/58>`_) Lock tuningstruc wrangling so it can only wrangle to flat tuningstrucs, also includes:

    - turning off all wrangling in preparation for re-doing crunching format
    - adding default sftlf cube

- (`#55 (github) <https://github.com/znicholls/netcdf-scm/pull/55>`_) Hotfix docs so they build properly
- (`#50 (github) <https://github.com/znicholls/netcdf-scm/pull/50>`_) Make pyam-iamc a core dependency

v1.0.0
------

- (`#49 (github) <https://github.com/znicholls/netcdf-scm/pull/49>`_) Make bandit only check ``src``
- (`#48 (github) <https://github.com/znicholls/netcdf-scm/pull/48>`_) Add ``isort`` to checks
- (`#47 (github) <https://github.com/znicholls/netcdf-scm/pull/47>`_) Add regression tests on crunching output to ensure stability. Also:

    - fixes minor docs bug
    - updates default regexp option in crunch and wrangle to avoid ``fx`` files
    - refactors ``cli.py`` a touch to reduce duplication
    - avoids ``collections`` deprecation warning in ``mat4py``


- (`#46 (github) <https://github.com/znicholls/netcdf-scm/pull/46>`_) Fix a number of bugs in ``netcdf-scm-wrangle``'s data handling when converting to tuningstrucs
- (`#45 (github) <https://github.com/znicholls/netcdf-scm/pull/45>`_) Refactor the masking of regions into a module allowing for more regions to be added as needed

v0.7.3
------

- (`#44 (github) <https://github.com/znicholls/netcdf-scm/pull/44>`_) Speed up crunching by forcing data to load before applying masks, not each time a mask is applied

v0.7.2
------

- (`#43 (github) <https://github.com/znicholls/netcdf-scm/pull/43>`_) Speed up crunching, in particular remove string parsing to convert cftime to python datetime

v0.7.1
------

- (`#42 (github) <https://github.com/znicholls/netcdf-scm/pull/42>`_) Add ``netcdf-scm-wrangle`` command line interface
- (`#41 (github) <https://github.com/znicholls/netcdf-scm/pull/41>`_) Fixed bug in path handling of ``CMIP6OutputCube``

v0.6.2
------

- (`#39 (github) <https://github.com/znicholls/netcdf-scm/pull/39>`_) Add ``netcdf-scm-crunch`` command line interface

v0.6.1
------

- (`#40 (github) <https://github.com/znicholls/netcdf-scm/pull/40>`_) Upgrade to pyam v0.2.0
- (`#38 (github) <https://github.com/znicholls/netcdf-scm/pull/38>`_) Update to using openscm releases and hence drop Python3.6 support
- (`#37 (github) <https://github.com/znicholls/netcdf-scm/pull/37>`_) Adjusted read in of gregorian with 0 reference to give all data from year 1 back
- (`#35 (github) <https://github.com/znicholls/netcdf-scm/pull/35>`_) Fixed bug which prevented SCMCube from crunching to scm timeseries with default earth radius when areacella cube was missing
- (`#34 (github) <https://github.com/znicholls/netcdf-scm/pull/34>`_) Move to new openscm naming i.e. returning ScmDataFrame rather than OpenSCMDataFrameBase
- (`#32 (github) <https://github.com/znicholls/netcdf-scm/pull/32>`_) Move to returning OpenSCMDataFrameBase rather than pandas DataFrame when crunching to scm format
- (`#29 (github) <https://github.com/znicholls/netcdf-scm/pull/29>`_) Fixed bug identified in `#30 (github) <https://github.com/znicholls/netcdf-scm/issues/30>`_
- (`#29 (github) <https://github.com/znicholls/netcdf-scm/pull/29>`_) Put crunching script into formal testsuite which confirms results against KNMI data available `here <https://climexp.knmi.nl/cmip5_indices.cgi?id=someone@somewhere>`_, however no docs or formal example until `#6 (github) <https://github.com/znicholls/netcdf-scm/issues/6>`_ is closed
- (`#28 (github) <https://github.com/znicholls/netcdf-scm/pull/28>`_) Added cmip5 crunching script example, not tested so use with caution until `#6 (github) <https://github.com/znicholls/netcdf-scm/issues/6>`_ is closed

v0.5.1
------

- (`#26 (github) <https://github.com/znicholls/netcdf-scm/pull/26>`_) Expose directory and filename parsers directly


v0.4.3
------

- Move ``import cftime`` into same block as iris imports


v0.4.2
------

- Update ``setup.py`` to install dependencies so that non-Iris dependent functionality can be run from a pip install


v0.4.1
------

- (`#23 (github) <https://github.com/znicholls/netcdf-scm/pull/23>`_) Added ability to handle cubes with invalid calendar (e.g. CMIP6 historical concentrations cubes)
- (`#20 (github) <https://github.com/znicholls/netcdf-scm/pull/20>`_) Added ``CMIP6Input4MIPsCube`` and ``CMIP6OutputCube`` which add compatibility with CMIP6 data


v0.3.1
------

- (`#17 (github) <https://github.com/znicholls/netcdf-scm/pull/17>`_) Update to crunch global and hemispheric means even if land-surface fraction data is missing
- (`#16 (github) <https://github.com/znicholls/netcdf-scm/pull/16>`_) Tidy up experimental crunching script
- (`#15 (github) <https://github.com/znicholls/netcdf-scm/pull/15>`_) Add ability to load from a directory with data that is saved in multiple timeslice files, also adds:

    - adds regular expressions section to development part of docs
    - adds an example script of how to crunch netCDF files into SCM csvs

- (`#14 (github) <https://github.com/znicholls/netcdf-scm/pull/14>`_) Streamline install process
- (`#13 (github) <https://github.com/znicholls/netcdf-scm/pull/13>`_) Add ``load_from_path`` method to ``SCMCube``
- (`#12 (github) <https://github.com/znicholls/netcdf-scm/pull/12>`_) Update to use output format that is compatible with pyam
- Update ``netcdftime`` to ``cftime`` to track name change
- (`#10 (github) <https://github.com/znicholls/netcdf-scm/pull/10>`_) Add land/ocean and hemisphere splits to ``_get_scm_masks`` outputs


v0.2.4
------

- Include simple tests in package


v0.2.3
------

- Include LICENSE in package


v0.2.2
------

- Add conda dev environment details


v0.2.1
------

- Update setup.py to reflect actual supported python versions


v0.2.0
------

- (`#4 (github) <https://github.com/znicholls/netcdf-scm/pull/4>`_) Add work done elsewhere previously
    - ``SCMCube`` base class for handling netCDF files
        - reading, cutting and manipulating files for SCM use
    - ``MarbleCMIP5Cube`` for handling CMIP5 netCDF files within a particular directory structure
    - automatic loading and use of surface land fraction and cell area files
    - returns timeseries data, once processed, in pandas DataFrames rather than netCDF format for easier use
    - demonstration notebook of how this first step works
    - CI for entire repository including notebooks
    - automatic documentation with Sphinx


v0.0.1
------

- initial release


v0.0
----

- dummy release
