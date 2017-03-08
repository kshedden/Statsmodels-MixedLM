Statsmodels Mixed Linear Models (MixedLM)
=========================================

Linear mixed Models
-------------------

Mixed models are a form of regression model, meaning that the goal is
to relate one _dependent variable_ (outcome, or response) to one or
more _independent variables_ (predictors, covariates, or regressors).
Mixed models are typically used when there may be statistical
dependence among the observations.  More basic regression procedures
like least squares regression and GLM take the observations to be
uncorrelated or independent of each other.

Mean and variance structure
---------------------------

Many regression models can be interpreted in terms of the way they
specify the _mean structure_ and the _variance structure_.  The mean
structure can be written as E[Y|X], read as "the mean of Y given X".
If your dependent variable is a person's income, and the predictors
are their age, number of years of schooling, and gender, you might
model the mean structure as

E[income | age, school, female] = b0 + b1⋅age + b2⋅school + b3⋅female

This is a _linear mean structure_, which is the mean structure used in
linear regression (e.g. OLS), and in linear mixed models.  The
_parameters_ b0, b1, b2, and b3 are unknown constants to be fit to the
data.

The variance structure can be written as Var[Y|X], read as "the
variance of Y given X".  A very basic variance structure is a constant
or homoscedastic variance structure.  For the income analysis
discussed above, this would mean that

Var[income | age, school, female] = v,

where v is an unkown constant to be fit to the data.

Dependent data
--------------

A common situation in applied research is that several observations
are made on a person.  These might be replicates of the same
measurement taken at one time (e.g. triplicate blood pressure
measurements), longitudinal measurements of the same trait taken over
time (e.g. annual BMI measurements taken over several years), or
related traits measured at the same or different times (e.g. hearing
level in the left and right ear).  When data are collected this way,
it is likely that the measures for a single person are correlated.

Dependent data often arise when taking repeated measurements on each
person, but other grouping variables are also possible.  For example,
we may have test scores on students in a classroom, with the classroom
nested in a school, which in turn is nested in a school district, etc.
The generic terms _cluster variable_ or _grouping variable_ are often
used to refer to whatever is the main unit of analysis on which the
repeated measures are made.

There are various ways to accommodate correlations in a regression
framework.  The approach taken in mixed modeling is that the
parameters in the regression model are taken vary from one cluster to
the next.  For example, if we have repeated measures of blood pressure
and age over time, we can regress blood pressure on age with a
_conditionally linear mean structure_ in which the intercept and slope
are subject-specific.  That is, for subject i we have

SBP(age, i) = a + b*age + a(i) + b(i)*age(i) + e(age, i)

This model states that for each subject, the blood pressure (SBP)
trends linearly with age, but each subject has their own intercept
a(i) and slope b(i).  These subject-specific parameters modify the
population parameters a and b.

To simplify interpretation, suppose that age is coded as years beyond
age 20.  Then the varying intercepts a(i) represent variation in the
population of the blood pressure at age 20, and the varying slopes
b(i) represent variation in the rate at which blood pressure changes
(presumably, increases) with respect to age.

In a mixed model, the values of a(i) and b(i) are taken to be random.
Each of these has a variance, e.g. var[a(i)] = v_a, and var[b(i)] =
v_b.  Also, there is a covariance c_ab = cov[a(i), b(i)] between the
parameters.

Suppose the mean trend is b = 0.6, meaning that an average person's
blood pressure increases 6 units (mm Hg) per decade.  If the standard
deviation sqrt(v_b) of the random slopes is 0.5, this means that
everyone has their own slope, with around 16% of the population having
a slope greater than 1.1, and 16% of the population having a slope
less than 0.1 (since 32% of a Gaussian population falls more than 1
standard deviation from the mean value).

__Terminology:__The following names are mostly equivalent: mixed model, mixed effects
model, multilevel model, hierarchical model, random effects model,
variance components model.

__Alternatives and related approaches:__ Generalized least squares
(GLS), generalized estimating equations (GEE), marginal regression.