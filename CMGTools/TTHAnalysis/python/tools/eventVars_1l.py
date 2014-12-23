from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2
import ROOT

def mt_2(p4one, p4two):
    return sqrt(2*p4one.Pt()*p4two.Pt()*(1-cos(p4one.Phi()-p4two.Phi())))

class EventVars1L:
    def __init__(self):
        self.branches = [ "METCopyPt", "DeltaPhiLepW", "minDPhiBMET", "idxMinDPhiBMET", "mTClBPlusMET", "mTBJetMET", "mTLepMET", "mLepBJet", "METtoTopProjection" ]
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):

        # make python lists as Collection does not support indexing in slices
        leps = [l for l in Collection(event,"LepGood","nLepGood20")] 
#        jets = [j for j in Collection(event,"Jet","nJet40",8)] # read in only the first eight jets
        jets = [j for j in Collection(event,"Jet","nJet40")] 

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

        minDPhiBMET    = 100
        idxMinDPhiBMET = -999
        for i, jet in enumerate(jets):
            if jet.btagCSV > 0.679:
                dPhiBMET = abs(jet.p4().DeltaPhi(metp4))
                if dPhiBMET<minDPhiBMET:
                    minDPhiBMET=dPhiBMET
                    idxMinDPhiBMET = i
#                    print dPhiBMET, i

        ret["idxMinDPhiBMET"] = idxMinDPhiBMET
        ret["minDPhiBMET"] = minDPhiBMET

        mTBJetMET      = -999
        mTLepMET      = -999
        mLepBJet       = -999
        if(idxMinDPhiBMET>=0):
            SumMetClosestBJet = jets[idxMinDPhiBMET].p4() + metp4
            ret["mTClBPlusMET"] = SumMetClosestBJet.Mt()
            mTBJetMET = mt_2(jets[idxMinDPhiBMET].p4(),metp4)
            if nlep>=1:
                mLepBJet = (jets[idxMinDPhiBMET].p4() + leps[0].p4()).M()
                mTLepMET = mt_2(leps[0].p4(),metp4)
        else:
            ret["mTClBPlusMET"] = -999

        ret["mTBJetMET"] = mTBJetMET
        ret["mTLepMET"]  = mTLepMET
        ret["mLepBJet"]  = mLepBJet
        

        METtoTopProjection = -999
        if(idxMinDPhiBMET>=0 and nlep >=1) :
            metV2  = ROOT.TVector2(0,0)
            lepV2  = ROOT.TVector2(0,0)
            bJetV2 = ROOT.TVector2(0,0)
            metV2   .SetMagPhi(event.met_pt, event.met_phi)
            lepV2   .SetMagPhi(leps[0].pt, leps[0].phi)
            bJetV2  .SetMagPhi(jets[idxMinDPhiBMET].pt, jets[idxMinDPhiBMET].phi)
            METtoTopProjection = (metV2*(metV2+lepV2+bJetV2))/(metV2*metV2)
        ret["METtoTopProjection"]  = METtoTopProjection
            
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

        
