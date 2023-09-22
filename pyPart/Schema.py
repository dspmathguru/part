import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

from Part import Footprint as FootprintModel
from Part import CompanyType as CompanyTypeModel
from Part import Company as CompanyModel
from Part import PartType as PartTypeModel
from Part import ManufacturerPart as ManufacturerPartModel
from Part import DistributorPart as DistributorPartModel
from Part import Part as PartModel
from Part import BOM as BOMModel
from Part import BOMItem as BOMItemModel
from Part import PartPrice as PartPriceModel
from Part import User as UserModel

class FootPrint(SQLAlchemyObjectType):
  class Meta:
    model = FootprintModel
    interfaces = (relay.Node, )

class CompanyType(SQLAlchemyObjectType):
  class Meta:
    model = CompanyTypeModel
    interfaces = (relay.Node, )

class Company(SQLAlchemyObjectType):
  class Meta:
    model = CompanyModel
    interfaces = (relay.Node, )

class PartType(SQLAlchemyObjectType):
  class Meta:
    model = PartTypeModel
    interfaces = (relay.Node, )

class ManufacturerPart(SQLAlchemyObjectType):
  class Meta:
    model = ManufacturerPartModel
    interfaces = (relay.Node, )

class DistributorPart(SQLAlchemyObjectType):
  class Meta:
    model = DistributorPartModel
    interfaces = (relay.Node, )

class Part(SQLAlchemyObjectType):
  class Meta:
    model = PartModel
    interfaces = (relay.Node, )

class BOM(SQLAlchemyObjectType):
  class Meta:
    model = BOMModel
    interfaces = (relay.Node, )

class BOMItem(SQLAlchemyObjectType):
  class Meta:
    model = BOMItemModel
    interfaces = (relay.Node, )

class PartPrice(SQLAlchemyObjectType):
  class Meta:
    model = PartPriceModel
    interfaces = (relay.Node, )

class User(SQLAlchemyObjectType):
  class Meta:
    model = UserModel
    interfaces = (relay.Node, )

class Query(graphene.ObjectType):
  node = relay.Node.Field()
  # Allows sorting over multiple columns, by default over the primary key
  all_users = SQLAlchemyConnectionField(User.connection)
  all_parts = SQLAlchemyConnectionField(Part.connection)
  all_boms = SQLAlchemyConnectionField(BOM.connection)
  all_bom_items = SQLAlchemyConnectionField(BOMItem.connection)
  all_part_prices = SQLAlchemyConnectionField(PartPrice.connection)
  all_footprints = SQLAlchemyConnectionField(FootPrint.connection)
  all_company_types = SQLAlchemyConnectionField(CompanyType.connection)
  all_companies = SQLAlchemyConnectionField(Company.connection)
  all_part_types = SQLAlchemyConnectionField(PartType.connection)
  all_manufacturer_parts = SQLAlchemyConnectionField(ManufacturerPart.connection)
  all_distributor_parts = SQLAlchemyConnectionField(DistributorPart.connection)


schema = graphene.Schema(query=Query,
                         types=[User, Part, BOM, BOMItem, PartPrice, FootPrint, CompanyType, Company,
                                PartType, ManufacturerPart, DistributorPart])
