# Fit mixed models to NHANES blood pressure data.  There are two blood
# pressure measurement types (systolic and diastolic), with up to 4
# repeated measures for each type.
#
# https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/BPX_G.XPT
# https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/BMX_G.XPT

import statsmodels.api as sm
import pandas as pd
import numpy as np

# Load and merge the data sets
demog = pd.read_sas("DEMO_G.XPT")
bpx = pd.read_sas("BPX_G.XPT")
bmx = pd.read_sas("BMX_G.XPT")
df = pd.merge(demog, bpx, left_on="SEQN", right_on="SEQN")
df = pd.merge(df, bmx, left_on="SEQN", right_on="SEQN")

# Convert from wide to long
syvars = ["BPXSY%d" % j for j in (1,2,3,4)]
divars = ["BPXDI%d" % j for j in (1,2,3,4)]
vvars = syvars + divars
idvars = ['SEQN', 'RIDAGEYR', 'RIAGENDR', 'BMXBMI']
dx = pd.melt(df, id_vars=idvars, value_vars=vvars,
             var_name='bpvar', value_name='bp')

# A bit of data cleanup
dx = dx.sort_values(by='SEQN')
dx = dx.reset_index(drop=True)
dx['SEQN'] = dx.SEQN.astype(np.int)
dx = dx.dropna()
dx["bpt"] = dx.bpvar.str[3:5]
dx["bpi"] = dx.bpvar.str[5].astype(np.int)
dx["female"] = (dx.RIAGENDR == 2).astype(np.int)

# Fit a misspecified OLS
model1 = sm.OLS.from_formula("bp ~ RIDAGEYR + female + C(bpt) + BMXBMI", dx)
result1 = model1.fit()

# Fit a mixed model to systolic data only with simple random intercept
# per subject (use subset for speed during workshop, full data set
# fits in ~30-40 seconds).  Then calculate ICC.
ds2 = dx.loc[dx.bpt == "SY"]
model2 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + BMXBMI",
                                 groups="SEQN", data=ds2.loc[0:5000,:])
result2 = model2.fit()
icc2 = result2.cov_re / (result2.cov_re + result2.scale)

# Fit a mixed model to diastolic data only with simple random
# intercept per subject (also using subset of data).  Then calculate
# ICC.
ds3 = dx.loc[dx.bpt == "DI"]
model3 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + BMXBMI",
                                 groups="SEQN", data=ds3.loc[0:5000,:])
result3 = model3.fit()
icc3 = result3.cov_re / (result3.cov_re + result3.scale)

# Fit a mixed model to diastolic data only with simple random
# intercept per subject (also using subset of data).
ds3 = dx.loc[dx.bpt == "DI"]
model4 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + BMXBMI + bpi",
                                 groups="SEQN", re_formula="1+bpi",
                                 data=ds3.loc[0:5000,:])
result4 = model4.fit()

# Fit a mixed model to both types of BP with simple random intercept
# per subject.
model5 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + C(bpt) + BMXBMI",
                                 groups="SEQN", data=dx.loc[0:5000,:])
result5 = model5.fit()

# Fit a mixed model to both types of BP with subject random intercept
# and unique random effect per BP type with common variance.
model6 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + C(bpt) + BMXBMI",
                                 groups="SEQN", re_formula="1",
                                 vc_formula={"bpt": "0+C(bpt)"},
                                 data=dx.loc[0:5000,:])
result6 = model6.fit()

# Fit a mixed model to both types of BP with subject random intercept
# and unique random effect per BP type with unique variance.
dx["sy"] = (dx.bpt == "SY").astype(np.int)
dx["di"] = (dx.bpt == "DI").astype(np.int)
model7 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + C(bpt) + BMXBMI",
                                 groups="SEQN", re_formula="1",
                                 vc_formula={"sy": "0+sy", "di": "0+di"},
                                 data=dx.loc[0:5000,:])
result7 = model7.fit()

# Fit a mixed model to both types of BP with subject random intercept
# and unique random effect per BP type with unique variance, and
# heteroscedasticity by BP type.
dx["sy1"] = (dx.bpvar == "BPXSY1").astype(np.int32)
dx["sy2"] = (dx.bpvar == "BPXSY2").astype(np.int32)
dx["sy3"] = (dx.bpvar == "BPXSY3").astype(np.int32)
dx["di1"] = (dx.bpvar == "BPXDI1").astype(np.int32)
dx["di2"] = (dx.bpvar == "BPXDI2").astype(np.int32)
dx["di3"] = (dx.bpvar == "BPXDI3").astype(np.int32)
model8 = sm.MixedLM.from_formula("bp ~ RIDAGEYR + female + C(bpt) + BMXBMI",
                                 groups="SEQN", re_formula="1",
                                 vc_formula={"sy": "0+sy", "di": "0+di", 
                                             "dye": "0+di1+di2+di3"},
                                 data=dx.loc[0:5000,:])
result8 = model8.fit()
