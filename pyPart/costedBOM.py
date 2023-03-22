#! /usr/bin/env python

import sys
import os
import argparse

import pandas as pd
import datetime

from Part import *
import PartDB

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")

date_string = f'{datetime.now():%Y-%m-%d}'

def costedBOM(bom_name, bom_version):
  db = PartDB.PartDB(db_url)
  costed_bom = {}
  bom = db.get_bom_by_name_and_version(bom_name, bom_version)
  if bom is None:
    print("BOM %s version %s not found" % (bom_name, bom_version))
    return
  print("BOM:", bom.name, bom.version)
  costed_bom['name'] = bom.name
  costed_bom['version'] = bom.version

  bom_items = db.get_bom_items_by_bom_id(bom.id)

  costed_bom['items'] = []
  for item in bom_items:
    print("Item:", item.bom_id, item.quantity, item.reference, item.assembly)
    part = db.get_part_by_id(item.part_id)
    print("part:", part.id, part.cspnold, part.description)
    distributor_parts = db.get_distributor_parts_by_part_id(part.id)

    costed_item = {
        'cspnold': part.cspnold,
        'quantity': item.quantity,
        'reference': item.reference,
        'part_id': part.id,
        'distributor_parts': []
    }
    for ignore, distributor_part in distributor_parts:
      print("Distributor part:", distributor_part.pn)
      distributor = db.get_company_by_id(distributor_part.company_id)
      print("Distributor:", distributor.name)
      prices = db.get_part_prices_by_distributor_part_id(distributor_part.id)

      costed_item['distributor_parts'].append({
          'pn': distributor_part.pn,
          'distributor': distributor.name,
          'price': prices[0].price,
      })

    costed_bom['items'].append(costed_item)
  xls = pd.DataFrame(costed_bom['items'])
  for i, row in xls.iterrows():
    for j, distributor_part in enumerate(row['distributor_parts']):
      xls.at[i, 'pn%d' % j] = distributor_part['pn']
      xls.at[i, 'distributor%d' % j] = distributor_part['distributor']
      xls.at[i, 'price%d' % j] = distributor_part['price']
      xls.at[i, 'total%d' % j] = distributor_part['price'] * row['quantity']
  xls = xls.drop(columns=['distributor_parts'])
  xls.loc['Total'] = xls['total0'].sum()
  xls_file = '%s-%s-%s.xlsx' % (bom_name, bom_version, date_string)
  xls.to_excel(xls_file)


def main():
  parser = argparse.ArgumentParser(description='Costed BOM')
  parser.add_argument('bom_name', help='BOM name')
  parser.add_argument('bom_version', help='BOM version')
  args = parser.parse_args()
  costedBOM(args.bom_name, args.bom_version)


if __name__ == "__main__":
  main()
