Statsmodels Mixed Linear Models (MixedLM)
=========================================

Linear mixed Models
-------------------

Mixed models are a form of regression model, meaning that the goal is
to relate one _dependent variable_ (also known as the outcome or
response) to one or more _independent variables_ (known as predictors,
covariates, or regressors).  Mixed models are typically used when
there may be statistical dependence among the observations.  More
basic regression procedures like least squares regression and GLM take
the observations to be uncorrelated or independent of each other.

__Terminology:__ The following names are mostly equivalent: mixed
model, mixed effects model, multilevel model, hierarchical model,
random effects model, variance components model.

__Alternatives and related approaches:__ Here we will focus on using
mixed linear models to capture the dependencies among data values.
Other approaches include generalized least squares (GLS), generalized
estimating equations (GEE), fixed effects regression, and marginal
regression.

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
data.  The term "linear" here refers to the fact that the mean
structure is linear in the parameters (b0, b1, b2, b3).  It is not
necessary for the mean structure to be linear in the data, e.g.

E[income | age, school, female] = b0 + b1⋅age + b2⋅age^2 + b3⋅school + b4⋅female

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
measurement taken at one point in time (e.g. triplicate blood pressure
measurements), longitudinal measurements of the same trait taken over
time (e.g. annual BMI measurements taken over several years), or
related traits measured at the same or different times (e.g. hearing
levels in the left and right ear).  When data are collected this way,
it is likely that the measures for a single person are correlated.

Dependent data often arise when taking repeated measurements on each
person, but other grouping variables are also possible.  For example,
we may have test scores on students in a classroom, with the classroom
nested in a school, which in turn is nested in a school district, etc.
The generic terms _cluster variable_ or _grouping variable_ are often
used to refer to whatever is the main unit of analysis on which the
repeated measures are made (people, classrooms, etc.).

Longitudinal data and random coefficients
-----------------------------------------

There are various ways to accommodate correlations in a regression
framework.  The approach taken in mixed modeling is that the
parameters in the regression model are taken to vary from one cluster
to the next.  For example, if we have repeated measures of blood
pressure and age over time within a person, we can regress blood
pressure on age with a _conditionally linear mean structure_ in which
the intercept and slope are subject-specific.  That is, for subject i
we have

SBP(age, i) = a + b⋅age + a(i) + b(i)⋅age(i) + e(age, i)

This model states that for each subject, the blood pressure (SBP)
trends linearly with age, but each subject has their own intercept
a(i) and slope b(i).  These subject-specific parameters modify the
population parameters a and b.

To simplify interpretation, suppose that age is coded as years beyond
age 20.  Then the varying intercepts a(i) represent variation between
people in their blood pressure at age 20, and the varying slopes b(i)
represent variation in the rate at which blood pressure changes
(presumably increases) with respect to age.

In a mixed model, the values of a(i) and b(i) are taken to be random.
Each of these has a variance, e.g. var[a(i)] = v_a, and var[b(i)] =
v_b.  Also, there is a covariance c_ab = cov[a(i), b(i)] between the
parameters.

Suppose the mean trend is b = 0.6, meaning that an average person's
blood pressure increases 6 units (mmHg) per decade.  If the standard
deviation sqrt(v_b) of the random slopes is 0.5, this means that
everyone has their own slope, with around 16% of the population having
a slope greater than 1.1, and 16% of the population having a slope
less than 0.1 (the random effects are taken to be Gaussian, and 32% of
a Gaussian population falls more than 1 standard deviation from the
mean value).

Variance components
-------------------

Above we focused on a setting in which the repeated measures are
predicted by a quantitative variable (age) and are taken over time
within each subject.  A different setting is when the repeated
measures are taken for various grouping variables that may be nested
or crossed.  These are often described as "variance components", but
can also be called "random intercepts" or simply "random effects".

A simple example would be if we had data on body mass index (BMI) for
subjects where we also know their residential location in terms of
neighborhood, city, and state.  The neighborhoods are nested in the
cities, and the cities are nested in the states.  Rather than
estimating a parameter for every level of each of these variables, we
can focus instead on estimating the variance contributed by each level
of the nesting.  A model for this could be

Y(i) = m + N[n(i)] + C[c(i)] + S[s(i)] + e(i)

where Y(i) is the BMI for subject i, m is the population mean, n(i),
c(i), and s(i) are, resepectively, the neighborhood, city, and state
where subject i lives, and N[⋅], C[⋅], S[⋅] are the random effects for
each of these levels.  Suppose that subject i lives in neighborhood
the Burns Park neighborhood of Ann Arbor, Michigan.  Then n(i) = Burns
Park, c(i) = Ann Arbor, s(i) = Michigan.

There are unkown random terms associated with each of these levels,
for example perhaps N[Burns Park] = 1, C[Ann Arbor] = 2, and
S[Michigan] = -1.  This means that people in Burns Park tend to have 1
unit higher BMI than other people in Ann Arbor, people in Ann Arbor
have 2 units higher BMI than other people in Michigan, and people in
Michigan have one unit lower BMI than people in other states.  These
terms add, so that subject i has conditional mean value m + 1 + 2 - 1
= m+2.

In variance components modeling, we don't care much about the specific
random terms associated with each level of each variable.  Instead, we
imagine that all the N[] terms come from a common distribution, say
with mean 0 and variance V_N, all the C[] terms come from a
distribution with mean 0 and variance V_C, and all the S[] terms come
from a distribiution with mean 0 and variance V_S.  Our only goal here
is to estimate V_N, V_C, and V_S, to better understand how the
different levels of geography contribute to the observed value of BMI.
