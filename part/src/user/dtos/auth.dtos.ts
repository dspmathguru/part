import { IsString, IsNotEmpty, IsEmail, MinLength, IsOptional} from 'class-validator'

export class SignupDto {
  @IsString()
  @IsNotEmpty()
  username: string

  @IsString()
  @MinLength(8)
  password: string

  @IsEmail()
  email: string
  role: string

  @IsOptional()
  @IsString()
  productKey?: string
}

export class SigninDto {
  @IsEmail()
  email: string

  @IsString()
  password: string
}