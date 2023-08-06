# -*- coding: utf-8 -*-

#Created on Wed Nov 20 15:08:41 2019
#
#@Author: Zhi-Jiang Yang, Dong-Sheng Cao
#@Institution: CBDD Group, Xiangya School of Pharmaceutical Science, CSU, China
#@Homepage: http://www.scbdd.com
#@Mail: yzjkid9@gmail.com; oriental-cds@163.com
#@Blog: https://blog.moyule.me



import os
import shutil
from subprocess import run
from .. import ScoConfig

   
def ShowMcloud(file, number=150, skip=0, savedir=None, hidden=False):
    """Visualization of large molecular data sets using the Molecule Cloud approach. 
    
    Reference:
        (1) `P. Ertl, B. Rohde (2012)`_.
        
    :param file: the absolute path of file whose first column is the SMILES, and second one is frequnency correspondly. Delimit is '\t'
    :type file: str
    :param number: process only first n molecules from the data file, defaults to 150
    :type number: int, optional
    :param skip: skip first n structures (usually used 1 to skip large phenyl), defaults to 0
    :type skip: int, optional
    :param savedir: the path to save figure, defaults to None
    :type savedir: str, optional
    :param hidden: whether hidden the figure after finished, defaults to False
    :type hidden: bool, optional
    :return: None
    
    .. _P. Ertl, B. Rohde (2012):
        https://jcheminf.biomedcentral.com/articles/10.1186/1758-2946-4-12
        
    """
    i = '-i' if savedir else ''
    nogui = '-nogui' if hidden else ''
    
    path = ScoConfig.MCDir
    
    command = 'cd /d {}\mcloud && \
    java -cp ".;depictjni.jar;depict.jar" ertl/mcloud/MCloud\
    -f {} -n {} -skip {} {} {}'.format(path, file, number, skip, i, nogui)
    
    run(command,shell=True)

    if savedir is not None:
        try:
            shutil.move(os.path.join(ScoConfig.MCDir,'mcloud\mcloud.png'), savedir)
        except:
            pass
    else:
        pass
    
if '__main__'==__name__:
    ShowMcloud(r"scaffolds.smi", savedir=r"mcloud.png")
    
    
    
    
    