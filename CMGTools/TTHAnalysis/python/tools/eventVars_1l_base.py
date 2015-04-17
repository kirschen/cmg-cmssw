from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

ROOT.gInterpreter.GenerateDictionary("vector<TLorentzVector>","TLorentzVector.h;vector") #need this to be able to use topness code

mt2wSNT = ROOT.heppy.mt2w_bisect.mt2w()
topness = ROOT.Topness.Topness()

def getPhysObjectArray(j): # https://github.com/HephySusySW/Workspace/blob/72X-master/RA4Analysis/python/mt2w.py
  px = j.pt*cos(j.phi )
  py = j.pt*sin(j.phi )
  pz = j.pt*sinh(j.eta )
  E = sqrt(px*px+py*py+pz*pz) #assuming massless particles...
  return array.array('d', [E, px, py,pz])


def mt_2(p4one, p4two):
	return sqrt(2*p4one.Pt()*p4two.Pt()*(1-cos(p4one.Phi()-p4two.Phi())))

def GetZfromM(vector1,vector2,mass):
	MT = sqrt(2*vector1.Pt()*vector2.Pt()*(1-cos(vector2.DeltaPhi(vector1))))
	if (MT<mass):
		Met2D = TVector2(vector2.Px(),vector2.Py())
		Lep2D = TVector2(vector1.Px(),vector1.Py())
		A = mass*mass/2.+Met2D*Lep2D
		Delta = vector1.E()*vector1.E()*(A*A-Met2D.Mod2()*Lep2D.Mod2())
		MetZ1 = (A*vector1.Pz()+sqrt(Delta))/Lep2D.Mod2()
		MetZ2 = (A*vector1.Pz()-sqrt(Delta))/Lep2D.Mod2()
	else:
		MetZ1 =vector1.Pz()*vector2.Pt()/vector1.Pt()
		MetZ2 =vector1.Pz()*vector2.Pt()/vector1.Pt()
	return [MT,MetZ1,MetZ2]

def minValueForIdxList(values,idxlist):
  cleanedValueList = [val for i,val in enumerate(values) if i in idxlist]
  if len(cleanedValueList)>0: return min(cleanedValueList)
  else: return -999
  #  print cleanedValueList, min(cleanedValueList)#d, key=d.get)


