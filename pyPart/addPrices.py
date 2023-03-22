#! /usr/bin/env python

import sys
import os
import argparse

import pandas as pd

from Part import *
import PartDB

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

def findDistributor(db, name):
  distributor = db.get_company_by_name(name)
  if distributor is None:
    distributor = Company(name=name, type=db.get_company_type_by_name("distributor"))
    db.add(distributor)
  return distributor

def getDistributorPart(db, distributor, part, manufacturer_part, distributor_pn):
  if distributor_pn is not None:
    distributor_part = db.get_distributor_part_by_pn(distributor_pn)
  else:
    distributor_part = DistributorPart(
        manufacturer_part=manufacturer_part, company_id=distributor.id, pn=part.cspnold)
    db.add(distributor_part)
  return distributor_part

def addPrices(distributor_name, xls_file, sheet_name, part_col, price_col, moq_col, manufacturer_pn_col, distributor_pn_col=None):
  db = PartDB.PartDB(db_url)
  distributor = findDistributor(db, distributor_name)
  print("Distributor:", distributor.name)
  xls = pd.read_excel(xls_file, sheet_name=sheet_name)
  xls = xls.dropna(subset=[part_col, price_col])
  for index, row in xls.iterrows():
    if float(row[price_col]) < 0.0000001:
      continue
    part = db.get_part_by_cspnold(row[part_col])
    if moq_col is not None:
      moq = int(row[moq_col])
    else:
      moq = 0
    if part is None:
      print("Part %s not found" % row[part_col])
      continue
    print("Found part %s at price %f" % (part.cspnold, row[price_col]))
    if manufacturer_pn_col:
      manufacturer_part = db.get_manufacturer_part_by_part_id_and_pn(
          part.id, row[manufacturer_pn_col])
      if manufacturer_part is None:
        print("Manufacturer part %s not found" % row[manufacturer_pn_col])
        continue
      print("Found manufacturer part %s" % manufacturer_part.pn)
      if distributor_pn_col is not None:
        distributor_pn = row[distributor_pn_col]
      else:
        distributor_pn = None
      distributor_part = getDistributorPart(
          db, distributor, part, manufacturer_part, distributor_pn)
      part_price = PartPrice(distributor_part=distributor_part,
                             price=row[price_col], moq=moq, currency="USD")
      db.add(part_price)
    else:
      print("No manufacturer part specified")

def main():
  parser = argparse.ArgumentParser(description='Add prices to parts')
  parser.add_argument('distributor', help='Distributor name')
  parser.add_argument('xls_file', help='Excel file')
  parser.add_argument('sheet_name', help='Excel sheet name')
  parser.add_argument('part_col', help='Excel column with part number')
  parser.add_argument('price_col', help='Excel column with price')
  parser.add_argument('manufacturer_pn_col', help='Excel column with manufacturer part number')
  parser.add_argument('--moq_col', help='Excel column with MOQ', default=None)
  parser.add_argument('--distributor_pn_col',
                      help='Excel column with distributor part number', default=None)
  args = parser.parse_args()
  addPrices(args.distributor, args.xls_file, args.sheet_name, args.part_col,
            args.price_col, args.moq_col, args.manufacturer_pn_col, args.distributor_pn_col)


if __name__ == "__main__":
  main()