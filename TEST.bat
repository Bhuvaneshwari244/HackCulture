@echo off
echo ========================================
echo RuralAI Finance Hub - System Test
echo ========================================
echo.

echo Testing Backend Components...
echo.

cd backend

echo [1/4] Testing Credit Scoring Engine...
py credit_scoring.py
if %errorlevel% neq 0 (
    echo ERROR: Credit Scoring test failed!
    pause
    exit /b 1
)
echo ✅ Credit Scoring: OK
echo.

echo [2/4] Testing Crop Loan Advisor...
py crop_loan_advisor.py
if %errorlevel% neq 0 (
    echo ERROR: Crop Loan Advisor test failed!
    pause
    exit /b 1
)
echo ✅ Crop Loan Advisor: OK
echo.

echo [3/4] Testing Fraud Detection...
py fraud_detection.py
if %errorlevel% neq 0 (
    echo ERROR: Fraud Detection test failed!
    pause
    exit /b 1
)
echo ✅ Fraud Detection: OK
echo.

echo [4/4] Testing Chatbot...
py chatbot.py
if %errorlevel% neq 0 (
    echo ERROR: Chatbot test failed!
    pause
    exit /b 1
)
echo ✅ Chatbot: OK
echo.

cd ..

echo ========================================
echo ✅ All Tests Passed!
echo ========================================
echo.
echo Your RuralAI Finance Hub is ready!
echo Run START.bat to launch the application.
echo.
pause
