#!/usr/bin/env python
import sys

from yieldClass import *
from ROOT import *

def printLatexHeader(nCol, f):
    nCol = nCol + 4
    f.write('\\begin{table}[ht] \n ')
    f.write('\\footnotesize \n')
    f.write('\\caption{bla} \n')
    f.write('\\begin{tabular}{|' + (nCol *'%(align)s | ') % dict(align = 'c') + '} \n')
    f.write('\\hline \n')


def printLatexFooter(f):
    f.write('\\hline \n')
    f.write('\\end{tabular} \n')
    f.write('\\end{table} \n')   

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    ## Create Yield Storage

    yds6 = YieldStore("lepYields")
    yds9 = YieldStore("lepYields")
    yds5 = YieldStore("lepYields")

#    pattern = "Yields/MC/lumi3fb/full/*/merged/LT*NJ6*"
    pattern = "lumi21fb/gridWithDLCR/merged/LT*NJ6*"
    yds6.addFromFiles(pattern,("lep","sele"))
#    pattern = "Yields/MC/lumi3fb/full/*/merged/LT*NJ9*"
    pattern = "lumi21fb/gridWithDLCR/merged/LT*NJ9*"
    yds9.addFromFiles(pattern,("lep","sele"))

    pattern = "Yields/data/lumi1p5fb_0p8scale/full/grid/merged/LT*NJ5*"
    yds5.addFromFiles(pattern,("lep","sele")) 
    


    #pattern = 'arturstuff/grid/merged/LT\*NJ6\*'

    printSamps = ['TTsemiLep','TTdiLep','TTV','SingleT', 'WJets', 'DY', 'QCD','background','T1t$^4$ 1.5$/$0.2','T1t$^4$ 1.5$/$0.9']

    
    cats = ('SR_MB', 'CR_MB', 'SR_SB', 'CR_SB','DLCR_MB', 'DLCR_SB',)
    for cat in cats:
        f =  open('yields' + cat + '.tex','w')
        samps = [('TTsemiLep',cat),('TTdiLep',cat),('TTV',cat), ('SingleT',cat), ('WJets',cat), ('DY',cat), ('QCD',cat), ('background',cat),
('T1tttt_Scan_mGo1500_mLSP200',cat),('T1tttt_Scan_mGo1500_mLSP900',cat)]
        printLatexHeader(len(samps), f)
        yds6.showStats()
        label = 'Expected events in SR for 3 fbinv for njet 6,8 '
        yds6.printLatexTable(samps, printSamps, label,f) 
        label = 'Expected events in SR for 3 fb for njet $\\geq 9$'
        yds9.printLatexTable(samps, printSamps, label, f)
        printLatexFooter(f)

    print "Prepare dileptonic printout by calculating"
    yds6.divideTwoYieldDictsForRatio('DLCR_MB','SR_MB','DLCR_MB_RelSize')
    yds6.divideTwoYieldDictsForRatio('DLCR_SB','SR_SB','DLCR_SB_RelSize')
    yds9.divideTwoYieldDictsForRatio('DLCR_MB','SR_MB','DLCR_MB_RelSize')
    yds9.divideTwoYieldDictsForRatio('DLCR_SB','SR_SB','DLCR_SB_RelSize')

    yds6.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'background','data')
    yds9.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'background','data')
                                                          
    yds6.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'DiLep_Inc','background')
    yds9.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'DiLep_Inc','background')
    
    yds6.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'TTdiLep','background')
    yds9.divideTwoYieldDictsForRatio('COPYALL','COPYALL','dummy', False, 'TTdiLep','background')
    

    OutputHelperList = []
    OutputHelperList.append(OutputHelper(('background','SR_MB'),"all bkg(SR)"))
    OutputHelperList.append(OutputHelper(('DiLep_Inc','SR_MB_RTo_background'),"dilept.(SR)","percentage"))
    OutputHelperList.append(OutputHelper(('TTdiLep','SR_MB_RTo_background'),"ttbar dilept(SR)","percentage"))

    OutputHelperList.append(OutputHelper(('DiLep_Inc','SR_MB'),"Dilept. bkg(SR)"))
#    OutputHelperList.append(OutputHelper(('TTdiLep','SR_MB'),"ttbar dilept. bkg(SR)"))
#    OutputHelperList.append(OutputHelper(('DiLep_Inc','DLCR_MB'),"Dilept. bkg(DLCR)"))
    OutputHelperList.append(OutputHelper(('background','DLCR_MB'),"all bkg(DLCR)"))
    OutputHelperList.append(OutputHelper(('DiLep_Inc','DLCR_MB_RTo_background'),"dilept.(DLCR)","percentage"))
    OutputHelperList.append(OutputHelper(('data','DLCR_MB'),"data(DLCR)"))
#    OutputHelperList.append(OutputHelper(('background','DLCR_MB_RelDataMC'),"MCData(DLCR)","percentage"))
    OutputHelperList.append(OutputHelper(('background','DLCR_MB_RTo_data'),"MCData(DLCR)","percentage"))
    OutputHelperList.append(OutputHelper(('background','CR_MB_RTo_data'),"MCData(CR\_MB)", "percentage"))
#    OutputHelperList.append(OutputHelper(('TTdiLep','DLCR_MB_RelSize'),"rel. size (DLCR) ttdilep", "percentage"))
    OutputHelperList.append(OutputHelper(('DiLep_Inc','DLCR_MB_RelSize'),"rel. size (DLCR)","percentage"))
#    OutputHelperList.append(OutputHelper(('data','DLCR_MB_RelSize'),"rel. size (DLCR)data", "percentage"))

    f =  open('yieldsDLCRComparison.tex','w')
    printLatexHeader(len(OutputHelperList), f)
    yds6.showStats()
    label = 'Yield comparison for DL CR vs. signal region for 2.1 fbinv for njet 6,8 '
    yds6.printLatexTableEnh(OutputHelperList, label,f) 
    label = 'Yield comparison for DL CR vs. signal region for 2.1 fbinv for njet $\\geq 9$'
    yds9.printLatexTableEnh(OutputHelperList, label, f)
    printLatexFooter(f)


    f =  open('45j_test.tex','w')
    label = 'Counts and Rcs from 4jet sideband used to predict events in a 5jet signal region $5j_{SR} = Rcs^{4j,data} \\times \\kappa^{EWK, MC} \\times 5j_{CR}$'
    printSamps = ['data 4j, SR','(data-QCD) 4j, CR','data 4j, Rcs$^{EWK}$','$\\kappa^{EWK}$, MC','(data-QCD) 5j, CR', 'data 5j, pred', 'data 5j, SR', 'MCx0.8 5j,SR']

    #    samps = [('data','SR_SB'),('data','CR_SB'),('data','Rcs_SB'),('EWK','Kappa'),('data','CR_MB'),('data','SR_MB_predict'), ('data','SR_MB'), ('background','SR_MB')]
    samps = [('data_QCDsubtr','SR_SB'),('data_QCDsubtr','CR_SB'),('data_QCDsubtr','Rcs_SB'),('EWK','Kappa'),('data_QCDsubtr','CR_MB'),('data_QCDsubtr','SR_MB_predict'), ('data_QCDsubtr','SR_MB'), ('EWK','SR_MB')]
    printLatexHeader(len(samps), f)
    yds5.printLatexTable(samps, printSamps, label,f) 
    printLatexFooter(f)
