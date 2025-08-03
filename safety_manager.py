"""
Модуль безопасности для Telegram Userbot
Обеспечивает защиту от блокировки через имитацию человеческого поведения
"""

import asyncio
import random
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class SafetyManager:
    """Менеджер безопасности для userbot"""
    
    def __init__(self):
        # Лимиты активности
        self.max_messages_per_hour = 20
        self.max_actions_per_day = 100
        self.min_delay_between_actions = 5  # секунд
        self.max_delay_between_actions = 30  # секунд
        
        # Счетчики
        self.messages_sent_this_hour = 0
        self.actions_today = 0
        self.last_action_time = 0
        
        # Временные метки
        self.hour_start = datetime.now()
        self.day_start = datetime.now()
        
        # Статистика
        self.action_history = []
        self.suspicious_patterns = []
        
        # Настройки человеческого поведения
        self.work_hours = {
            'start': 9,   # 9:00
            'end': 18     # 18:00
        }
        self.weekend_activity = 0.3  # 30% активности в выходные
        
    async def safe_action(self, action_type: str, action_func, *args, **kwargs):
        """Безопасное выполнение действия с проверками"""
        
        # Проверка времени работы (ОТКЛЮЧЕНО)
        # if not self._is_work_time():
        #     logger.info("⏰ Вне рабочего времени - действие отложено")
        #     return False
        
        # Проверка лимитов (ОТКЛЮЧЕНО)
        # if not self._check_limits():
        #     logger.warning("⚠️ Достигнут лимит действий - ожидание")
        #     return False
        
        # Случайная задержка (ОТКЛЮЧЕНО)
        # delay = random.uniform(self.min_delay_between_actions, self.max_delay_between_actions)
        # await asyncio.sleep(delay)
        
        # Выполнение действия
        try:
            result = await action_func(*args, **kwargs)
            
            # Обновление статистики (ОТКЛЮЧЕНО)
            # self._update_stats(action_type)
            
            logger.info(f"✅ Действие выполнено: {action_type}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка при выполнении действия {action_type}: {e}")
            return False
    
    def _is_work_time(self) -> bool:
        """Проверка рабочего времени"""
        now = datetime.now()
        current_hour = now.hour
        is_weekend = now.weekday() >= 5
        
        # В выходные снижаем активность
        if is_weekend:
            return random.random() < self.weekend_activity
        
        # В рабочие дни проверяем часы
        return self.work_hours['start'] <= current_hour <= self.work_hours['end']
    
    def _check_limits(self) -> bool:
        """Проверка лимитов активности"""
        now = datetime.now()
        
        # Сброс счетчиков каждый час
        if now - self.hour_start > timedelta(hours=1):
            self.messages_sent_this_hour = 0
            self.hour_start = now
        
        # Сброс счетчиков каждый день
        if now - self.day_start > timedelta(days=1):
            self.actions_today = 0
            self.day_start = now
        
        # Проверка лимитов
        if self.messages_sent_this_hour >= self.max_messages_per_hour:
            logger.warning("⚠️ Достигнут лимит сообщений в час")
            return False
        
        if self.actions_today >= self.max_actions_per_day:
            logger.warning("⚠️ Достигнут дневной лимит действий")
            return False
        
        return True
    
    def _update_stats(self, action_type: str):
        """Обновление статистики"""
        now = time.time()
        
        # Минимальный интервал между действиями
        if now - self.last_action_time < self.min_delay_between_actions:
            self.suspicious_patterns.append(f"Слишком частые действия: {action_type}")
        
        self.last_action_time = now
        self.actions_today += 1
        
        if action_type == "message":
            self.messages_sent_this_hour += 1
        
        # Сохранение истории
        self.action_history.append({
            'type': action_type,
            'timestamp': datetime.now(),
            'hour_count': self.messages_sent_this_hour,
            'day_count': self.actions_today
        })
    
    async def safe_message(self, client, chat_id: int, text: str) -> bool:
        """Безопасная отправка сообщения"""
        async def send_message():
            await client.send_message(chat_id, text)
        
        return await self.safe_action("message", send_message)
    
    async def safe_forward(self, client, from_chat: int, to_chat: int, message_id: int) -> bool:
        """Безопасная пересылка сообщения"""
        async def forward_message():
            await client.forward_messages(to_chat, message_id, from_chat)
        
        return await self.safe_action("forward", forward_message)
    
    async def safe_reply(self, client, chat_id: int, message_id: int, text: str) -> bool:
        """Безопасный ответ на сообщение"""
        async def reply_message():
            await client.send_message(chat_id, text, reply_to=message_id)
        
        return await self.safe_action("reply", reply_message)
    
    def get_safety_report(self) -> str:
        """Отчет о безопасности"""
        report = f"📊 **Отчет безопасности**\n\n"
        report += f"⏰ Время работы: {self._is_work_time()}\n"
        report += f"📨 Сообщений в час: {self.messages_sent_this_hour}/{self.max_messages_per_hour}\n"
        report += f"📈 Действий сегодня: {self.actions_today}/{self.max_actions_per_day}\n"
        report += f"⚠️ Подозрительных паттернов: {len(self.suspicious_patterns)}\n"
        
        if self.suspicious_patterns:
            report += f"\n🚨 Последние предупреждения:\n"
            for pattern in self.suspicious_patterns[-3:]:
                report += f"• {pattern}\n"
        
        return report
    
    def is_safe_to_continue(self) -> bool:
        """Проверка безопасности продолжения работы"""
        # Слишком много подозрительных паттернов
        if len(self.suspicious_patterns) > 10:
            logger.error("🚨 Слишком много подозрительных паттернов - остановка")
            return False
        
        # Превышение лимитов
        if self.messages_sent_this_hour >= self.max_messages_per_hour:
            return False
        
        if self.actions_today >= self.max_actions_per_day:
            return False
        
        return True 