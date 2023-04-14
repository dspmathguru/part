import { IsString, IsNotEmpty, IsEmail, MinLength} from 'class-validator'

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
}

export class SigninDto {
  @IsEmail()
  email: string

  @IsString()
  password: string
}