#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 08:28 2023

@author: rjjt
"""

import sys
import os
import argparse
import pandas as pd

from Part import *
import PartDB

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

ITEM = 'Item'
QUANTITY = 'Quantity'
REFERENCE = 'Reference'
PART = 'Part'
ASSEMBLY = 'Assembly'
PCB_FOOTPRINT = 'PCB Footprint'
CEPHA_PN = 'Cepha PN'
MFR = 'MFR'
MPN = 'MPN'
MFR2 = 'MFR2'
MPN2 = 'MPN2'


def importBOM(bom_file, first_row=0):
  db = PartDB.PartDB(db_url)
  if first_row > 0:
    bom = pd.read_csv(bom_file, skiprows=first_row-1)
  else:
    bom = pd.read_csv(bom_file)

  bom = bom.dropna(subset=[ITEM, QUANTITY])
  for i, row in bom.iterrows():
    print("Importing BOM item %s: %s" % (row[ITEM], row[PART]))
    part = db.get_part_by_name(row[PART])
    if part is None:
      print("Part %s not found" % row[PART])
      continue
    print("Found part %s" % part.name)
    print("Adding BOM item %s: %s" % (row[ITEM], row[PART]))
    bom_item = BOMItem(
        item=row[ITEM],
        quantity=row[QUANTITY],
        reference=row[REFERENCE],
        part=part.id,
        assembly=row[ASSEMBLY],
        pcb_footprint=row[PCB_FOOTPRINT],
        cepha_pn=row[CEPHA_PN],
        mfr=row[MFR],
        mpn=row[MPN],
        mfr2=row[MFR2],
        mpn2=row[MPN2]
    )
    db.add(bom_item)
