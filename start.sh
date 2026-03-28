#!/bin/bash
if [ ! -d "$HOME/.cache/ms-playwright/chromium-1208" ]; then
    echo "Installing Playwright browsers..."
    playwright install chromium
    playwright install-deps chromium
else
    echo "Playwright browsers already installed, skipping..."
fi
echo "Starting bot..."
python bot_start.py
