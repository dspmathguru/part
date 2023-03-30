import { Body, Controller, Param, ParseEnumPipe, Post, UnauthorizedException } from '@nestjs/common';

@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}
  @Post('/signup/:userType')
  signup(
    @Body() body: SignupDto, 
    @Param('userType', new ParseEnumPipe(UserType)) userType: UserType
  ) {

    if (userType !== UserType.BUYER) {
      if (!body.productKey) {
        throw new UnauthorizedException()
      }

      const validProductKey = `${body.email}-${userType}-${process.env.PRODUCT_KEY_SECRET}`
      const isValidProductKey = bcrypt.compare(validProductKey, body.productKey)

      if (!isValidProductKey) {
        throw new UnauthorizedException()
      }
    }

    return this.authService.signup(body, userType)
  }

  @Post("/signin")
  signin(@Body() body: SigninDto) {
    return this.authService.signin(body)
  }

  @Post("/key")
  generateProductKey(@Body() {userType, email}: GenerateProductKeyDto) {
    return this.authService.generateProductKey(email, userType)
  }

  @Get("/me")
  me(@User() user: UserInfo) {
    return user
}
