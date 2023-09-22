#! /usr/bin/env python

from datetime import datetime
import os
import sys
import argparse

import pandas as pd
import PartDB
import Part

import dotenv

dotenv.load_dotenv()

db_url = os.getenv("DATABASE_URL")
company_name = os.getenv("COMPANY_NAME")
company_street = os.getenv("COMPANY_STREET")
company_city = os.getenv("COMPANY_CITY")
company_state = os.getenv("COMPANY_STATE")
company_zip = os.getenv("COMPANY_ZIP")
company_country = os.getenv("COMPANY_COUNTRY")
company_phone = os.getenv("COMPANY_PHONE")
company_email = os.getenv("COMPANY_EMAIL")
company_website = os.getenv("COMPANY_WEBSITE")
company_logo = os.getenv("COMPANY_LOGO")
company_contact = os.getenv("COMPANY_CONTACT")

date_string = f'{datetime.now():%Y-%m-%d}'


def createRFQ(boms, name, version, system_qty):
  db = PartDB.PartDB(db_url)

  all_parts = dict()
  max_manu_pns = 0
  for bom_arg in boms:
    bom = db.get_bom_by_name_version(bom_arg[0], bom_arg[1])
    bom_qty = int(bom_arg[2])
    if bom is None:
      print("BOM %s not found" % bom_arg[0])
      continue
    print("Found BOM %s" % bom.name)

    for item in bom.items:
      if item.reference == 'DNI':
        continue

      print("Adding RFQ item %s: %s" % (item.part.cspnold, item.part.description))
      qty = int(item.quantity) * bom_qty * system_qty
      part_id = item.part.id
      cspnold = item.part.cspnold
      manufacturers = db.get_all_manufacturer_parts_by_part_id(part_id)
      if len(manufacturers) == 0:
        print("No manufacturers found for part %s" % cspnold)
        continue
      manu_pns = []
      for manufacturer in manufacturers:
        company = db.get_company_by_id(manufacturer.company_id).name
        manu_pns.append((company, manufacturer.pn))
      if len(manu_pns) > max_manu_pns:
        max_manu_pns = len(manu_pns)

      if cspnold in all_parts:
        all_parts[cspnold]['qty'] += qty
      else:
        all_parts[cspnold] = {
            'qty': qty,
            'manu_pns': manu_pns,
            'description': item.part.description
        }

  if len(all_parts) == 0:
    print("No parts found")
    return

  xls = pd.DataFrame(all_parts).T
  xls['qty'] = xls['qty'].astype(int)
  xls['description'] = xls['description'].astype(str)
  for i in range(max_manu_pns):
    xls['Manufacturer %d' % (i+1)] = ''
    xls['Manufacturer Part Number %d' % (i+1)] = ''
  for i, row in xls.iterrows():
    for j, manu_pn in enumerate(row['manu_pns']):
      xls.at[i, 'Manufacturer %d' % (j+1)] = manu_pn[0]
      xls.at[i, 'Manufacturer Part Number %d' % (j+1)] = manu_pn[1]
  xls = xls.drop(columns=['manu_pns'])
  xls_name = '%s-%s-%s.xlsx' % (name, version, date_string)
  xls.to_excel(xls_name, index_label='CSPNOLD')

  print("Created %s" % xls_name)


def main():
  parser = argparse.ArgumentParser(description='Create a new RFQ')
  parser.add_argument('name', help='RFQ name')
  parser.add_argument('version', help='RFQ version')
  parser.add_argument('qty', help='RFQ quantity', type=int)
  parser.add_argument('boms', help='bom version qty bom version qty ...', nargs='+')

  args = parser.parse_args()

  boms = [(a, b, int(c)) for a, b, c in zip(args.boms[0::3], args.boms[1::3], args.boms[2::3])]
  print(boms)
  createRFQ(boms, args.name, args.version, args.qty)


if __name__ == '__main__':
  main()
