import { Injectable, UnauthorizedException } from '@nestjs/common'
import { SigninDto, SignupDto } from '../dtos/auth.dtos'
import { usertype } from '@prisma/client'
import { PrismaService } from 'src/prisma/prisma.service'
import * as bcrypt from 'bcryptjs'
import * as jwt from 'jsonwebtoken'

interface SignupParams {
  email: string
  username: string
  password: string
  role: string
  userType: usertype
}

interface SigninParams {
  email: string
  password: string
}

@Injectable()
export class AuthService {
  constructor(private readonly prismaService: PrismaService) {}

  async signup({ email, password, username, role }: SignupParams, userType: usertype) {
    const userExists = await this.prismaService.user.findUnique({ where: { email } })
    if (userExists) {
      throw new UnauthorizedException()
    }

    const hashedPassword = await bcrypt.hash(password, 10)

    const user = await this.prismaService.user.create({
      data: {
        email,
        username,
        password: hashedPassword,
        role,
        user_type: userType,
        created: new Date(),
        updated: new Date(),
      }
    })

    return this.generateJWT(username, user.id)

  }

  async signin({ email, password }: SigninParams) {
    const user = await this.prismaService.user.findUnique({ where: { email } })
    if (!user) {
      throw new UnauthorizedException()
    }

    const isPasswordValid = await bcrypt.compare(password, user.password)
    if (!isPasswordValid) {
      throw new UnauthorizedException()
    }

    return this.generateJWT(user.username, user.id)
  }

  private generateJWT(username: string, id: number) {
    return jwt.sign(
      {
        username,
        id,
      },
      process.env.JSON_WEB_TOKEN_SECRET,
      { expiresIn: '1d' },
    )
  }

  async generateProductKey(email: string, userType: usertype) {
    const validProductKey = `${email}-${userType}-${process.env.PRODUCT_KEY_SECRET}`
    const productKey = await bcrypt.hash(validProductKey, 10)
    return { productKey }
  }
}
