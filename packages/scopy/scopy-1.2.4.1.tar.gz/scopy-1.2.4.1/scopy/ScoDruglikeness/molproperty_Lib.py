# -*- coding: utf-8 -*-
"""
Created on Fri May 15 22:47:38 2020

@Author: Zhi-Jiang Yang, Dong-Sheng Cao
@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
@Homepage: http://www.scbdd.com
@Mail: yzjkid9@gmail.com; oriental-cds@163.com
@Blog: https://blog.iamkotori.com

♥I love Princess Zelda forever♥
"""



import os
import csv
from multiprocessing import Pool
from rdkit import Chem
from . import molproperty
from .. import ScoConfig
from ..ScoRepresent.fingerprints import CalculateGhoseCrippen

    


def _GetSmi(mol):
    """
    Get the SMILES of molecule
    
    :param mols: molecule
    :type mols: rdkit.Chem.rdchem.Mol
    :return: The SMILES of molecule
    :rtype: string
    
    """
    return Chem.MolToSmiles(mol)
    

class PC_properties(object):
    """
    Here, we comdat the whole function that computing property retrieved from module molproperty
    
    :param mols: The molecule to be scanned.
    :type mols: Iterable object, each element is rdkit.Chem.rdchem.Mol
    :param n_jobs: The number of CPUs to use to do the computation, defaults to 1
    :type n_jobs: int, optional
    
    """
    def __init__(self, mols, n_jobs=1):
        self.mols = mols if type(mols) is not Chem.rdchem.Mol else [mols]
        self.n_jobs = n_jobs if n_jobs>=1 else None
    
    def CalculateMolWeight(self):    
        """
        Calculation of molecular weight(contain hydrogen atoms)   
        --->MW  
        
        :param mols: molecules
        :type mols: Iterable
        :return: the weight of molecule(contain hydrogen atoms)
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        MW = pool.map_async(molproperty.CalculateMolWeight, self.mols).get()
        pool.close()
        pool.join()
        return MW
    
    def CalculateNumBonds(self):
        """
        Calculation the number of bonds where between heavy atoms       
        --->nBond
            
        :param mols: molecules
        :type mols: Iterable
        :return: the number of bonds where between heavy atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nBond = pool.map_async(molproperty.CalculateNumBonds, self.mols).get()
        pool.close()
        pool.join()
        return nBond
    
    def CalculateNumAtoms(self):
        """
        Calculation of the number of atoms in molecular(contain hydrogen atoms) 
        --->nAtom
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of atoms in molecular(contain hydrogen atoms)
        :rtype: int
        
        """  
        pool = Pool(self.n_jobs)
        nAtom = pool.map_async(molproperty.CalculateNumAtoms, self.mols).get()
        pool.close()
        pool.join()
        return nAtom
        
    def CalculateNumHetero(self):
        """
        Calculation of the number of heteroatom in a molecule  
        --->nHet
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of heteroatom in a molecule  
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nHet = pool.map_async(molproperty.CalculateNumHetero, self.mols).get()
        pool.close()
        pool.join()
        return nHet
    
    
    def CalculateNumRotatableBonds(self):
        """
        Calculation of the number of rotatableBonds
        --->nRot
        
        Note:
            In some situaion Amide C-N bonds are not considered 
            because of their high rotational energy barrier
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of rotatableBond  
        :rtype: list
        
        
        """
        pool = Pool(self.n_jobs)
        nRot = pool.map_async(molproperty.CalculateNumRotatableBonds, self.mols).get()
        pool.close()
        pool.join()
        return nRot
    
    def CalculateNumRigidBonds(self):
        """
        Number of non-flexible bonds, in opposite to rotatable bonds    
        --->nRig
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of non-flexible bonds 
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nRig = pool.map_async(molproperty.CalculateNumRigidBonds, self.mols).get()
        pool.close()
        pool.join()
        return nRig
     
    def CalculateFlexibility(self):
        """
        The flexibility (ration between rotatable and rigid bonds)
        --->Flex
        
        :param mol: molecules
        :type mol: rdkit.Chem.rdchem.Mol
        :return: the number of ring   
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        Flex = pool.map_async(molproperty.CalculateFlexibility, self.mols).get()
        pool.close()
        pool.join()
        return Flex
    
    def CalculateNumRing(self):
        """
        Calculation of the number of ring   
        --->nRing
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of ring   
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nRing = pool.map_async(molproperty.CalculateNumRing, self.mols).get()
        pool.close()
        pool.join()
        return nRing
       
    def CalculateNumHeavyAtom(self):
        """
        Calculation of Heavy atom counts in a molecule   
        --->nHev
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of heavy atom counts in a molecule  
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nHev = pool.map_async(molproperty.CalculateNumHeavyAtom, self.mols).get()
        pool.close()
        pool.join()
        return nHev
    
    def CalculateLogD(self):
        """
        Calculation of molecular logD under pH=7.4
        --->LogD
        
        Note:
            We have built a liner model with DNN to predict logD7.4.
        
        :param mols: molecules
        :type mols: Iterable
        :return: molecular logD under pH=7.4 
        :rtype: list
        
        """
        intercept = 0.5748907159915493
    
        fps = CalculateGhoseCrippen(self.mols,self.n_jobs)
        with open(os.path.join(ScoConfig.CrippenDir, 'Crippen.txt')) as f_obj:
            lines = csv.reader(f_obj,delimiter='\t')
            next(lines)
            contri = [x[-1] for x in lines]
            contri = [float(x) for x in contri]
        f_obj.close()
        logD = (fps*contri).sum(axis=1) + intercept
        return list(logD)
    
    def CalculateLogP(self):    
        """
        Calculation of molecular LogP
        --->logP
        
        :param mols: molecules
        :type mols: Iterable
        :return: molecular logP 
        :rtype: float
        
        """  
        pool = Pool(self.n_jobs)
        logp = pool.map_async(molproperty.CalculateLogP, self.mols).get()
        pool.close()
        pool.join()
        return logp
    
    def CheckAcid(self):
        """
        Judge a molecular whether is acid via SMARTS.
        These SMARTS retrived from https://www.daylight.com/dayhtml_tutorials/languages/smarts/smarts_examples.html
        --->ab
        
        :param mols: molecules
        :type mols: Iterable
        :return: classification to acid or base
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        ab = pool.map_async(molproperty.CheckAcid, self.mols).get()
        pool.close()
        pool.join()
        return ab     
      
          
    def CalculatepKa(self):
        """
        *This function should be revised*
        Calculating pKa based on the ralation between logD and logP in specific pH.
        --->pKa
        
        Eq.:
            abs(pH-pKa) = log10(10^(logP-logD)-1)
            pKa = pH - log10(10^(logP-logD)-1) for acid
            pKa = log10(10^(logP-logD)-1) - pH for base
            
        :param mols: molecules
        :type mols: Iterable
        :return: molecular pKa
        :rtype: list
        
        """
        import warnings
        warnings.filterwarnings('ignore')
        from math import log10
        logDl = self.CalculateLogD()
        logPl = self.CalculateLogP()
        statusl = self.CheckAcid()
        res = []
        for status,logP, logD in zip(statusl,logPl,logDl):
            try:
                if status == 'acid':
                    pKa = 7.4 - log10(10**(logP-logD)-1)
                else:
                    pKa = log10(10**(logP-logD)-1) - 7.4
                res.append(pKa)
            except:
                res.append('N/A')
        return res
        
    def CalculateMolMR(self):
        """
        Cacluation of molecular refraction value based on Crippen method 
        --->MR
        
        :param mols: molecules
        :type mols: Iterable
        :return: molecular refraction value based on Crippen method
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        mr = pool.map_async(molproperty.CalculateMolMR, self.mols).get()
        pool.close()
        pool.join()
        return mr
    
    def CalculateNumHDonors(self):    
        """
        Caculation of the number of Hydrogen Bond Donors
        --->nHD
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of Hydrogen Bond Donors
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nHD = pool.map_async(molproperty.CalculateNumHDonors, self.mols).get()
        pool.close()
        pool.join()
        return nHD
    
    def CalculateNumHAcceptors(self):    
        """
        Caculation of the number of Hydrogen Bond Acceptors  
        --->nHA
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of Hydrogen Bond Acceptors
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nHA = pool.map_async(molproperty.CalculateNumHAcceptors, self.mols).get()
        pool.close()
        pool.join()
        return nHA
    
    def CalculateNumHyBond(self):
        """
        Sum of Hydrogen Bond Donnors and Acceptors   
        --->nHB
        
        :param mols: molecules
        :type mols: Iterable
        :return: sum of Hydrogen Bond Donnors and Acceptors
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nHB = pool.map_async(molproperty.CalculateNumHyBond, self.mols).get()
        pool.close()
        pool.join()
        return nHB
    
    
    def CalculateAromaticProportion(self):
        """
        The proportion of heavy atoms in the molecule that are in an aromatic ring  
        --->AP
        
        :param mols: molecules
        :type mols: Iterable
        :return: the proportion of heavy atoms in the molecule that are in an aromatic ring  
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        aroma = pool.map_async(molproperty.CalculateAromaticProportion, self.mols).get()
        pool.close()
        pool.join()
        return aroma
        
    
    def CalculateLogSw(self):
        """
        The logSw represents the logarithm of compounds water solubility computed by the ESOL method
        --->logSw
        
        Equation: 
            Log(Sw) = 0.16-0.638*clogP-0.0062*MWT+0.066*RB-0.74*AP
            where, MWT: Molecular Weight; RB: Rotatable bonds; AP: Aromatic proportion
        
        Reference:
            (1) `Delaney, John S (2004)`_. 
        
        :param mols: molecules
        :type mols: Iterable
        :return: the molecular logSw
        :rtype: list
        
        .. _Delaney, John S (2004):
            https://pubs.acs.org/doi/abs/10.1021/ci034243x
            
        """
        pool = Pool(self.n_jobs)
        logSw = pool.map_async(molproperty.CalculateLogSw, self.mols).get()
        pool.close()
        pool.join()
        return logSw
    
    def CalculateFsp3(self):
        """
        Fsp3 (carbon bond saturation) is defined as the number of sp3 hybridized carbons / total carbon count.   
        --->FSP3
        
        :param mols: molecules
        :type mols: Iterable
        :return: the carbon bond saturation
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        fsp3 = pool.map_async(molproperty.CalculateFsp3, self.mols).get()
        pool.close()
        pool.join()
        return fsp3
        
    def CalculateTPSA(self):
        """
        Calculation of TPSA   
        --->TPSA
        
        :param mols: molecules
        :type mols: Iterable
        :return: TPSA
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        tpsa = pool.map_async(molproperty.CalculateTPSA, self.mols).get()
        pool.close()
        pool.join()
        return tpsa
        
               
    def CalculateQEDmean(self):
        """
        Calculation QED descriptor under different weights 
        A descriptor a measure of drug-likeness based on the concept of desirability
        Here, calculating the QED descriptor using average descriptor weights.
        --->QEDmean
        
        Reference:
            (1) `Bickerton, G. Richard (2012)`_.
        
        :param mols: molecules
        :type mols: Iterable
        :return: QED descriptor using average descriptor weights
        :rtype: list
        
        .. _Bickerton, G. Richard (2012):
            https://www.nature.com/nchem/journal/v4/n2/abs/nchem.1243.html
            
        """    
        pool = Pool(self.n_jobs)
        qed_mean = pool.map_async(molproperty.CalculateQEDmean, self.mols).get()
        pool.close()
        pool.join()
        return qed_mean
    
    
    def CalculateQEDmax(self):
        """
        Calculation QED descriptor under different weights   
        A descriptor a measure of drug-likeness based on the concept of desirability
        Here, calculating the QED descriptor using maximal descriptor weights.
        --->QEDmax
        
        Reference:
            (1) `Bickerton, G. Richard (2012)`_.
        
        :param mols: molecules
        :type mols: Iterable
        :return: QED descriptor using maximal descriptor weights
        :rtype: list
        
        .. _Bickerton, G. Richard (2012):
            https://www.nature.com/nchem/journal/v4/n2/abs/nchem.1243.html
            
        """    
        pool = Pool(self.n_jobs)
        qed_max = pool.map_async(molproperty.CalculateQEDmax, self.mols).get()
        pool.close()
        pool.join()
        return qed_max
    
    def CalculateQEDnone(self):
        """
        Calculation QED descriptor under different weights   
        A descriptor a measure of drug-likeness based on the concept of desirability
        Here, calculating the QED descriptor using unit weights.
        --->QEDnone
        
        Reference:
            (1) `Bickerton, G. Richard (2012)`_.
        
        :param mols: molecules
        :type mols: Iterable
        :return: QED descriptor using unit weights
        :rtype: list
        
        .. _Bickerton, G. Richard (2012):
            https://www.nature.com/nchem/journal/v4/n2/abs/nchem.1243.html
            
        """    
        pool = Pool(self.n_jobs)
        qed_none = pool.map_async(molproperty.CalculateQEDnone, self.mols).get()
        pool.close()
        pool.join()
        return qed_none
    
    def CalculateMaxSizeSystemRing(self):
        """
        Number of atoms involved in the biggest system ring  
        ---> maxring
        
        :param mols: molecules
        :type mols: Iterable
        :return: number of atoms involved in the biggest system ring
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        maxring = pool.map_async(molproperty.CalculateMaxSizeSystemRing, self.mols).get()
        pool.close()
        pool.join()
        return maxring
    
    def CalculateNumStereocenters(self):
        """
        *This can not implement under multiprocessing*
        The number of stereo centers
        --->nStereo
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of stereo centers
        :rtype: list
        
        """
        nStereo = map(molproperty.CalculateNumStereocenters, self.mols)
        return list(nStereo)
        
    def CalculateNumCarbon(self):
        """
        Calculation of Carbon number in a molecule    
        --->nC
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of carbon atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nC = pool.map_async(molproperty.CalculateNumCarbon, self.mols).get()
        pool.close()
        pool.join()
        return nC
    
    def CalculateNumBoron(self):
        """
        Calculation of Boron counts in a molecule  
        --->nB
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of boron atoms
        :rtype: list
        
        """       
        pool = Pool(self.n_jobs)
        nB = pool.map_async(molproperty.CalculateNumBoron, self.mols).get()
        pool.close()
        pool.join()
        return nB
    
    def CalculateNumFluorin(self):
        """
        Calculation of Fluorin counts in a molecule  
        --->nF
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of fluori atoms
        :rtype: list
        
        """         
        pool = Pool(self.n_jobs)
        nF = pool.map_async(molproperty.CalculateNumFluorin, self.mols).get()
        pool.close()
        pool.join()
        return nF
    
    def CalculateNumChlorin(self):
        """
        Calculation of Chlorin counts in a molecule
        --->nCl
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of chlorin atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nCl = pool.map_async(molproperty.CalculateNumChlorin, self.mols).get()
        pool.close()
        pool.join()
        return nCl
    
    def CalculateNumBromine(self):
        """
        Calculation of Bromine counts in a molecule  
        --->nBr
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of bromine atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nBr = pool.map_async(molproperty.CalculateNumBromine, self.mols).get()
        pool.close()
        pool.join()
        return nBr
    
    def CalculateNumIodine(self):
        """
        Calculation of Iodine counts in a molecule 
        --->nI
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of bromine atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nI = pool.map_async(molproperty.CalculateNumIodine, self.mols).get()
        pool.close()
        pool.join()
        return nI
    
    def CalculateNumPhosphor(self):
        """
        Calcualtion of Phosphor number in a molecule
        --->nP
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of phosphor atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nP = pool.map_async(molproperty.CalculateNumPhosphor, self.mols).get()
        pool.close()
        pool.join()
        return nP
    
    def CalculateNumSulfur(self):
        """
        Calculation of Sulfur counts in a molecule  
        --->nS
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of sulfur atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nS = pool.map_async(molproperty.CalculateNumSulfur, self.mols).get()
        pool.close()
        pool.join()
        return nS
    
    def CalculateNumOxygen(self):
        """
        Calculation of Oxygen counts in a molecule    
        --->nO
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of oxygen atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nO = pool.map_async(molproperty.CalculateNumOxygen, self.mols).get()
        pool.close()
        pool.join()
        return nO
            
    def CalculateNumNitrogen(self):
        """
        Calculation of Nitrogen counts in a molecule
        --->nN
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of nitrogen atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nN = pool.map_async(molproperty.CalculateNumNitrogen, self.mols).get()
        pool.close()
        pool.join()
        return nN
    
    def CalculateNumChargedGroups(self):
        """
        Number of Charged Groups 
        --->nChar
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of charged group
        :rtype: list
        
        """
        pass
      
    def CalculateHetCarbonRatio(self):
        """
        The ratio between the number of non carbon atoms and the number of carbon atoms.
        --->HetRatio
        
        :param mols: molecules
        :type mols: Iterable
        :return: the ratio between the number of non carbon atoms and the number of carbon atoms
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        HetRatio = pool.map_async(molproperty.CalculateHetCarbonRatio, self.mols).get()
        pool.close()
        pool.join()
        return HetRatio
        
    def CalculateSAscore(self):
        """
        A function to estimate ease of synthesis (synthetic accessibility) of drug-like molecules
        --->SAscore
        
        Reference:
            (1) `Ertl, Peter, and Ansgar Schuffenhauer (2009)`_.
            
        :param mols: molecules
        :type mols: Iterable
        :return: ease of synthesis
        :rtype: list
        
        .. _Ertl, Peter, and Ansgar Schuffenhauer (2009):
            https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-1-8
            
        """
        pool = Pool(self.n_jobs)
        SA = pool.map_async(molproperty.CalculateSAscore, self.mols).get()
        pool.close()
        pool.join()
        return SA
    
    def CalculateNPscore(self):
        """
        A function to calculate the natural product-likeness score
        --->NPscore
        
        Reference:
            (1) `Ertl (2008)`_.
        
        :param mols: molecules
        :type mols: Iterable
        :return: product-likeness score
        :rtype: list
        
        .. _Ertl (2008):
            https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-1-8
            
        """
        pool = Pool(self.n_jobs)
        NP = pool.map_async(molproperty.CalculateNPscore, self.mols).get()
        pool.close()
        pool.join()
        return NP
            
    def CalculateMolVolume(self):
        """
        Calculation of Van der Waals Volume of molecule
        --->MV
        
        Equation: 
            for single atom: Vw = 4/3*pi*rw^3, the rw is the Van der Waals radius of atom
            VvdW = ∑(atom contributions)-5.92NB(Unit in Å^3), NB is the total number of bonds
            the Van der Waals radius of atom is derived from wikipedia.
            
        :param mols: molecules
        :type mols: Iterable
        :return: Van der Waals Volume of molecule
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        mv = pool.map_async(molproperty.CalculateMolVolume, self.mols).get()
        pool.close()
        pool.join()
        return mv
    
    def CalculateMolDensity(self):
        """
        Calculation of density of molecule
        --->Dense
        
        :param mols: molecules
        :type mols: Iterable
        :return: density of molecule
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        md = pool.map_async(molproperty.CalculateMolDensity, self.mols).get()
        pool.close()
        pool.join()
        return md
    
    def CalculateMolFCharge(self):
        """
        Calculation of formal charge of molecule
        --->fChar
        
        :param mols: molecules
        :type mols: Iterable
        :return: formal charge of molecule
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        fChar = pool.map_async(molproperty.CalculateMolFCharge, self.mols).get()
        pool.close()
        pool.join()
        return fChar
    
    def CalculateNumSinBond(self):
        """
        Calculation of single bond number of molecule
        --->nSingle
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of single bond
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nSingle = pool.map_async(molproperty.CalculateNumSinBond, self.mols).get()
        pool.close()
        pool.join()
        return nSingle
    
    def CalculateNumDouBond(self):
        """
        Calculation of double bond number of molecule
        --->nDouble
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of double bond
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nDouble = pool.map_async(molproperty.CalculateNumDouBond, self.mols).get()
        pool.close()
        pool.join()
        return nDouble
    
    def CalculateNumTriBond(self):
        """
        Calculation of triple bond number of molecule
        ---> nTriple
        
        :param mols: molecules
        :type mols: Iterable
        :return: the number of triple bond
        :rtype: list
        
        """
        pool = Pool(self.n_jobs)
        nTriple = pool.map_async(molproperty.CalculateNumTriBond, self.mols).get()
        pool.close()
        pool.join()
        return nTriple

    def GetProperties(self,
                      items = ['MW','Vol','Dense','fChar','nBond','nAtom','nHD','nHA','nHB',
                               'nHet','nStereo','nHev','nRot','nRig','nRing','Flex',
                               'logP','logD','pKa','logSw','ab','MR','TPSA','AP','HetRatio',
                               'Fsp3','MaxRing','QEDmean','QEDmax','QEDnone','SAscore','NPscore',
                               'nSingle','nDouble','nTriple','nC','nB','nF','nCl','nBr','nI',
                               'nP','nS','nO','nN'
                               ],
                      showSMILES = False):
        """
        Get all PC - properties in scopy
        
        """
        funcl = {'MW': 'self.CalculateMolWeight()',
                'Vol': 'self.CalculateMolVolume()',
                'Dense': 'self.CalculateMolDensity()',
                'fChar': 'self.CalculateMolFCharge()',
                'nBond': 'self.CalculateNumBonds()',
                'nAtom': 'self.CalculateNumAtoms()',
                'nHet': 'self.CalculateNumHetero()',
                'nRot': 'self.CalculateNumRotatableBonds()',
                'nRig': 'self.CalculateNumRigidBonds()',
                'nRing': 'self.CalculateNumRing()',
                'nHev': 'self.CalculateNumHeavyAtom()',
                'logP': 'self.CalculateLogP()',
                'logD': 'self.CalculateLogD()',
                'pKa': 'self.CalculatepKa()',
                'ab': 'self.CheckAcid()',
                'MR': 'self.CalculateMolMR()',
                'nHD': 'self.CalculateNumHDonors()',
                'nHA': 'self.CalculateNumHAcceptors()',
                'nHB': 'self.CalculateNumHyBond()',
                'AP': 'self.CalculateAromaticProportion()',
                'logSw': 'self.CalculateLogSw()',
                'Fsp3': 'self.CalculateFsp3()',
                'TPSA': 'self.CalculateTPSA()',
                'MaxRing': 'self.CalculateMaxSizeSystemRing()',
                'nStereo': 'self.CalculateNumStereocenters()',
                'Flex': 'self.CalculateFlexibility()',
                'HetRatio': 'self.CalculateHetCarbonRatio()',
                'QEDmean': 'self.CalculateQEDmean()',
                'QEDmax': 'self.CalculateQEDmax()',
                'QEDnone': 'self.CalculateQEDnone()',
                'SAscore': 'self.CalculateSAscore()',
                'NPscore': 'self.CalculateNPscore()',
                'nSingle': 'self.CalculateNumSinBond()',
                'nDouble': 'self.CalculateNumDouBond()',
                'nTriple': 'self.CalculateNumTriBond()',
                'nC': 'self.CalculateNumCarbon()',
                'nB': 'self.CalculateNumBoron()',
                'nF': 'self.CalculateNumFluorin()',
                'nCl': 'self.CalculateNumChlorin()',
                'nBr': 'self.CalculateNumBromine()',
                'nI': 'self.CalculateNumIodine()',
                'nP': 'self.CalculateNumPhosphor()',
                'nS': 'self.CalculateNumSulfur()',
                'nO': 'self.CalculateNumOxygen()',
                'nN': 'self.CalculateNumNitrogen()',}
        
    
        vals = []
        for item in items:
            val = eval(funcl[item])
            vals.append(val)
        
        if showSMILES:
            pool = Pool(self.n_jobs)
            smis = pool.map_async(_GetSmi, self.mols).get()
            pool.close()
            pool.join()
            
            items.insert(0, 'SMILES')
            vals.insert(0, smis)

        return dict(zip(items, vals))
    
    
