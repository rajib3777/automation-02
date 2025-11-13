#!/bin/bash

# Wafid Booking Automation - Web Deployment Script
# Author: MiniMax Agent
# Date: 2025-09-18

echo "🚀 WAFID BOOKING AUTOMATION - WEB DEPLOYMENT"
echo "============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker is installed"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit: https://docs.docker.com/compose/install/"
        exit 1
    fi
    print_success "Docker Compose is installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p logs data ssl
    print_success "Directories created"
}

# Build Docker image
build_image() {
    print_status "Building Wafid Booking Web Application Docker image..."
    if docker-compose build; then
        print_success "Docker image built successfully"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Deploy application
deploy_application() {
    print_status "Deploying Wafid Booking Web Application..."
    
    # Stop any running instances
    docker-compose down
    
    # Start the application
    if docker-compose up -d; then
        print_success "Application deployed successfully"
    else
        print_error "Failed to deploy application"
        exit 1
    fi
}

# Check deployment status
check_deployment() {
    print_status "Checking deployment status..."
    sleep 10
    
    if curl -f http://localhost:5000/ > /dev/null 2>&1; then
        print_success "Application is running and accessible"
    else
        print_warning "Application might still be starting up"
        print_status "Check logs with: docker-compose logs -f"
    fi
}

# Show deployment information
show_deployment_info() {
    echo ""
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "======================"
    echo ""
    echo "📱 Web Dashboard: http://localhost:5000"
    echo "🔧 Configuration: Access via dashboard"
    echo "📊 Real-time Monitoring: Built-in dashboard"
    echo ""
    echo "🛠️ Management Commands:"
    echo "  View logs:    docker-compose logs -f"
    echo "  Stop app:     docker-compose down"
    echo "  Restart:      docker-compose restart"
    echo "  Update:       ./deploy.sh"
    echo ""
    echo "🎯 Your Wafid booking automation is now live!"
    echo "   Center Code 346 (Check Up Diagnostic Centre) is ready for targeting."
    echo ""
}

# Main deployment process
main() {
    print_status "Starting Wafid Booking Web Deployment..."
    
    check_docker
    check_docker_compose
    create_directories
    build_image
    deploy_application
    check_deployment
    show_deployment_info
}

# Run main function
main