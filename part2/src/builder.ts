import SchemaBuilder from '@pothos/core'
import PrismaPlugin from '@pothos/plugin-prisma'
import type PrismaTypes from '@pothos/plugin-prisma/generated'
import { DateTimeResolver } from 'graphql-scalars'
import ScopeAuthPlugin from '@pothos/plugin-scope-auth'
import { prisma } from './db'

export const builder = new SchemaBuilder<{
  PrismaTypes: PrismaTypes
  Context: {
    user?: {
      id: string
      role: string
    }
  }
  Scalars: {
    DateTime: {
      Input: Date
      Output: Date
    }
  }
  AuthScopes: {
    isAuthorized: boolean
    admin: boolean
    developer: boolean
    accounting: boolean
    engineering: boolean
    sales: boolean
  }
}>({
  plugins: [PrismaPlugin, ScopeAuthPlugin],
  prisma: {
    client: prisma,
  },
  authScopes: async (ctx) => {
    const isAuthorized = ctx!.user !== undefined
    console.log('isAuthorized', isAuthorized)
    scopes: {
      isAuthorized:  isAuthorized
      admin: isAuthorized && ctx!.user!.role === 'ADMIN'
      developer: isAuthorized && ctx!.user!.role === 'DEVELOPER'
      accounting: isAuthorized && ctx!.user!.role === 'ACCOUNTING'
      engineering: isAuthorized && ctx!.user!.role === 'ENGINEERING'
      sales: isAuthorized && ctx!.user!.role === 'SALES'
    }
  },
  scopeAuthOptions: {
    authorizeOnSubscribe: true,
  }
})

builder.queryType({})
builder.mutationType({})

builder.addScalarType('DateTime', DateTimeResolver, {})
