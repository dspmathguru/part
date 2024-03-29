import bcrypt = require('bcryptjs')
import { builder } from '../builder'
import { prisma } from '../db'

builder.prismaObject('user', {
  fields: (t) => ({
    id: t.exposeInt('id'),
    email: t.exposeString('email'),
    username: t.exposeString('username'),
    password: t.exposeString('password'),
    role: t.exposeString('role'),
    user_type: t.exposeString('user_type'),
    product_key: t.exposeString('product_key', { nullable: true }),
  }),
})

export const UserUniqueInput = builder.inputType('UserUniqueInput', {
  fields: (t) => ({
    id: t.int(),
    email: t.string(),
  }),
})

export const LoginUserInput = builder.inputType('LoginUserInput', {
  fields: (t) => ({
    email: t.string({ required: true }),
    password: t.string({ required: true }),
  }),
})

const UserCreateInput = builder.inputType('UserCreateInput', {
  fields: (t) => ({
    email: t.string({ required: true }),
    username: t.string({ required: true }),
    password:t.string({ required: true }),
    role: t.string({ required: true }),
    user_type: t.string({ required: true }),
    product_key: t.string({ required: true }),
    phone: t.string({ required: true }),
  }),
})

builder.queryFields((t) => ({
  allUsers: t.prismaField({
    type: ['user'],
    resolve: (query, parent, args, context) => {
      console.log('context', context)
      if (!context.authScopes.isAuthorized) throw new Error('not authorized')
      return prisma.user.findMany({ ...query })
    }
  }),
}))

builder.mutationFields((t) => ({
  signupUser: t.prismaField({
    type: 'user',
    args: {
      data: t.arg({
        type: UserCreateInput,
        required: true,
      }),
    },
    resolve: async (query, parent, args) => {
      const exists = await prisma.user.count({
        where: {
          email: args.data.email
        }
      })
      if (exists) throw new Error('email already exists')
      const exists2 = await prisma.user.count({
        where: {
          username: args.data.username
        }
      })
      if (exists2) throw new Error('username already exists')
      const salt = bcrypt.genSaltSync(10)
      const password = bcrypt.hashSync(args.data.password, salt)
      return prisma.user.create({
        ...query,
        data: {
          email: args.data.email,
          username: args.data.username,
          password: password,
          role: args.data.role,
          user_type: args.data.user_type,
          product_key: args.data.product_key,
          phone: args.data.phone,
          created: new Date(),
          updated: new Date(),
        },
      })
    },
  }),
}))

builder.mutationFields((t) => ({
  loginUser: t.prismaField({
    type: 'user',
    args: {
      data: t.arg({
        type: LoginUserInput,
        required: true,
      }),
    },
    resolve: async (query, parent, args, ctx) => {
      const user = await prisma.user.findFirst({
        where: {
          email: args.data.email
        }
      })
      if (!user) throw new Error('email not found')
      const valid = bcrypt.compareSync(args.data.password, user.password)

      if (!valid) throw new Error('invalid password')

      ctx.user = {
        id: user.id.toString(),
        role: user.role,
      }
      
      return user
    }
  })
}))

builder.mutationFields((t) => ({
  logoutUser: t.field({
    type: 'String',
    args: {},
    resolve: (root, args, ctx) => {
      ctx.user = undefined
      return 'logged out'
    }
  })
}))
