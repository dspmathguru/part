import { Module } from '@nestjs/common'
import { PrismaService } from '../prisma/prisma.service'
import { AuthController } from './auth/auth.controller'
import { AuthService } from './auth/auth.service'

@Module({
  imports: [PrismaService],
  controllers: [AuthController],
  providers: [AuthService]
})
export class UserModule {}
