import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"  # use environmental variable, useful for instance to run on CRAB
#json=dataDir+'/json/Cert_246908-257599_13TeV_PromptReco_Collisions15_25ns_JSON_v3_private.txt'
#https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2503.html
#golden JSON 225.57/pb

# https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/2520.html
json="/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Cert_246908-258714_13TeV_PromptReco_Collisions15_25ns_JSON.txt"

### ----------------------------- Magnetic Field On ----------------------------------------

Jet_Run2015B            = kreator.makeDataComponent("Jet_Run2015B"           , "/Jet/Run2015B-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json, [251585,251883])
JetHT_Run2015B          = kreator.makeDataComponentDESY("JetHT_Run2015B"         , "/JetHT/Run2015B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json, [251585,251883])
HTMHT_Run2015B          = kreator.makeDataComponent("HTMHT_Run2015B"         , "/HTMHT/Run2015B-PromptReco-v1/MINIAOD"         , "CMS", ".*root", json, [251585,251883])
MET_Run2015B            = kreator.makeDataComponentDESY("MET_Run2015B"           , "/MET/Run2015B-PromptReco-v1/MINIAOD"           , "CMS", ".*root", json, [251585,251883])
SingleElectron_Run2015B = kreator.makeDataComponentDESY("SingleElectron_Run2015B", "/SingleElectron/Run2015B-PromptReco-v1/MINIAOD", "CMS", ".*root", json, [251585,251883])
SingleMu_Run2015B       = kreator.makeDataComponent("SingleMu_Run2015B"      , "/SingleMu/Run2015B-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json, [251585,251883])
SingleMuon_Run2015B     = kreator.makeDataComponent("SingleMuon_Run2015B"    , "/SingleMuon/Run2015B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json, [251585,251883])
SinglePhoton_Run2015B   = kreator.makeDataComponent("SinglePhoton_Run2015B"  , "/SinglePhoton/Run2015B-PromptReco-v1/MINIAOD"  , "CMS", ".*root", json, [251585,251883])
EGamma_Run2015B         = kreator.makeDataComponent("EGamma_Run2015B"        , "/EGamma/Run2015B-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json, [251585,251883])
DoubleEG_Run2015B       = kreator.makeDataComponent("DoubleEG_Run2015B"      , "/DoubleEG/Run2015B-PromptReco-v1/MINIAOD"      , "CMS", ".*root", json, [251585,251883])
MuonEG_Run2015B         = kreator.makeDataComponent("MuonEG_Run2015B"        , "/MuonEG/Run2015B-PromptReco-v1/MINIAOD"        , "CMS", ".*root", json, [251585,251883])
DoubleMuon_Run2015B     = kreator.makeDataComponent("DoubleMuon_Run2015B"    , "/DoubleMuon/Run2015B-PromptReco-v1/MINIAOD"    , "CMS", ".*root", json, [251585,251883])

minBias_Run2015B  = kreator.makeDataComponent("minBias_Run2015B" , "/MinimumBias/Run2015B-PromptReco-v1/MINIAOD", "CMS", ".*root", json, [251585,251883])
zeroBias_Run2015B = kreator.makeDataComponent("zeroBias_Run2015B", "/ZeroBias/Run2015B-PromptReco-v1/MINIAOD"   , "CMS", ".*root", json, [251585,251883])

dataSamples_Run2015B = [Jet_Run2015B, JetHT_Run2015B, HTMHT_Run2015B, MET_Run2015B, SingleElectron_Run2015B, SingleMu_Run2015B, SingleMuon_Run2015B, SinglePhoton_Run2015B, EGamma_Run2015B, DoubleEG_Run2015B, MuonEG_Run2015B, DoubleMuon_Run2015B, minBias_Run2015B, zeroBias_Run2015B]


### ----------------------------- 17July re-reco ----------------------------------------

JetHT_Run2015B_17Jul          = kreator.makeDataComponent("JetHT_Run2015B_17Jul"         , "/JetHT/Run2015B-17Jul2015-v1/MINIAOD"         , "CMS", ".*root", json)
HTMHT_Run2015B_17Jul          = kreator.makeDataComponent("HTMHT_Run2015B_17Jul"         , "/HTMHT/Run2015B-17Jul2015-v1/MINIAOD"         , "CMS", ".*root", json)
SingleElectron_Run2015B_17Jul = kreator.makeDataComponent("SingleElectron_Run2015B_17Jul", "/SingleElectron/Run2015B-17Jul2015-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015B_17Jul     = kreator.makeDataComponent("SingleMuon_Run2015B_17Jul"    , "/SingleMuon/Run2015B-17Jul2015-v1/MINIAOD"    , "CMS", ".*root", json)


dataSamples_17Jul = [JetHT_Run2015B_17Jul, HTMHT_Run2015B_17Jul, SingleElectron_Run2015B_17Jul, SingleMuon_Run2015B_17Jul]

### ----------------------------- Run2015D ----------------------------------------
### only those at desy

JetHT_Run2015D          = kreator.makeDataComponentDESY("JetHT_Run2015D"         , "/JetHT/Run2015D-PromptReco-v3/MINIAOD"         , "CMS", ".*root", json)
SingleElectron_Run2015D = kreator.makeDataComponentDESY("SingleElectron_Run2015D", "/SingleElectron/Run2015D-PromptReco-v3/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2015D     = kreator.makeDataComponentDESY("SingleMuon_Run2015D"    , "/SingleMuon/Run2015D-PromptReco-v3/MINIAOD"    , "CMS", ".*root", json)

dataSamples_Run2015D = [JetHT_Run2015D, SingleElectron_Run2015D, SingleMuon_Run2015D]

### ----------------------------- summary ----------------------------------------

dataSamples = dataSamples_Run2015B + dataSamples_17Jul + dataSamples_Run2015D
samples = dataSamples

### ---------------------------------------------------------------------

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

for comp in dataSamples:
    comp.splitFactor = 1000
    comp.isMC = False
    comp.isData = True

if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(samples)
