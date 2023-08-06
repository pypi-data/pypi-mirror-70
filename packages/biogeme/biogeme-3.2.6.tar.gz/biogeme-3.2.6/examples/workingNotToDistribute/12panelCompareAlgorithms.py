"""File 12panelCompareAlgorithms.py

:author: Michel Bierlaire, EPFL
:date: Sun Sep  8 18:55:38 2019

 Example of a mixture of logit models, using Monte-Carlo integration.
 The datafile is organized as panel data.
 Three alternatives: Train, Car and Swissmetro
 SP data
"""
from datetime import datetime
import numpy as np
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
import biogeme.optimization as opt
from biogeme.expressions import Beta, DefineVariable, bioDraws, PanelLikelihoodTrajectory, MonteCarlo, log

# Read the data
df = pd.read_csv("swissmetro.dat",sep='\t')
database = db.Database("swissmetro",df)

# They are organized as panel data. The variable ID identifies each individual.
database.panel("ID")

# The Pandas data structure is available as database.data. Use all the
# Pandas functions to invesigate the database
#print(database.data.describe())

# The following statement allows you to use the names of the variable
# as Python variable.
globals().update(database.variables)

# Removing some observations can be done directly using pandas.
#remove = (((database.data.PURPOSE != 1) & (database.data.PURPOSE != 3)) | (database.data.CHOICE == 0))
#database.data.drop(database.data[remove].index,inplace=True)

# Here we use the "biogeme" way for backward compatibility
exclude = (( PURPOSE != 1 ) * (  PURPOSE   !=  3  ) +  ( CHOICE == 0 )) > 0
database.remove(exclude)

# Parameters to be estimated
ASC_CAR = Beta('ASC_CAR',0,None,None,0)
ASC_TRAIN = Beta('ASC_TRAIN',0,None,None,0)
ASC_SM = Beta('ASC_SM',0,None,None,1)
B_TIME = Beta('B_TIME',0,None,None,0)
B_COST = Beta('B_COST',0,None,None,0)
B_TIME_S = Beta('B_TIME_S',0,None,None,0)

# Define a random parameter, normally distributed across individuals,
# designed to be used for Monte-Carlo simulation
B_TIME_RND = B_TIME + B_TIME_S * bioDraws('B_TIME_RND','NORMAL')

# Definition of new variables
SM_COST =  SM_CO   * (  GA   ==  0  ) 
TRAIN_COST =  TRAIN_CO   * (  GA   ==  0  )

# Definition of new variables: adding columns to the database 
TRAIN_TT_SCALED = DefineVariable('TRAIN_TT_SCALED',\
                                 TRAIN_TT / 100.0,database)
TRAIN_COST_SCALED = DefineVariable('TRAIN_COST_SCALED',\
                                   TRAIN_COST / 100,database)
SM_TT_SCALED = DefineVariable('SM_TT_SCALED', SM_TT / 100.0,database)
SM_COST_SCALED = DefineVariable('SM_COST_SCALED', SM_COST / 100,database)
CAR_TT_SCALED = DefineVariable('CAR_TT_SCALED', CAR_TT / 100,database)
CAR_CO_SCALED = DefineVariable('CAR_CO_SCALED', CAR_CO / 100,database)

# Definition of the utility functions
V1 = ASC_TRAIN + \
     B_TIME_RND * TRAIN_TT_SCALED + \
     B_COST * TRAIN_COST_SCALED
V2 = ASC_SM + \
     B_TIME_RND * SM_TT_SCALED + \
     B_COST * SM_COST_SCALED
V3 = ASC_CAR + \
     B_TIME_RND * CAR_TT_SCALED + \
     B_COST * CAR_CO_SCALED

# Associate utility functions with the numbering of alternatives
V = {1: V1,
     2: V2,
     3: V3}

# Associate the availability conditions with the alternatives
CAR_AV_SP =  DefineVariable('CAR_AV_SP',CAR_AV  * (  SP   !=  0  ),database)
TRAIN_AV_SP =  DefineVariable('TRAIN_AV_SP',TRAIN_AV  * (  SP   !=  0  ),database)
av = {1: TRAIN_AV_SP,
      2: SM_AV,
      3: CAR_AV_SP}

# Conditional to B_TIME_RND, the likelihood of one observation is
# given by the logit model (called the kernel)
obsprob = models.logit(V,av,CHOICE)

# Conditional to B_TIME_RND, the likelihood of all observations for
# one individual (the trajectory) is the product of the likelihood of
# each observation.
condprobIndiv = PanelLikelihoodTrajectory(obsprob)

# We integrate over B_TIME_RND using Monte-Carlo
logprob = log(MonteCarlo(condprobIndiv))

# Define level of verbosity
import biogeme.messaging as msg
logger = msg.bioMessage()
#logger.setSilent()
#logger.setWarning()
#logger.setGeneral()
logger.setDetailed()
#logger.setDebug()

# Create the Biogeme object
biogeme  = bio.BIOGEME(database,logprob,numberOfDraws=1000)

# Estimate the parameters. 

allResults = {}

for alpha in np.arange(0.0, 1.0, 0.1):
    biogeme.modelName = f'12panel_{alpha}'
    logger.detailed(f'Proportion of analytical hessian : {100*alpha}%')
    algoParameters = {'proportionAnalyticalHessian': alpha}
    start_time = datetime.now()

    results = biogeme.estimate(algorithm=opt.simpleBoundsNewtonAlgorithmForBiogeme,algoParameters = algoParameters)
    processingTime = datetime.now() - start_time
    allResults[alpha] = processingTime, results.data.logLike
    pandasResults = results.getEstimatedParameters()

for k, v in allResults.items():
    logger.detailed(f'alpha = {k}\t Running time: {v[0]}\tFinal log likelihood: {v[1]}')



