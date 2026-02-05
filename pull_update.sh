#!/bin/bash
echo "📥 Получение обновлений с GitHub..."
cd "$(dirname "$0")"
git pull origin main
echo "✅ Готово! Файлы обновлены."
echo ""
echo "Текущий статус:"
git status --short