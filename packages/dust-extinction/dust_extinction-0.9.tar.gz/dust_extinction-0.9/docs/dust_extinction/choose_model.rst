#####################
How to Choose a Model
#####################

The ``dust_extinction`` package provides a suite of dust extinction models.
Which model to use can depend on the wavelength range of interest, the expected
type of extinction, or some other property.

Average Models
==============

Simple Average Curves
---------------------

These are straightforward averages of observed extinction curves.  They are the
simplest models and include models for the MW
(:class:`~dust_extinction.averages.RL85_MWGC`,
:class:`~dust_extinction.averages.I05_MWAvg`,
:class:`~dust_extinction.averages.CT06_MWLoc`,
:class:`~dust_extinction.averages.CT06_MWGC`,
:class:`~dust_extinction.averages.GCC09_MWAvg`,
:class:`~dust_extinction.averages.F11_MWGC`;
Note the different valid wavelength ranges), the LMC
(:class:`~dust_extinction.averages.G03_LMCAvg`,
:class:`~dust_extinction.averages.G03_LMC2`) and the SMC
(:class:`~dust_extinction.averages.G03_SMCBar`).

One often used alternative to these straight average models is to use one of
the parameter dependent models with the average R(V) value.  For the Milky
Way, the usual average used is R(V) = 3.1.

+--------------+-------------+------------------+--------------+
| Model        | x range     | wavelength range |       galaxy |
|              | [1/micron]  | [micron]         |              |
+==============+=============+==================+==============+
| GCC09_MWAvg  | 0.3 - 10.96 |     0.0912 - 3.3 |           MW |
+--------------+-------------+------------------+--------------+
| I05_MWAvg    |  0.13 - 0.8 |      1.24 - 7.76 |           MW |
+--------------+-------------+------------------+--------------+
| CT06_MWLoc   | 0.037 - 0.8 |      1.24 - 27.0 |   MW (Local) |
+--------------+-------------+------------------+--------------+
| RL85_MWGC    |  0.08 - 0.8 |      1.25 - 13.0 | MW (GCenter) |
+--------------+-------------+------------------+--------------+
| CT06_MWGC    | 0.037 - 0.8 |      1.24 - 27.0 | MW (GCenter) |
+--------------+-------------+------------------+--------------+
| F11_MWGC     |  0.05 - 0.8 |      1.28 - 19.1 | MW (GCenter) |
+--------------+-------------+------------------+--------------+
| G03_LMCAvg   |  0.3 - 10.0 |        0.1 - 3.3 |          LMC |
+--------------+-------------+------------------+--------------+
| G03_LMC2     |  0.3 - 10.0 |        0.1 - 3.3 | LMC (30 Dor) |
+--------------+-------------+------------------+--------------+
| G03_SMCBar   |  0.3 - 10.0 |        0.1 - 3.3 |          SMC |
+--------------+-------------+------------------+--------------+


Parameter Dependent Average Curves
----------------------------------

The models that are dependent on parameters provide average curves that account
for overall changes in the extinction curve shapes.  For example, the average
behavior of Milky Way extinction curves has been shown to be dependent on R(V)
= A(V)/E(B-V).  R(V) roughly tracks with the average dust grain size.

The most general model is :class:`~dust_extinction.parameter_averages.G16` as this
model encompasses the average measured behavior of extinction curves in the MW,
LMC, and SMC.  The :class:`~dust_extinction.parameter_averages.G16` model reduces
to the :class:`~dust_extinction.parameter_averages.F99` model with f\ :sub:`A`\ =
1.0.  If only MW type extinction is expected, then the
:class:`~dust_extinction.parameter_averages.F19` model should be considered as it
is based on spectroscopic extinction curves in the optical and ultraviolet and
significantly more extinction curves than the
:class:`~dust_extinction.parameter_averages.CCM89` or
:class:`~dust_extinction.parameter_averages.O94` models.

+----------+-------------+-------------+------------------+--------------+
| Model    | Parameters  | x range     | wavelength range |       galaxy |
|          |             | [1/micron]  | [micron]         |              |
+==========+=============+=============+==================+==============+
| CCM89    |  R(V)       |  0.3 - 10.0 |        0.1 - 3.3 |           MW |
+----------+-------------+-------------+------------------+--------------+
| O94      |  R(V)       |  0.3 - 10.0 |        0.1 - 3.3 |           MW |
+----------+-------------+-------------+------------------+--------------+
| F99, F04 |  R(V)       |  0.3 - 10.0 |        0.1 - 3.3 |           MW |
+----------+-------------+-------------+------------------+--------------+
| VCG04    |  R(V)       |   3.3 - 8.0 |     0.125 - 0.31 |           MW |
+----------+-------------+-------------+------------------+--------------+
| GCC09    |  R(V)       |  3.3 - 11.0 |     0.091 - 0.31 |           MW |
+----------+-------------+-------------+------------------+--------------+
| M14      |  R_5495     |  0.3 -  3.3 |       0.31 - 3.3 |      MW, LMC |
+----------+-------------+-------------+------------------+--------------+
| G16      | R(V)_A, f_A |  0.3 - 10.0 |        0.1 - 3.3 | MW, LMC, SMC |
+----------+-------------+-------------+------------------+--------------+
| F19      |  R(V)       |   0.3 - 8.7 |      0.115 - 3.3 |           MW |
+----------+-------------+-------------+------------------+--------------+

Notes
-----

The :class:`~dust_extinction.parameter_averages.GCC09` model is the only
model that applies all the way to 912 A, but has the limitation that it
only applies to the UV spectral region (not derived in the NIR/Optical).

The :class:`~dust_extinction.parameter_averages.M14` models focus on refining
models in the optical, and use the
:class:`~dust_extinction.parameter_averages.CCM89` models for the NIR and the UV.
The :class:`~dust_extinction.parameter_averages.M14` models use
R_5495 = A(5485)/E(4405-5495), the spectroscopic equivalent to
band-integrated R(V); see the paper for discussion.  Because of a spurious
feature in the near UV caused by smoothly tying their optical to the
:class:`~dust_extinction.parameter_averages.CCM89` UV, only the NIR and
optical portions of the :class:`~dust_extinction.parameter_averages.M14`
models are provided here.

Shape Models
============

The models that focus on describing the full extinction curve shape are usually
used to fit measured extinction curves.  These models allow features in the
extinction curve to be measured (e.g., 2175 A bump or 10 micron silicate
feature).  The :class:`~dust_extinction.shapes.P92` is the most
general as it covers the a very broad wavelength range.  The
:class:`~dust_extinction.shapes.FM90` model has been extensively used,
but only covers the UV wavelength range.

+------------+--------------+------------------+-------------------+
| Model      | x range      | wavelength range | # of parameters   |
|            | [1/micron]   | [micron]         |                   |
+============+==============+==================+===================+
| FM90       | 3.13 - 11.0  |    0.0912 - 0.32 |  6                |
+------------+--------------+------------------+-------------------+
| P92        | 0.001 - 1000 |     0.001 - 1000 |  19 (24 possible) |
+------------+--------------+------------------+-------------------+