class EventVars1L_base:
	def __init__(self):
		self.branches = [ "METCopyPt", "DeltaPhiLepW",
						  ("nTightLeps","I"),("tightLepsIdx","I",10,"nTightLeps"),("nVetoLeps","I"),("vetoLepsIdx","I",10,"nVetoLeps"),
						  ("tightLeps_DescFlag","I",10,"nTightLeps"),
						  ("nTightEl","I"),("tightElIdx","I",10,"nTightEl"),("nVetoEl","I"),("vetoElIdx","I",10,"nVetoEl"),
						  ("nTightMu","I"),("tightMuIdx","I",10,"nTightMu"),("nVetoMu","I"),("vetoMuIdx","I",10,"nVetoMu"),
						  'HT','ST','LepGood1_pt','LepGood1_pdgId','LepGood1_eta',
						  ("nCentralJet30","I"),("centralJet30idx","I",100,"nCentralJet30"),("centralJet30_DescFlag","F",100,"nCentralJet30"),
						  ("nBJetCMVAMedium30","I"),("BJetCMVAMedium30idx","I",50,"nBJetCMVAMedium30"),
						  "nGoodBJets_allJets", "nGoodBJets",
						  "LSLjetptGT80", "htJet30j", "htJet30ja"
						  ]


	def listBranches(self):
		return self.branches[:]


	def __call__(self,event,keyvals):

		# make python lists as Collection does not support indexing in slices
		genleps = [l for l in Collection(event,"genLep","ngenLep")]

		leps = [l for l in Collection(event,"LepGood","nLepGood")]
		jets = [j for j in Collection(event,"Jet","nJet")]

		fatjets = [j for j in Collection(event,"FatJet","nFatJet")]

		njet = len(jets); nlep = len(leps)

		metp4 = ROOT.TLorentzVector(0,0,0,0)
		metp4.SetPtEtaPhiM(event.met_pt,event.met_eta,event.met_phi,event.met_mass)
		pmiss  =array.array('d',[event.met_pt * cos(event.met_phi), event.met_pt * sin(event.met_phi)] )

		#isolation criteria as defined for PHYS14 1l synchronisation exercise
		ele_relisoCut = 0.14
		muo_relisoCut = 0.12
		#ele tight id --> >2
		#muo tight id ==1
		centralEta = 2.4

		muo_minirelisoCut = 0.2
		Lep_minirelisoCut = 0.4
		ele_minirelisoCut = 0.1

		goodEl_lostHits = 0
		goodEl_sip3d = 4

		goodEl_mvaPhys14_eta0p8_T = 0.73;
		goodEl_mvaPhys14_eta1p4_T = 0.57;
		goodEl_mvaPhys14_eta2p4_T = 0.05;

		### LEPTONS

		hardTightLeps = []
		hardTightLepsIdx = []
		hardVetoLeps = []
		hardVetoLepsIdx = []

		softTightLeps = []
		softTightLepsIdx = []
		softVetoLeps = []
		softVetoLepsIdx = []

		hardTightMu = []
		hardTightMuIdx = []
		hardVetoMu = []
		hardVetoMuIdx = []

		softTightMu = []
		softTightMuIdx = []
		softVetoMu = []
		softVetoMuIdx = []

		hardTightEl = []
		hardTightElIdx = []
		hardVetoEl = []
		hardVetoElIdx = []

		softTightEl = []
		softTightElIdx = []
		softVetoEl = []
		softVetoElIdx = []

		for idx,lep in enumerate(leps):

			# check acceptance
			lepEta = abs(lep.eta)

			if(lepEta > 2.5): continue

			# muons
			if(abs(lep.pdgId) == 13):
				# pass variables
				passID = False
				passIso = False

				# hard: pt > 25
				if lep.pt > 25:

					# all hard leptons are veto for soft
					softVetoLeps.append(lep); softVetoLepsIdx.append(idx);
					softVetoMu.append(lep); softVetoMuIdx.append(idx);

					# ID and Iso check:
					if lep.mediumMuonId == 1 and lep.sip3d < 4.0: passID = True
					if lep.miniRelIso < muo_minirelisoCut:        passIso = True

					# fill
					if passID and passIso:
						hardTightLeps.append(lep); hardTightLepsIdx.append(idx);
						hardTightMu.append(lep); hardTightMuIdx.append(idx);
					else:
						hardVetoLeps.append(lep); hardVetoLepsIdx.append(idx);
						hardVetoMu.append(lep); hardVetoMuIdx.append(idx);

				# soft muons + tight veto
				elif lep.pt > 5:
					# veto for tight if pt > 10
					if lep.pt > 10:
						hardVetoLeps.append(lep); hardVetoLepsIdx.append(idx);
						hardVetoMu.append(lep); hardVetoMuIdx.append(idx);
					# Soft leptons
					# ID check
					if lep.mediumMuonId == 1 and lep.sip3d < 4.0: passID = True
					# iso check
					if lep.pt < 15   and lep.miniRelIso < Lep_minirelisoCut: passIso = True
					elif lep.pt > 15 and lep.miniRelIso < muo_minirelisoCut: passIso = True

					# fill
					if passID and passIso:
						softTightLeps.append(lep); softTightLepsIdx.append(idx);
						softTightMu.append(lep); softTightMuIdx.append(idx);
					else:
						softVetoLeps.append(lep); softVetoLepsIdx.append(idx);
						softVetoMu.append(lep); softVetoMuIdx.append(idx);

			# electrons
			if(abs(lep.pdgId) == 11):
				# pass variables
				passID = False
				passIso = False
				passEta = False
				passConv = False

				# hard: pt > 25
				if lep.pt > 25:

					# all hard leptons are veto for soft
					softVetoLeps.append(lep); softVetoLepsIdx.append(idx);
					softVetoEl.append(lep); softVetoElIdx.append(idx);

					# Iso check:
					if lep.miniRelIso < ele_minirelisoCut: passIso = True
					# Eta dependent MVA ID check:
					if lepEta < 0.8 and lep.mvaIdPhys14 > goodEl_mvaPhys14_eta0p8_T: passID = True
					elif lepEta >= 0.8 and lepEta < 1.44 and lep.mvaIdPhys14 > goodEl_mvaPhys14_eta1p4_T: passID = True
					elif lepEta >= 1.57 and lepEta < 2.4 and lep.mvaIdPhys14 > goodEl_mvaPhys14_eta2p4_T: passID = True
					# conversion check
					if lep.lostHits <= goodEl_lostHits and lep.convVeto and lep.sip3d < goodEl_sip3d: passConv = True

					# fill
					if passID and passIso and passConv:
						hardTightLeps.append(lep); hardTightLepsIdx.append(idx);
						hardTightEl.append(lep); hardTightElIdx.append(idx);
					else:
						hardVetoLeps.append(lep); hardVetoLepsIdx.append(idx);
						hardVetoEl.append(lep); hardVetoElIdx.append(idx);

				# soft muons + tight veto
				elif lep.pt > 5:

					# veto fro tight if pt > 10
					if lep.pt > 10:
						hardVetoLeps.append(lep); hardVetoLepsIdx.append(idx);
						hardVetoEl.append(lep); hardVetoElIdx.append(idx);

					# Soft leptons
					# check eta
					if (lepEta < 1.44 or lepEta >= 1.57) and lepEta < 2.4: passEta = True

					# MVA(ID+Iso) check
					if lep.mvaSusy > 0.53: passID = True
					# conversion check
					if lep.lostHits <= goodEl_lostHits and lep.convVeto and lep.sip3d < goodEl_sip3d: passConv = True

					# fill
					if passID and passEta and passConv:
						softTightLeps.append(lep); softTightLepsIdx.append(idx);
						softTightEl.append(lep); softTightElIdx.append(idx);
					else:
						softVetoLeps.append(lep); softVetoLepsIdx.append(idx);
						softVetoEl.append(lep); softVetoElIdx.append(idx);
		# end lepton loop

		# choose common lepton collection: select hard or soft lepton
		if len(hardTightLeps) > 0:
			tightLeps = hardTightLeps
			tightLepsIdx = hardTightLepsIdx
			vetoLeps = hardVetoLeps
			vetoLepsIdx = hardVetoLepsIdx

			tightEl = hardTightEl
			tightElIdx = hardTightElIdx
			vetoEl = hardVetoEl
			vetoElIdx = hardVetoElIdx

			tightMu = hardTightMu
			tightMuIdx = hardTightMuIdx
			vetoMu = hardVetoMu
			vetoMuIdx = hardVetoMuIdx

		else: #if len(softTightLeps) > 0: or empty collection
			tightLeps = softTightLeps
			tightLepsIdx = softTightLepsIdx
			vetoLeps = softVetoLeps
			vetoLepsIdx = softVetoLepsIdx

			tightEl = softTightEl
			tightElIdx = softTightElIdx
			vetoEl = softVetoEl
			vetoElIdx = softVetoElIdx

			tightMu = softTightMu
			tightMuIdx = softTightMuIdx
			vetoMu = softVetoMu
			vetoMuIdx = softVetoMuIdx

		#initialize the dictionary with a first entry
		ret = {}
		#ret = { 'nTightLeps'   : len(tightLeps) }
		ret['nTightLeps'] = len(tightLeps)
		ret['tightLepsIdx'] = tightLepsIdx
		ret['nVetoLeps'] = len(vetoLeps)
		ret['vetoLepsIdx'] = vetoLepsIdx

		ret['nTightEl'] = len(tightEl)
		ret['tightElIdx'] = tightElIdx
		ret['nVetoEl'] = len(vetoEl)
		ret['vetoElIdx'] = vetoElIdx

		ret['nTightMu'] = len(tightMu)
		ret['tightMuIdx'] = tightMuIdx
		ret['nVetoMu'] = len(vetoMu)
		ret['vetoMuIdx'] = vetoMuIdx

		# save leading lepton vars
		if len(tightLeps) > 0:
			ret['LepGood1_pt'] = tightLeps[0].pt
			ret['LepGood1_eta'] = tightLeps[0].eta
			ret['LepGood1_pdgId'] = tightLeps[0].pdgId
		elif len(leps) > 0: # fill it with leading lepton
			ret['LepGood1_pt'] = leps[0].pt
			ret['LepGood1_eta'] = leps[0].eta
			ret['LepGood1_pdgId'] = leps[0].pdgId
		else:
			ret['LepGood1_pt'] = -99
			ret['LepGood1_eta'] = -99
			ret['LepGood1_pdgId'] = -99

		### JETS

		centralJet30 = []
		centralJet30idx = []
		for i,j in enumerate(jets):
			if j.pt>30 and abs(j.eta)<centralEta:
				centralJet30.append(j)
				centralJet30idx.append(i)

		ret['nCentralJet30']   = len(centralJet30)
		ret['centralJet30idx'] = centralJet30idx

		ret['LSLjetptGT80'] = 1 if sum([j.pt>80 for j in centralJet30])>=2 else 0

		ret['htJet30j']  = sum([j.pt for j in centralJet30])
		ret['htJet30ja'] = sum([j.pt for j in jets if j.pt>30])

		ret['HT'] = ret['htJet30j']

		BJetCMVAMedium30 = []
		BJetCMVAMedium30idx = []
		NonBJetCMVAMedium30 = []
		for i,j in enumerate(centralJet30):
			if j.btagCMVA>0.732:
				BJetCMVAMedium30.append(j)
				BJetCMVAMedium30idx.append(centralJet30idx[i])
			else:
				NonBJetCMVAMedium30.append(j)
		ret['nBJetCMVAMedium30']    = len(BJetCMVAMedium30)
		ret['BJetCMVAMedium30idx']  = BJetCMVAMedium30idx

		ret['nGoodBJets']    = sum([j.btagCMVA>0.732 for j in centralJet30])
		ret['nGoodBJets_allJets']    = sum([j.btagCMVA>0.732 and j.pt>30 and abs(j.eta)<centralEta for j in jets]) # where is the working point defined?

		#plain copy of MET pt (just as an example and cross-check for proper friend tree production)
		ret["METCopyPt"] = metp4.Pt()

		# deltaPhi between the (single) lepton and the reconstructed W (lep + MET)
		dPhiLepW = -999 # set default value to -999 to spot "empty" entries
		# ST of lepton and MET
		ST = -999

		if len(tightLeps) >=1:
			recoWp4 =  tightLeps[0].p4() + metp4
			dPhiLepW = tightLeps[0].p4().DeltaPhi(recoWp4)
			ST = tightLeps[0].pt + event.met_pt

		ret["DeltaPhiLepW"] = dPhiLepW
		ret['ST'] = ST

		centralJet30_DescFlag = []
		tightLeps_DescFlag = []

		for i,l in enumerate(tightLeps):
		  if abs(l.mcMatchId)==6: tightLeps_DescFlag.append(1)    #top
		  elif abs(l.mcMatchId)==24: tightLeps_DescFlag.append(2) #W-boson
		  else: tightLeps_DescFlag.append(0)

		for i,j in enumerate(centralJet30):
		  if abs(j.mcMatchId)==6:
			if len(genleps)>0 and abs(genleps[0].sourceId) ==6 and abs(j.mcFlavour)==5:
			  if j.mcMatchId==genleps[0].sourceId:
				centralJet30_DescFlag.append(genleps[0].charge)
			  else:
				centralJet30_DescFlag.append(2)
			elif abs(j.mcFlavour) not in [0,5,21]:
			  centralJet30_DescFlag.append(3)
			else: centralJet30_DescFlag.append(-999) #; print "should not happen..."
		  else: centralJet30_DescFlag.append(0)

		ret["centralJet30_DescFlag"]=centralJet30_DescFlag
		ret["tightLeps_DescFlag"]=tightLeps_DescFlag

		return ret

# Main function for test
if __name__ == '__main__':
	from sys import argv
	file = ROOT.TFile(argv[1])
	tree = file.Get("tree")
	class Tester(Module):
		def __init__(self, name):
			Module.__init__(self,name,None)
			self.sf = EventVars1L()
		def analyze(self,ev):
			print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
			print self.sf(ev)
	el = EventLoop([ Tester("tester") ])
	el.loop([tree], maxEvents = 50)
