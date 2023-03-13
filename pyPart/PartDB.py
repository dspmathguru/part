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

  def add_part(self, part):
    self.session.add(part)
    self.session.commit() 
  
  def get_part(self, id): 
    return self.session.query(Part).get(id)
  
  def get_all_parts(self):
    return self.session.query(Part).all()
  
  def get_all_parts_by_footprint(self, footprint):  
    return self.session.query(Part).filter(Part.footprint == footprint).all()
  
  def get_all_parts_by_manufacturer(self, manufacturer):
    return self.session.query(Part).filter(Part.manufacturer == manufacturer).all() 
  
  def get_all_parts_by_distributor(self, distributor):
    return self.session.query(Part).filter(Part.distributor == distributor).all()
  
  def add_footprint(self, footprint):
    self.session.add(footprint)
    self.session.commit()
  
  def get_footprint(self, id):
    return self.session.query(Footprint).get(id)  
  
  def get_all_footprints(self):
    return self.session.query(Footprint).all()  
  
  def add_company(self, company):
    self.session.add(company)
    self.session.commit()

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


