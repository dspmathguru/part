import { PrismaClient, usertype } from '@prisma/client'

const prisma = new PrismaClient()

async function create() {
  await prisma.user.create({
    data: {
      username: "rjjt",
      password: "test",
      phone: "(408) 858-4007",
      email: "rjjt@cephasonics.com",
      role: "admin",
      user_type: usertype.ADMIN,
      created: new Date(),
      updated: new Date()
    },
  })

  const allUsers = await prisma.user.findMany()
  console.dir(allUsers, { depth: null })
}

async function main() {
  const post = await prisma.user.update({
    where: { id: 1 },
    data: { 
      role: 'cool dudes are us',
      updated: new Date()
    },
  })

  const allUsers = await prisma.user.findMany()
  console.dir(allUsers, { depth: null })
}


main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })
