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

const UserCreateInput = builder.inputType('UserCreateInput', {
  fields: (t) => ({
    email: t.string({ required: true }),
    username: t.string({ required: true }),
    password:t.string({ required: true }),
    role: t.string({ required: true }),
    user_type: t.string({ required: true }),
    product_key: t.string({ required: true }),
  }),
})

builder.queryFields((t) => ({
  allUsers: t.prismaField({
    type: ['user'],
    resolve: (query) => prisma.user.findMany({ ...query }),
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
    resolve: (query, parent, args) => {
      return prisma.user.create({
        ...query,
        data: {
          email: args.data.email,
          username: args.data.username,
          password: args.data.password,
          role: args.data.role,
          user_type: args.data.user_type,
          product_key: args.data.product_key,
          created: new Date(),
          updated: new Date(),
        },
      })
    },
  }),
}))
