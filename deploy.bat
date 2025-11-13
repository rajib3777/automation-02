@echo off
REM Wafid Booking Automation - Windows Web Deployment Script
REM Author: MiniMax Agent
REM Date: 2025-09-18

echo 🚀 WAFID BOOKING AUTOMATION - WEB DEPLOYMENT
echo =============================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)
echo ✅ Docker is installed

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker Compose is not installed. Please install Docker Compose first.
    echo Visit: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)
echo ✅ Docker Compose is installed

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "ssl" mkdir ssl
echo ✅ Directories created

REM Build Docker image
echo 🔨 Building Wafid Booking Web Application Docker image...
docker-compose build
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to build Docker image
    pause
    exit /b 1
)
echo ✅ Docker image built successfully

REM Deploy application
echo 🚀 Deploying Wafid Booking Web Application...

REM Stop any running instances
docker-compose down

REM Start the application
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ ERROR: Failed to deploy application
    pause
    exit /b 1
)
echo ✅ Application deployed successfully

REM Wait for application to start
echo ⏳ Waiting for application to start...
timeout /t 15 /nobreak >nul

REM Show deployment information
echo.
echo 🎉 DEPLOYMENT COMPLETE!
echo ======================
echo.
echo 📱 Web Dashboard: http://localhost:5000
echo 🔧 Configuration: Access via dashboard
echo 📊 Real-time Monitoring: Built-in dashboard
echo.
echo 🛠️ Management Commands:
echo   View logs:    docker-compose logs -f
echo   Stop app:     docker-compose down
echo   Restart:      docker-compose restart
echo   Update:       deploy.bat
echo.
echo 🎯 Your Wafid booking automation is now live!
echo    Center Code 346 (Check Up Diagnostic Centre) is ready for targeting.
echo.

REM Open browser
echo 🌐 Opening web dashboard...
start http://localhost:5000

pause