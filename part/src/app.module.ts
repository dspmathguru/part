import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PartController } from './part/part.controller';
import { PartService } from './part/part.service';
import { PrismaModule } from './prisma/prisma.module';
import { PartModule } from './part/part.module';
import { UserModule } from './user/user.module';
import { UserModule } from './user/user.module';

@Module({
  imports: [PrismaModule, PartModule, UserModule],
  controllers: [AppController, PartController],
  providers: [AppService, PartService],
})
export class AppModule {}
