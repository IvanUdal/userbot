# Скрипт для сборки Docker с автоматическим fallback
# Автор: Telegram Userbot Team

Write-Host "Starting Docker build..." -ForegroundColor Green

# Пробуем основной Dockerfile
Write-Host "Trying main Dockerfile..." -ForegroundColor Yellow
try {
    docker-compose build --no-cache
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Build completed successfully!" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "Error building main Dockerfile" -ForegroundColor Red
}

# Если основной не сработал, пробуем упрощенный
Write-Host "Switching to simple Dockerfile..." -ForegroundColor Yellow

# Временно переименовываем файлы
if (Test-Path "Dockerfile") {
    Rename-Item "Dockerfile" "Dockerfile.main"
}
if (Test-Path "Dockerfile.simple") {
    Rename-Item "Dockerfile.simple" "Dockerfile"
}

try {
    docker-compose build --no-cache
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Simple Dockerfile build completed successfully!" -ForegroundColor Green
        
        # Возвращаем оригинальные имена
        if (Test-Path "Dockerfile") {
            Rename-Item "Dockerfile" "Dockerfile.simple"
        }
        if (Test-Path "Dockerfile.main") {
            Rename-Item "Dockerfile.main" "Dockerfile"
        }
        
        exit 0
    }
} catch {
    Write-Host "Error building simple Dockerfile" -ForegroundColor Red
}

# Возвращаем оригинальные имена в случае ошибки
if (Test-Path "Dockerfile") {
    Rename-Item "Dockerfile" "Dockerfile.simple"
}
if (Test-Path "Dockerfile.main") {
    Rename-Item "Dockerfile.main" "Dockerfile"
}

Write-Host "All build attempts failed!" -ForegroundColor Red
Write-Host "Check internet connection and try again later" -ForegroundColor Yellow
exit 1 