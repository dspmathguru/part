-- CreateEnum
CREATE TYPE "usertype" AS ENUM ('ADMIN', 'DEVELOPER', 'OPERATIONS', 'ACCOUNTING', 'ENGINEERING', 'SALES');

-- CreateTable
CREATE TABLE "bom" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "note" VARCHAR(2000),
    "version" VARCHAR(10),
    "created" TIMESTAMP(6) NOT NULL,
    "updated" TIMESTAMP(6) NOT NULL,

    CONSTRAINT "bom_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "bom_items" (
    "id" SERIAL NOT NULL,
    "bom_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,
    "part_id" INTEGER NOT NULL,
    "reference" VARCHAR(2000) NOT NULL,
    "assembly" VARCHAR(50),
    "note" VARCHAR(2000),

    CONSTRAINT "bom_items_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "company" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "company_type" INTEGER NOT NULL,
    "street" VARCHAR(50),
    "city" VARCHAR(50),
    "state" VARCHAR(50),
    "zip" VARCHAR(50),
    "country" VARCHAR(50),
    "phone" VARCHAR(50),
    "email" VARCHAR(50),
    "website" VARCHAR(50),
    "contact" VARCHAR(50),

    CONSTRAINT "company_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "company_type" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(50) NOT NULL,

    CONSTRAINT "company_type_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "distributor_part" (
    "id" SERIAL NOT NULL,
    "company_id" INTEGER NOT NULL,
    "pn" VARCHAR(50) NOT NULL,
    "part_url" VARCHAR(200),
    "manufacturer_part_id" INTEGER NOT NULL,

    CONSTRAINT "distributor_part_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "footprint" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200),

    CONSTRAINT "footprint_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "manufacturer_part" (
    "id" SERIAL NOT NULL,
    "company" INTEGER NOT NULL,
    "pn" VARCHAR(50) NOT NULL,
    "part_url" VARCHAR(200),
    "datasheet_url" VARCHAR(200),
    "description" VARCHAR(2000),
    "part_id" INTEGER NOT NULL,

    CONSTRAINT "manufacturer_part_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "part" (
    "id" SERIAL NOT NULL,
    "cspnold" VARCHAR(50) NOT NULL,
    "cspn" VARCHAR(50) NOT NULL,
    "footprint" INTEGER,
    "type" INTEGER NOT NULL,
    "orcad_uri" VARCHAR(50),
    "description" VARCHAR(2000),

    CONSTRAINT "part_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "part_price" (
    "id" SERIAL NOT NULL,
    "moq" INTEGER NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "currency" VARCHAR(3) NOT NULL,
    "distributor_part_id" INTEGER NOT NULL,
    "created" TIMESTAMP(6) NOT NULL,
    "updated" TIMESTAMP(6) NOT NULL,

    CONSTRAINT "part_price_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "part_type" (
    "id" SERIAL NOT NULL,
    "type" VARCHAR(50) NOT NULL,
    "prefix" VARCHAR(10) NOT NULL,
    "version" VARCHAR(10),
    "description" VARCHAR(200),

    CONSTRAINT "part_type_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "user" (
    "id" SERIAL NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "password" VARCHAR(2048) NOT NULL,
    "phone" VARCHAR(50) NOT NULL,
    "email" VARCHAR(50) NOT NULL,
    "role" VARCHAR(50) NOT NULL,
    "user_type" "usertype" NOT NULL,
    "product_key" VARCHAR(50),
    "created" TIMESTAMP(6) NOT NULL,
    "updated" TIMESTAMP(6) NOT NULL,

    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "session" (
    "id" VARCHAR NOT NULL,
    "sid" VARCHAR(50) NOT NULL,
    "data" VARCHAR(2048) NOT NULL,
    "expiresAt" TIMESTAMP(6) NOT NULL,

    CONSTRAINT "session_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "session_sid_key" ON "session"("sid");

-- AddForeignKey
ALTER TABLE "bom_items" ADD CONSTRAINT "bom_items_bom_id_fkey" FOREIGN KEY ("bom_id") REFERENCES "bom"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "bom_items" ADD CONSTRAINT "bom_items_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "part"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "company" ADD CONSTRAINT "company_company_type_fkey" FOREIGN KEY ("company_type") REFERENCES "company_type"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "distributor_part" ADD CONSTRAINT "distributor_part_company_id_fkey" FOREIGN KEY ("company_id") REFERENCES "company"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "distributor_part" ADD CONSTRAINT "distributor_part_manufacturer_part_id_fkey" FOREIGN KEY ("manufacturer_part_id") REFERENCES "manufacturer_part"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "manufacturer_part" ADD CONSTRAINT "manufacturer_part_company_fkey" FOREIGN KEY ("company") REFERENCES "company"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "manufacturer_part" ADD CONSTRAINT "manufacturer_part_part_id_fkey" FOREIGN KEY ("part_id") REFERENCES "part"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "part" ADD CONSTRAINT "part_footprint_fkey" FOREIGN KEY ("footprint") REFERENCES "footprint"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "part" ADD CONSTRAINT "part_type_fkey" FOREIGN KEY ("type") REFERENCES "part_type"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- AddForeignKey
ALTER TABLE "part_price" ADD CONSTRAINT "part_price_distributor_part_id_fkey" FOREIGN KEY ("distributor_part_id") REFERENCES "distributor_part"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

