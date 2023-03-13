#! /usr/bin/env python

from dotenv import load_dotenv
import os

import PartDB
import Part

load_dotenv()

db = PartDB.PartDB(os.getenv("DATABASE_URL"))

# Add a footprint
footprint = PartDB.Footprint(name="SOT-23-5")
db.add_footprint(footprint)

# Add a manufacturer
manufacturer = PartDB.Manufacturer(name="Texas Instruments")

# Add a distributor
distributor = PartDB.Distributor(name="Digikey")

# Add a part type
part_type = PartDB.PartType(name="Op Amp")

# Add a part
part = PartDB(Part.Part(
  name="LMV321IDBVR",
  part_type=part_type,
  description="Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3V, 5V, 8-Bit, 2.5V to 5.5V, Rail-to-Rail Output, Single Supply, Low Power, Low Noise, 1.8V, 3.3",
  manufacturer=manufacturer,
  distributor=distributor,
  footprint=footprint,
  quantity=100,
  price=0.25,
  url="https://www.digikey.com/product-detail/en/texas-instruments/LMV321IDBVR/296-10083-5-ND/1000000",
  notes="This is a note"
))