Mixed Linear Models (MixedLM) in Python Statsmodels
===================================================

Linear mixed Models
-------------------

Mixed models are a form of regression model, meaning that the goal is
to relate one _dependent variable_ (also known as the outcome or
response) to one or more _independent variables_ (known as predictors,
covariates, or regressors).  Mixed models are typically used when
there may be statistical dependencies among the observations.  More
basic regression procedures like least squares regression and GLM take
the observations to be uncorrelated or independent of each other.
Although it is sometimes possible to use OLS or GLM with dependent
data, usually an alternative approach that explicitly accounts for the
dependence is a better choice

__Terminology:__ The following terms are mostly equivalent: mixed
model, mixed effects model, multilevel model, hierarchical model,
random effects model, variance components model.

__Alternatives and related approaches:__ Here we focus on using mixed
linear models to capture dependencies among data values.  Other
approaches include generalized least squares (GLS), generalized
estimating equations (GEE), fixed effects regression, and marginal
regression.

__Nonlinear mixed models:__ Here we only consider linear mixed models.
Generalized linear and non-linear mixed effects models also exist, but
are not currently available in Python Statsmodels.

Mean and variance structure
---------------------------

Many regression approaches can be interpreted in terms of the way that
they specify the _mean structure_ and the _variance structure_.  The
mean structure can be written as E[Y|X], read as "the mean of Y given
X".  For example, if your dependent variable is a person's income, and
the predictors are their age, number of years of schooling, and
gender, you might model the mean structure as

E[income | age, school, female] = b0 + b1⋅age + b2⋅school + b3⋅female.

This is a _linear mean structure_, which is the mean structure used in
linear regression (e.g. OLS), and in linear mixed models.  The
_parameters_ b0, b1, b2, and b3 are unknown constants to be fit to the
data.  The term "linear" here refers to the fact that the mean
structure is linear in the parameters (b0, b1, b2, b3).  It is not
necessary for the mean structure to be linear in the data, e.g. we
could have specified the mean structure as

E[income | age, school, female] = b0 + b1⋅age + b2⋅age^2 + b3⋅school + b4⋅female

The variance structure can be written as Var[Y|X], and is read as "the
variance of Y given X".  A very basic variance structure is a constant
or homoscedastic variance structure.  For the income analysis
discussed above, this would mean that

Var[income | age, school, female] = v,

where v is an unkown constant to be fit to the data.

In the context of mixed models, the mean and variance and variance
structures defined here are often referred to as the _marginal mean
structure_ and _marginal variance structure_, for reasons that will be
explained further below.

Dependent data
--------------

A common situation in applied research is that several observations
are made on each person in a sample.  These might be replicates of the
same measurement taken at one point in time (e.g. triplicate blood
pressure measurements), longitudinal measurements of the same trait
taken over time (e.g. annual BMI measurements taken over several
years), or related traits measured at the same or different times
(e.g. hearing levels in the left and right ear).  When data are
collected this way, it is likely that the measures for a single person
are correlated.

Dependent data often arise when taking repeated measurements on each
person, but other grouping variables are also possible.  For example,
we may have test scores on students in a classroom, with the classroom
nested in a school, which in turn is nested in a school district, etc.
In this case, the students in one classroom (or school, etc.) may tend
to score higher, or lower than students in other classrooms or
schools.  This is also a form of statistical dependence.  The generic
terms _cluster variable_ or _grouping variable_ are often used to
refer to whatever is the main unit of analysis on which the repeated
measures are made (people, classrooms, etc.).

Longitudinal data and random coefficients
-----------------------------------------

There are various ways to accommodate correlations in a regression
framework.  In mixed modeling, the parameters in the regression model
are taken to vary from one cluster to the next.  For example, if we
have repeated measures of blood pressure and age over time within a
person, we can regress blood pressure on age using a _conditionally
linear mean structure_ in which the intercept and slope are
subject-specific.  That is, for subject i we have

E[SBP(age, i) | a(i), b(i)] = a + b⋅age + a(i) + b(i)⋅age(i)