if '__main__' == __name__:
    smis = [
            'C1=CC=CC(C(Br)C)=C1',
            'C1=CC2NC(=O)CC3C=2C(C(=O)C2C=CC=CC=23)=C1',
            'C1=CC=C2C(=O)C3C=CNC=3C(=O)C2=C1',
            'C1=NC(CCN)=CN1',
            'C1CCCC(CCO)C1',
            'C1=CC=C2N=C(O)C=CC2=C1',
            'C(OC)1=C(C)C=C2OC[C@]([H])3OC4C(C)=C(OC)C=CC=4C(=O)[C@@]3([H])C2=C1C',
            'C1=C2N=CC=NC2=C2N=CNC2=C1',
            'C1=C(O)C=CC(O)=C1',
            'CCC1(c2ccccc2)C(=O)NC(=O)NC1=O',
            'N1=CN=CN=C1',
            'C1=C2C=CC=CC2=CC2C=CC=CC1=2', #NonGenotoxic_Carcinogenicity
            'C1=CC=C2C(=O)CC(=O)C2=C1', #Pains
            'C1=CC=CC(COCO)=C1', #Potential_Electrophilic
            'N1=NC=CN1C=O', #Promiscuity
            'CC(=O)OC(=O)C1C=COC1', #Skin_Sensitization
            'S',
            'CCCCC(=O)[H]', #Biodegradable
            'C1=CN=C(C(=O)O)C=C1', #Chelating
            'C(OC)1=CC=C2OCC3OC4C=C(OC)C=CC=4C(=O)C3C2=C1',
            'C1=C2N=CC=NC2=C2N=CNC2=C1', #Genotoxic_Carcinogenicity_Mutagenicity
            'N(CC)(CCCCC)C(=S)N', #Idiosyncratic
            ]
    mols = [Chem.MolFromSmiles(smi) for smi in smis]
    pc = PC_properties(mols, n_jobs=4)
    res = pc.GetProperties()
    print(res)