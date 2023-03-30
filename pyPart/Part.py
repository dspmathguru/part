#! /usr/bin/env python

from datetime import datetime
import enum
from typing import List
from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

class Footprint(Base):
  __tablename__ = 'footprint'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50))
  description: Mapped[str | None] = mapped_column(String(200))

  def __repr__(self) -> str:
    return f"<Footprint(id={self.id!r}, name={self.name!r})>"

class CompanyType(Base):
  __tablename__ = 'company_type'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50))

  def __repr__(self) -> str:
    return f"<CompanyType(id={self.id!r}, name={self.name!r})>"

class Company(Base):
  __tablename__ = 'company'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50))
  company_type: Mapped[CompanyType] = mapped_column(ForeignKey("company_type.id"))
  street: Mapped[str | None] = mapped_column(String(50))
  city: Mapped[str | None] = mapped_column(String(50))
  state: Mapped[str | None] = mapped_column(String(50))
  zip: Mapped[str | None] = mapped_column(String(50))
  country: Mapped[str | None] = mapped_column(String(50))
  phone: Mapped[str | None] = mapped_column(String(50))
  email: Mapped[str | None] = mapped_column(String(50))
  website: Mapped[str | None] = mapped_column(String(50))
  contact: Mapped[str | None] = mapped_column(String(50))

  def __repr__(self) -> str:
    return f"<Company(id={self.id!r}, name={self.name!r})>"

class PartType(Base):
  __tablename__ = 'part_type'

  id: Mapped[int] = mapped_column(primary_key=True)
  type: Mapped[str] = mapped_column(String(50))
  prefix: Mapped[str] = mapped_column(String(10))
  version: Mapped[str | None] = mapped_column(String(10))
  description: Mapped[str | None] = mapped_column(String(200))

  def __repr__(self) -> str:
    return f"<PartType(id={self.id!r}, type={self.type!r}, description={self.description!r}>"

class ManufacturerPart(Base):
  __tablename__ = "manufacturer_part"

  id: Mapped[int] = mapped_column(primary_key=True)
  company: Mapped[int] = mapped_column(ForeignKey("company.id"))
  pn: Mapped[str] = mapped_column(String(50))
  part_url: Mapped[str | None] = mapped_column(String(200))
  datasheet_url: Mapped[str | None] = mapped_column(String(200))
  description: Mapped[str | None] = mapped_column(String(2000))

  part_id: Mapped[int] = mapped_column(ForeignKey("part.id"))
  parts: Mapped["Part"] = relationship(back_populates="manufacturers")

  distributors: Mapped[List["DistributorPart"]] = relationship(
      back_populates="manufacturer_part", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"<ManufacturerPart(id={self.id!r}, manufacturer={self.manufacturer!r}, pn={self.pn!r}>"

class DistributorPart(Base):
  __tablename__ = "distributor_part"

  id: Mapped[int] = mapped_column(primary_key=True)
  company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
  pn: Mapped[str] = mapped_column(String(50))
  part_url: Mapped[str | None] = mapped_column(String(200))
  manufacturer_part_id: Mapped[int] = mapped_column(ForeignKey("manufacturer_part.id"))
  manufacturer_part: Mapped[ManufacturerPart] = relationship(back_populates="distributors")
  prices: Mapped[List["PartPrice"]] = relationship(
      back_populates="distributor_part", cascade="all, delete-orphan"
  )

  def __repr__(self) -> str:
    return f"<DistributorPart(id={self.id!r}, company_id={self.company_id!r}, pn={self.pn!r}>"

class Part(Base):
  __tablename__ = 'part'

  id: Mapped[int] = mapped_column(primary_key=True)
  cspnold: Mapped[str] = mapped_column(String(50))
  cspn: Mapped[str] = mapped_column(String(50))
  manufacturers: Mapped[List[ManufacturerPart]] = relationship(
      back_populates="parts", cascade="all, delete-orphan"
  )
  footprint: Mapped[Footprint | None] = mapped_column(ForeignKey("footprint.id"))
  type: Mapped[int] = mapped_column(ForeignKey("part_type.id"))
  orcad_uri: Mapped[str | None] = mapped_column(String(50))
  description: Mapped[str | None] = mapped_column(String(2000))

  bom_items: Mapped[List['BOMItem']] = relationship(
      back_populates='part', cascade='all, delete-orphan'
  )

  def __repr__(self) -> str:
    return f"<Part(id={self.id!r}, cspnold={self.cspnold!r}, cspn={self.cspn!r}, footprint={self.footprint!r}, description={self.description!r}>"

class BOM(Base):
  __tablename__ = 'bom'

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(String(50))
  note: Mapped[str | None] = mapped_column(String(2000))
  version: Mapped[str | None] = mapped_column(String(10))
  created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
  updated: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

  items: Mapped[List['BOMItem']] = relationship(
      back_populates='item', cascade='all, delete-orphan'
  )

  def __repr__(self) -> str:
    return f'<BOM name={self.name}>'

class BOMItem(Base):
  __tablename__ = 'bom_items'

  id: Mapped[int] = mapped_column(primary_key=True)
  bom_id: Mapped[int] = mapped_column(ForeignKey("bom.id"))
  item: Mapped[BOM] = relationship(back_populates='items')
  quantity: Mapped[int] = mapped_column(Integer)
  part_id: Mapped[int] = mapped_column(ForeignKey("part.id"))
  part: Mapped[Part] = relationship(back_populates='bom_items')
  reference: Mapped[str] = mapped_column(String(2000))
  assembly: Mapped[str | None] = mapped_column(String(50))
  note: Mapped[str | None] = mapped_column(String(2000))

  def __repr__(self) -> str:
    return f'<BOMItem id={self.id}, bom_id={self.bom_id}>'

class PartPrice(Base):
  __tablename__ = 'part_price'

  id: Mapped[int] = mapped_column(primary_key=True)
  moq: Mapped[int] = mapped_column(Integer)
  price: Mapped[float] = mapped_column(Float)
  currency: Mapped[str] = mapped_column(String(3))
  distributor_part: Mapped[DistributorPart] = relationship(back_populates='prices')
  distributor_part_id: Mapped[int] = mapped_column(ForeignKey("distributor_part.id"))
  created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
  updated: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __repr__(self) -> str:
    return f'<PartPrice id={self.id}, distributor_part_id={self.distributor_part_id}>'


class UserType(enum.Enum):
  ADMIN = 'admin'
  DEVELOPER = 'developer'
  OPERATIONS = 'operations'
  ACCOUNTING = 'accounting'
  ENGINEERING = 'engineering'
  SALES = 'sales'

class User(Base):
  __tablename__ = 'user'

  id: Mapped[int] = mapped_column(primary_key=True)
  username: Mapped[str] = mapped_column(String(50))
  password: Mapped[str] = mapped_column(String(2048))
  phone: Mapped[str] = mapped_column(String(50))
  email: Mapped[str] = mapped_column(String(50))
  role: Mapped[str] = mapped_column(String(50))
  user_type: Mapped[UserType] = mapped_column(Enum(UserType))
  product_key: Mapped[str | None] = mapped_column(String(50))
  created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
  updated: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __repr__(self) -> str:
    return f'<User id={self.id}, username={self.username}>'
