from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT


class EventVars1LWeightsForSystematics:
    def __init__(self):
        self.branches = ["GenTopPt", "GenAntiTopPt", "TopPtWeight", "GenTTBarPt", "GenTTBarWeight", "DilepNJetWeightConst", "DilepNJetWeightSlope", "DilepNJetWeight", 
                         ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base={}):
        #
        # prepare output
        ret = {}
        for name in self.branches:
#            print name
            if type(name) is tuple:
                ret[name] = []
            elif type(name) is str:
                ret[name] = -999.0
            else:
                print "could not identify"
#        print ret

        if base['Selected']!=1: return ret #only run the full module on selected leptons, not the ones for QCD estimate

        GenTopPt = -999
        GenTopIdx = -999
        GenAntiTopPt = -999
        GenAntiTopIdx = -999
        TopPtWeight = 1.
        GenTTBarPt = -999
        GenTTBarWeight = 1.

        nGenTops = 0
        if not event.isData:
            genParts = [l for l in Collection(event,"GenPart","nGenPart")]
            for i_part, genPart in enumerate(genParts):
                if genPart.pdgId ==  6:     
                    GenTopPt = genPart.pt
                    GenTopIdx = i_part
                if genPart.pdgId == -6: 
                    GenAntiTopPt = genPart.pt
                    GenAntiTopIdx = i_part
                if abs(genPart.pdgId) ==  6: nGenTops+=1

                if GenTopPt!=-999 and GenAntiTopPt!=-999 and nGenTops==2:
                    SFTop     = exp(0.156    -0.00137*GenTopPt    )
                    SFAntiTop = exp(0.156    -0.00137*GenAntiTopPt)
                    TopPtWeight = sqrt(SFTop*SFAntiTop)
                    if TopPtWeight<0.5: TopPtWeight=0.5
            
                if GenAntiTopIdx!=-999 and GenTopIdx!=-999:
                    GenTTBarp4 = genParts[GenTopIdx].p4()+ genParts[GenAntiTopIdx].p4()
                    GenTTBarPt = GenTTBarp4.Pt()
                    if GenTTBarPt>120: GenTTBarWeight= 0.95
                    if GenTTBarPt>150: GenTTBarWeight= 0.90
                    if GenTTBarPt>250: GenTTBarWeight= 0.80
                    if GenTTBarPt>400: GenTTBarWeight= 0.70

#markus proposal for njet-reweighting           
#The level of agreement is important to us. We could reweight top events by 1.05 per jet that does not come from the top and compare again the distributions (changes yield ~ 27% for 5 jets not from the top). If that is more that the difference we see in data we can propose this as an uncertainty.


        # values in sync with AN2015_207_v3
        #        Const weight
        # const: 0.85 +-0.06
        #        16%
        wmean = 5.82 - 0.5
        # slope: 0.03 +/-0.05
        slopevariation = sqrt(0.03*0.03 +0.05*0.05) 
        if (event.ngenLep+event.ngenTau)==2:
            ret['DilepNJetWeightConst'] = 0.84
            ret['DilepNJetWeightSlope'] = 1+ (base['nJets30Clean']-wmean)*slopevariation
        else:
            ret['DilepNJetWeightConst'] = 1.
            ret['DilepNJetWeightSlope'] = 1.


        #Alternative "all in one" weight which is the envelope of the 68% unc. band with a big jump around the mean value (to be deprecated)
        DiLepWeightDict = dict([ ( 3 , 0.8402), 
                                 ( 4 , 0.8913), 
                                 ( 5 , 0.9265), 
                                 ( 6 , 1.0788), 
                                 ( 7 , 1.1286), 
                                 ( 8 , 1.1832), 
                                 ( 9 , 1.2475), 
                                 ( 10 , 1.3034), 
                                 ( 11 , 1.3578), 
                                 ])
        if base['nJets30Clean']<12 and base['nJets30Clean']>2 and event.ngenLep+event.ngenTau==2:
            ret['DilepNJetWeight'] = DiLepWeightDict[base['nJets30Clean']]
        else:
            ret['DilepNJetWeight'] = 1.

        ret['GenTopPt'] = GenTopPt
        ret['GenAntiTopPt'] = GenAntiTopPt
        ret['TopPtWeight']  = TopPtWeight
        ret['GenTTBarPt']  = GenTTBarPt
        ret['GenTTBarWeight'] = GenTTBarWeight
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1LWeightsForSystematics()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
#            tree.Show(0)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
