@echo off
echo ========================================
echo RuralAI - SMS Provider Setup
echo ========================================
echo.

echo This script will help you set up real SMS delivery
echo for OTP authentication in your RuralAI app.
echo.

:MENU
echo ========================================
echo Choose Your SMS Provider:
echo ========================================
echo.
echo 1. Twilio (Recommended - $15 free credit)
echo 2. MSG91 (India - 100 free SMS)
echo 3. Fast2SMS (India - 50 free SMS)
echo 4. Install All (Best for production)
echo 5. Test SMS Setup
echo 6. Exit
echo.

set /p choice="Enter your choice [1-6]: "

if "%choice%"=="1" goto TWILIO
if "%choice%"=="2" goto MSG91
if "%choice%"=="3" goto FAST2SMS
if "%choice%"=="4" goto ALL
if "%choice%"=="5" goto TEST
if "%choice%"=="6" goto EXIT
goto MENU

:TWILIO
echo.
echo ========================================
echo Installing Twilio SDK...
echo ========================================
cd backend
call venv\Scripts\activate
pip install twilio
echo.
echo ✅ Twilio installed successfully!
echo.
echo 📝 Next Steps:
echo 1. Sign up at https://www.twilio.com/try-twilio
echo 2. Get your Account SID and Auth Token
echo 3. Get a phone number
echo 4. Add to backend\.env file:
echo    TWILIO_ACCOUNT_SID=your_sid_here
echo    TWILIO_AUTH_TOKEN=your_token_here
echo    TWILIO_PHONE_NUMBER=your_number_here
echo.
pause
goto MENU

:MSG91
echo.
echo ========================================
echo MSG91 Setup (No extra install needed)
echo ========================================
echo.
echo 📝 Setup Steps:
echo 1. Sign up at https://msg91.com/signup
echo 2. Get your Auth Key from dashboard
echo 3. Create DLT Template (takes 24-48 hours)
echo 4. Add to backend\.env file:
echo    MSG91_AUTH_KEY=your_key_here
echo    MSG91_TEMPLATE_ID=your_template_id
echo.
pause
goto MENU

:FAST2SMS
echo.
echo ========================================
echo Fast2SMS Setup (No extra install needed)
echo ========================================
echo.
echo 📝 Setup Steps:
echo 1. Sign up at https://www.fast2sms.com/register
echo 2. Get API Key from dashboard
echo 3. Add to backend\.env file:
echo    FAST2SMS_API_KEY=your_key_here
echo.
pause
goto MENU

:ALL
echo.
echo ========================================
echo Installing All SMS Providers...
echo ========================================
cd backend
call venv\Scripts\activate
pip install twilio boto3 sendgrid
echo.
echo ✅ All providers installed!
echo.
echo 📝 Configure your chosen provider in backend\.env
echo    See SMS_SETUP_GUIDE.md for detailed instructions
echo.
pause
goto MENU

:TEST
echo.
echo ========================================
echo Testing SMS Configuration...
echo ========================================
cd backend
call venv\Scripts\activate
python test_sms.py
pause
goto MENU

:EXIT
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo 📖 For detailed instructions, see:
echo    SMS_SETUP_GUIDE.md
echo.
echo 🧪 To test your setup:
echo    cd backend
echo    venv\Scripts\activate
echo    python test_sms.py
echo.
echo 🚀 Start your app with:
echo    START.bat
echo.
pause
exit
