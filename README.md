The Annual Social and Economic Survey
=====================================

Initiated by [Alex Golec](http://www.alexgolec.com)

Please direct all productive things (i.e feature requests and bug reports) to
the [github page](http://github.com/alexgolec/march-census-supplement).

Please directly all unproductive things (i.e. love and hate) to
[my email](mailto://alex@alexgolec.com).

Introduction
------------

In addition to the boring old people-counting census, the US census bureau
performs an annual social and economic survey called, intuitively enough, the
Annual Social and Economic Survey.

The raw data for this census is made available in a strange and seemingly
proprietary format. This project aims to reverse-engineer that format, and
provide an straightforward API that could be used to process and manipulate
this interesting dataset.

The Solution
------------

The format is as follows:

* A data file, ending in .dat. This file consists of one line per entry. Each
  line is a densly-packet ASCII record, with no spaces or other delineators.
* A dictionary file, ending in dd.txt, which specifies the names, positions,
  possible value codes, and value code intepretations for the lines in the data
  file.

`TODO:` Continue writing here.
