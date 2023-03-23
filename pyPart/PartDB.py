#! /usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from Part import *

class PartDB:
  def __init__(self, db):
    self.db = db
    print('db:', db)
    self.engine = create_engine(db)
    self.session = Session(self.engine)

    Base.metadata.create_all(self.engine)

  def add(self, part):
    self.session.add(part)
    self.session.commit()

  def delete(self, part):
    self.session.delete(part)
    self.session.commit()

  def get_company_type(self, id):
    return self.session.query(CompanyType).get(id)

  def get_all_company_types(self):
    return self.session.query(CompanyType).all()

  def get_company_type_by_name(self, name):
    return self.session.query(CompanyType).filter(CompanyType.name == name).first()

  def get_part(self, id):
    return self.session.query(Part).get(id)

  def get_all_parts(self):
    return self.session.query(Part).all()

  def get_all_parts_by_type(self, type):
    return self.session.query(Part).filter(Part.type == type).all()

  def get_part_type(self, id):
    return self.session.query(PartType).get(id)

  def get_part_type_by_type(self, type):
    return self.session.query(PartType).filter(PartType.type == type).first()

  def get_all_part_types(self):
    return self.session.query(PartType).all()

  def get_all_parts_by_footprint(self, footprint):
    return self.session.query(Part).filter(Part.footprint == footprint).all()

  def get_all_parts_by_manufacturer(self, manufacturer):
    return self.session.query(Part).filter(Part.manufacturer == manufacturer).all()

  def get_all_parts_by_distributor(self, distributor):
    return self.session.query(Part).filter(Part.distributor == distributor).all()

  def get_part_by_cspnold(self, cspnold):
    return self.session.query(Part).filter(Part.cspnold == str(cspnold)).first()

  def get_part_by_cspn(self, cspn):
    return self.session.query(Part).filter(Part.cspn == cspn).first()

  def get_footprint(self, id):
    return self.session.query(Footprint).get(id)

  def get_all_footprints(self):
    return self.session.query(Footprint).all()

  def get_company(self, id):
    return self.session.query(Company).get(id)

  def get_all_companies(self):
    return self.session.query(Company).all()

  def add_distributor_part(self, distributor_part):
    self.session.add(distributor_part)
    self.session.commit()

  def get_distributor_part(self, id):
    return self.session.query(DistributorPart).get(id)

  def get_all_distributor_parts(self):
    return self.session.query(DistributorPart).all()

  def add_manufacturer_part(self, manufacturer_part):
    self.session.add(manufacturer_part)
    self.session.commit()

  def get_manufacturer_part(self, id):
    return self.session.query(ManufacturerPart).get(id)

  def get_all_manufacturer_parts(self):
    return self.session.query(ManufacturerPart).all()

  def get_company_by_name(self, name):
    return self.session.query(Company).filter(Company.name == name).first()

  def get_bom_by_name_version(self, name, version):
    return self.session.query(BOM).filter(BOM.name == name).filter(BOM.version == version).first()

  def get_all_manufacturer_parts_by_part_id(self, part_id):
    return self.session.query(ManufacturerPart).filter(ManufacturerPart.part_id == part_id).all()

  def get_company_by_id(self, id):
    return self.session.query(Company).filter(Company.id == id).first()

  def get_manufacturer_part_by_part_id_and_pn(self, part_id, pn):
    return self.session.query(ManufacturerPart).filter(ManufacturerPart.part_id == part_id).filter(ManufacturerPart.pn == pn).first()

  def get_bom_by_name_and_version(self, name, version):
    return self.session.query(BOM).filter(BOM.name == name).filter(BOM.version == version).first()

  def get_bom_items_by_bom_id(self, bom_id):
    return self.session.query(BOMItem).filter(BOMItem.bom_id == bom_id).all()

  def get_part_by_id(self, id):
    return self.session.query(Part).filter(Part.id == id).first()

  def get_distributor_parts_by_part_id(self, part_id):
    query = self.session.query(ManufacturerPart.part_id, DistributorPart).join(DistributorPart)
    return query.filter(ManufacturerPart.part_id == part_id).all()

  def get_part_prices_by_distributor_part_id(self, distributor_part_id):
    return self.session.query(PartPrice).filter(PartPrice.distributor_part_id == distributor_part_id).all()

  def get_manufacturer_part_by_id(self, id):
    return self.session.query(ManufacturerPart).filter(ManufacturerPart.id == id).first()
