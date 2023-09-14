import { createYoga } from 'graphql-yoga'
import { PrismaSessionStore } from '@quixo3/prisma-session-store'
import express from 'express'
import expressSession from 'express-session'
import { prisma } from './db'
import { schema } from './schema'

const yoga = createYoga({
  graphqlEndpoint: '/graphql',
  schema,
  context: (req) => {
    return {
      req,
    }
  },
})

const app = express()

app.use(
  expressSession({
   cookie: {
     maxAge: 7 * 24 * 60 * 60 * 1000 // ms
    },
    secret: "some very long string here to keep the session secure",
    resave: true,  // NOTE: read notes when true
    saveUninitialized: true,
    store: new PrismaSessionStore(
      prisma,
      {
        checkPeriod: 2 * 60 * 1000, //ms
        dbRecordIdIsSessionId: true,
        dbRecordIdFunction: undefined,
      },
    ),
  })
)

app.use(
  '/graphql',
  yoga
)

app.listen(4000, () => {
  console.log(`\
🚀 Server ready at: http://127.0.0.1:4000
  `)
})