This model states that for each subject, the blood pressure (SBP)
trends linearly with age, but each subject has their own intercept
a(i) and slope b(i).  These subject-specific parameters modify the
population parameters a and b, i.e. the overall intercept for subject
i is a + a(i), and the overall slope is b + b(i).

The model above is expressed in conditional mean form.  Alternatively,
it may be expressed as a fully generative model

SBP(age, i) = a + b⋅age + a(i) + b(i)⋅age(i) + e(age, i),

where e(age, i) are independent "errors", which represent unexplained
or unstructured variation.

To simplify interpretation, suppose that age is coded as years beyond
age 20.  Then the varying intercepts a(i) represent variation between
people in their blood pressure at age 20, and the varying slopes b(i)
represent variation in the rate at which blood pressure changes with
respect to age.

In a mixed model, the values of a(i) and b(i) are taken to be random.
Each of these has a variance, e.g. var[a(i)] = v_a, and var[b(i)] =
v_b.  Also, there is a covariance c_ab = cov[a(i), b(i)] between the
parameters.

As a concrete numerical example, suppose the mean trend is b = 0.6,
meaning that an average person's blood pressure increases 6 units (mm
Hg) per decade.  If the standard deviation sqrt(v_b) of the random
slopes is 0.5, this means that everyone has their own slope, with
around 16% of the population having a slope greater than 0.6+0.5 =
1.1, and 16% of the population having a slope less than 0.6-0.5 = 0.1
(the random effects are taken to be Gaussian, and 32% of a Gaussian
population falls more than 1 standard deviation from the mean value).

Nested variance components
--------------------------

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
of the nesting.  A model for these data could be

Y(i) = m + N[n(i)] + C[c(i)] + S[s(i)] + e(i)

where Y(i) is the BMI for subject i, m is the population mean, n(i),
c(i), and s(i) are, resepectively, the neighborhood, city, and state
where subject i lives, and N[⋅], C[⋅], S[⋅] are the random effects for
each of these levels.  Suppose that subject i lives in the Burns Park
neighborhood of Ann Arbor, Michigan.  Then n(i) = Burns Park, c(i) =
Ann Arbor, and s(i) = Michigan.

There are unkown random terms associated with each of these levels,
for example perhaps N[Burns Park] = 1, C[Ann Arbor] = 2, and
S[Michigan] = -1.  This means that people in Burns Park tend to have 1
unit higher BMI than other people in Ann Arbor, people in Ann Arbor
have 2 units higher BMI than other people in Michigan, and people in
Michigan have one unit lower BMI than people in other states.  These
terms combine additively, so that subject i has conditional mean value
m + 1 + 2 - 1 = m+2.

In variance components modeling, we don't care much about the specific
random terms associated with each level of each variable.  Instead, we
imagine that all the N[] terms come from a common distribution, say
with mean 0 and variance V_N, all the C[] terms come from a
distribution with mean 0 and variance V_C, and all the S[] terms come
from a distribution with mean 0 and variance V_S.  Our only goal here
is to estimate V_N, V_C, and V_S, to better understand how the
different levels of geography contribute to the observed value of BMI.

Crossed variance components
---------------------------

Variance components can also be crossed.  Fitting this type of model
puts more stress on the software, but it can be done if there aren't
too many levels of crossing.  Suppose for example that we have the
number of emails sent among people in a sample.  For simplicity, we
model these counts with a Gaussian distribution so we can use linear
mixed models.  We can imagine that each person has a propensity A[] to
send emails, and also a propensity B[] to receive emails.  A simple
additive variance component would be

Y(i,j) = m + A[i] + B[j] + e(i, j),

where Y(i, j) is the number of emails sent from subject i to subject
j.  The random effect A[i] reflects person i's propensity to send
emails, and B[j] represents person j's propensity to receive emails.
These random effects are crossed, meaning that any of the A[] terms
can occur in combination with any of the B[] terms.  As above, we are
mainly interested in the variance parameters V_a and V_b, describing,
respectively, the variation in the population of email sending and
email receiving propensities.

More general model formulations
-------------------------------

Above we gave examples of longitudinal, purely nested, and purely
crossed mixed models.  In general, a mixed model can have any
combination of terms of various types (hence the term "mixed" which
may refer to the presence of fixed effects and random effects in the
same model, although this term may also refer to the technical fact
that the marginal distributions in a mixed model can be represented as
infinite mixtures).

The notion of a mixed model is very broad and there is no formal
definition of exactly what scope of models falls into this class.
Certain types of time series models, spatial-temporal models, and
structural-equation models can be viewed as mixed models.

Parameters and random effects
-----------------------------

Python Statsmodels uses maximum likelihood (or restricted maximum
likelihood, the difference is not important here) to fit mixed models
to data.  This means that we are optimizing the parameter values in a
class of parametric models to best fit the data.  The random effects,
e.g. a(i) or N[] above, are random but not observed.  We therefore
marginalize them out of the model's likelihood function before fitting
to the data.  This means that the fitting process does not directly
involve these random effects, although it does involve the parameters
defining the distribution of random effects.

The parameters in a mixed model can broadly be considered as being one
of the following types:

* Mean structure parameters: this includes regression intercepts and
  slopes.  These parameters determine the marginal mean structure
  (defined above) but are not sufficient to describe the conditional
  mean structure, which also depends on a subject's random effects.
  These parameters are sometimes called "fixed effects" because they
  describe the marginal trends in the population, not the unique
  trends for individual subjects.

* Variance structure parameters: this includes variances of random
effects, and covariance parameters describing how various random
effects are correlated.  These are structural parameters describing
how the random effects are distributed, not the random effects
themselves.

In the longitudinal mixed model

E[SBP(age, i) | a(i), b(i)] = a + b⋅age + a(i) + b(i)⋅age(i)

a and b are mean structure parameters (fixed effects), and V_a, V_b,
and C_ab are variance structure parameters, along with the "error
variance" V[SBP(age, i) | a(i), b(i)].  The a(i) and b(i) are the
actual random effects.

In the nested variance components model

Y(i) = m + N[n(i)] + C[c(i)] + S[s(i)] + e(i)

the only mean structure parameter is m.  The variance structure
parameters are V_n, V_c, V_s, and the error variance (in a variance
components model the random effects are independent within and between
levels, so there are no covariance parameters).

In the crossed variance components model

Y(i,j) = m + A[i] + B[j] + e(i, j),

the mean structure parameter is m, and the variance structure
parameters are V_a, V_b, and the error variance (again there are no
covariance parameters).

Software and algorithms
-----------------------

Estimation routines for linear mixed models are much more challenging
to implement than routines for fitting more basic regression
approaches such as OLS and GLM.  However a series of developments in
the past 20 years has led to algorithms that are reasonably fast and
stable.  Statsmodels utilizes many of these best practices, such as
internally re-parameterizing the covariance parameters through their
Choleky factor, and profiling out certain parameters during the
estimation process.

The earlier specifications of linear models were explicitly
group-based.  This means that there was some grouping variable such as
a person, such that observations made on different groups are taken to
be independent.  Many applications of mixed modeling are compatible
with this group-based approach.  One exception is heavily crossed
models that are widely used in, for example, experimental psychology
and linguistics.

Recent versions of R's LMER have taken a somewhat different
algorithmic approach, utilizing the "sparse Cholesky factorization".
Statsmodels does not use this approach, partly because the sparse
Cholesky code is not available with a Python-compatible license.  The
sparse Chleksy approach may be somewhat more efficient for handling
large crossed models as noted above.  However Python Statsmodels does
use sparse matrices and exploits some matrix factorizations to allow
crossed models to be fit.

Another important disctinction between Python Statsmodels and LMER in
R (which is the most mature open-source implementation of mixed
models) is that the Statsmodels code is written in Python, whereas
LMER is mostly written in C that is then linked to R.  The Python
MixedLM code makes use of advanced Numpy and Scipy techniques (which
are written in C) and therefore the distinction is not as clear as it
may at first seem.  There are many trade-offs in this decision, but at
present the Python code generally runs somewhat slower than LMER.
There are many innovations underway to accelerate numerical Python
code so it is likely that the Statsmodels code will become faster over
time.