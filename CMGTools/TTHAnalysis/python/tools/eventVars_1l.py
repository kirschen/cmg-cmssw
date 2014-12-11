from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector
import ROOT

class EventVars1L:
    def __init__(self):
        self.branches = [ "METCopyPt", "DeltaPhiLepW" ]
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):

        # make python lists as Collection does not support indexing in slices
        leps = [l for l in Collection(event,"LepGood","nLepGood20",4)] #read in only the first 4 leptons
        jets = [j for j in Collection(event,"Jet","nJet40",8)] # read in only the first eight jets

        njet = len(jets); nlep = len(leps)

        metp4 = ROOT.TLorentzVector(0,0,0,0)
        metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass)

        # prepare output
        ret = dict([(name,0.0) for name in self.branches])
        # fill output

        #plain copy of MET pt
        ret["METCopyPt"] = metp4.Pt()
        
        dPhiLepW = -999
        if nlep>=1:
            recoWp4 =  leps[0].p4() + metp4
            dPhiLepW = leps[0].p4().DeltaPhi(recoWp4)
        ret["DeltaPhiLepW"] = dPhiLepW

        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("treeProducerSusySingleLepton") 
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
