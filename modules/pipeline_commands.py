"""
Команды управления пайплайнами для масштабируемого парсинга
"""

import json
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from telethon import events
from telethon.tl.types import User

from .pipeline_manager import PipelineManager

class PipelineCommands:
    """Команды управления пайплайнами"""
    
    def __init__(self, client, pipeline_manager: PipelineManager):
        self.client = client
        self.pipeline_manager = pipeline_manager
        self.logger = pipeline_manager.logger
    
    async def setup_commands(self):
        """Настройка команд"""
        @self.client.on(events.NewMessage(pattern=r'^\.pipelines_start_all$'))
        async def start_all_pipelines(event):
            await self.start_all_pipelines_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.pipelines_stop_all$'))
        async def stop_all_pipelines(event):
            await self.stop_all_pipelines_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.pipeline_status (.+)$'))
        async def pipeline_status(event):
            await self.pipeline_status_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.source_add (.+) (-?\d+)$'))
        async def add_source(event):
            await self.add_source_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.source_remove (.+)$'))
        async def remove_source(event):
            await self.remove_source_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.destination_add (.+) (.+) (.+)$'))
        async def add_destination(event):
            await self.add_destination_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.destination_remove (.+)$'))
        async def remove_destination(event):
            await self.remove_destination_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.pipeline_create (.+) (.+) (.+)$'))
        async def create_pipeline(event):
            await self.create_pipeline_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.pipeline_remove (.+)$'))
        async def remove_pipeline(event):
            await self.remove_pipeline_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.stats_export (.+)$'))
        async def export_stats(event):
            await self.export_stats_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.pipelines_list$'))
        async def list_pipelines(event):
            await self.list_pipelines_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.sources_list$'))
        async def list_sources(event):
            await self.list_sources_command(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.destinations_list$'))
        async def list_destinations(event):
            await self.list_destinations_command(event)
    
    async def start_all_pipelines_command(self, event):
        """Команда .pipelines_start_all"""
        try:
            started_count = 0
            failed_count = 0
            
            for pipeline_name in self.pipeline_manager.pipelines:
                if self.pipeline_manager.pipelines[pipeline_name].enabled:
                    success = await self.pipeline_manager.start_pipeline(pipeline_name)
                    if success:
                        started_count += 1
                    else:
                        failed_count += 1
            
            response = f"🚀 **Запуск всех пайплайнов завершен**\n\n"
            response += f"✅ Успешно запущено: {started_count}\n"
            response += f"❌ Ошибок: {failed_count}\n"
            response += f"📊 Всего пайплайнов: {len(self.pipeline_manager.pipelines)}"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка запуска пайплайнов: {e}")
    
    async def stop_all_pipelines_command(self, event):
        """Команда .pipelines_stop_all"""
        try:
            stopped_count = 0
            
            for pipeline_name in self.pipeline_manager.pipelines:
                success = await self.pipeline_manager.stop_pipeline(pipeline_name)
                if success:
                    stopped_count += 1
            
            response = f"🛑 **Остановка всех пайплайнов завершена**\n\n"
            response += f"✅ Остановлено: {stopped_count}\n"
            response += f"📊 Всего пайплайнов: {len(self.pipeline_manager.pipelines)}"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка остановки пайплайнов: {e}")
    
    async def pipeline_status_command(self, event):
        """Команда .pipeline_status <pipeline_name>"""
        try:
            pipeline_name = event.pattern_match.group(1)
            status = await self.pipeline_manager.get_pipeline_status(pipeline_name)
            
            if not status:
                await event.respond(f"❌ Пайплайн '{pipeline_name}' не найден")
                return
            
            response = f"📊 **Статус пайплайна: {pipeline_name}**\n\n"
            response += f"🔄 Статус: {'✅ Активен' if status['enabled'] else '❌ Отключен'}\n"
            response += f"📥 Источник: {status['source']}\n"
            response += f"📤 Назначения: {', '.join(status['destinations'])}\n"
            response += f"📈 Обработано: {status['total_processed']}\n"
            response += f"❌ Ошибок: {status['total_errors']}\n"
            
            if status['last_run']:
                response += f"🕐 Последний запуск: {status['last_run']}\n"
            
            if status['stats']:
                stats = status['stats']
                response += f"\n📊 **Детальная статистика:**\n"
                response += f"• Сообщений обработано: {stats.get('messages_processed', 0)}\n"
                response += f"• Ошибок: {stats.get('messages_errors', 0)}\n"
                response += f"• Время обработки: {stats.get('processing_time', 0):.2f}с\n"
                
                if stats.get('last_activity'):
                    response += f"• Последняя активность: {stats['last_activity']}\n"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения статуса: {e}")
    
    async def add_source_command(self, event):
        """Команда .source_add <name> <id>"""
        try:
            name = event.pattern_match.group(1)
            source_id = int(event.pattern_match.group(2))
            
            success = await self.pipeline_manager.add_source(name, source_id)
            
            if success:
                response = f"✅ **Источник добавлен**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"🆔 ID: {source_id}\n"
                response += f"📊 Всего источников: {len(self.pipeline_manager.sources)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Ошибка добавления источника '{name}'")
        
        except ValueError:
            await event.respond("❌ Неверный формат ID источника")
        except Exception as e:
            await event.respond(f"❌ Ошибка добавления источника: {e}")
    
    async def remove_source_command(self, event):
        """Команда .source_remove <name>"""
        try:
            name = event.pattern_match.group(1)
            success = await self.pipeline_manager.remove_source(name)
            
            if success:
                response = f"🗑️ **Источник удален**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"📊 Осталось источников: {len(self.pipeline_manager.sources)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Источник '{name}' не найден")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка удаления источника: {e}")
    
    async def add_destination_command(self, event):
        """Команда .destination_add <name> <type> <config>"""
        try:
            name = event.pattern_match.group(1)
            dest_type = event.pattern_match.group(2)
            config_str = event.pattern_match.group(3)
            
            # Парсинг конфигурации
            try:
                config = json.loads(config_str)
            except json.JSONDecodeError:
                await event.respond("❌ Неверный формат конфигурации (должен быть JSON)")
                return
            
            success = await self.pipeline_manager.add_destination(name, dest_type, config)
            
            if success:
                response = f"✅ **Назначение добавлено**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"🔧 Тип: {dest_type}\n"
                response += f"⚙️ Конфигурация: {json.dumps(config, ensure_ascii=False)}\n"
                response += f"📊 Всего назначений: {len(self.pipeline_manager.destinations)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Ошибка добавления назначения '{name}'")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка добавления назначения: {e}")
    
    async def remove_destination_command(self, event):
        """Команда .destination_remove <name>"""
        try:
            name = event.pattern_match.group(1)
            success = await self.pipeline_manager.remove_destination(name)
            
            if success:
                response = f"🗑️ **Назначение удалено**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"📊 Осталось назначений: {len(self.pipeline_manager.destinations)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Назначение '{name}' не найдено")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка удаления назначения: {e}")
    
    async def create_pipeline_command(self, event):
        """Команда .pipeline_create <name> <source> <destinations>"""
        try:
            name = event.pattern_match.group(1)
            source = event.pattern_match.group(2)
            destinations_str = event.pattern_match.group(3)
            
            # Парсинг списка назначений
            destinations = [dest.strip() for dest in destinations_str.split(',')]
            
            success = await self.pipeline_manager.create_pipeline(name, source, destinations)
            
            if success:
                response = f"✅ **Пайплайн создан**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"📥 Источник: {source}\n"
                response += f"📤 Назначения: {', '.join(destinations)}\n"
                response += f"📊 Всего пайплайнов: {len(self.pipeline_manager.pipelines)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Ошибка создания пайплайна '{name}'")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка создания пайплайна: {e}")
    
    async def remove_pipeline_command(self, event):
        """Команда .pipeline_remove <name>"""
        try:
            name = event.pattern_match.group(1)
            success = await self.pipeline_manager.remove_pipeline(name)
            
            if success:
                response = f"🗑️ **Пайплайн удален**\n\n"
                response += f"📝 Название: {name}\n"
                response += f"📊 Осталось пайплайнов: {len(self.pipeline_manager.pipelines)}"
                
                await event.respond(response)
            else:
                await event.respond(f"❌ Пайплайн '{name}' не найден")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка удаления пайплайна: {e}")
    
    async def export_stats_command(self, event):
        """Команда .stats_export <type>"""
        try:
            export_type = event.pattern_match.group(1)
            
            if export_type == "all_pipelines":
                stats = await self.pipeline_manager.get_statistics()
                
                response = f"📊 **Экспорт статистики**\n\n"
                response += f"📈 **Общая статистика:**\n"
                response += f"• Источников: {stats['sources_count']}\n"
                response += f"• Назначений: {stats['destinations_count']}\n"
                response += f"• Пайплайнов: {stats['pipelines_count']}\n"
                response += f"• Активных источников: {stats['active_sources']}\n"
                response += f"• Активных назначений: {stats['active_destinations']}\n"
                response += f"• Активных пайплайнов: {stats['active_pipelines']}\n\n"
                
                if stats['report']:
                    report = stats['report']
                    response += f"📋 **Отчет мониторинга:**\n"
                    response += f"• Всего пайплайнов: {report['summary']['total_pipelines']}\n"
                    response += f"• Обработано сообщений: {report['summary']['total_processed']}\n"
                    response += f"• Ошибок: {report['summary']['total_errors']}\n"
                    response += f"• Активных пайплайнов: {report['summary']['active_pipelines']}\n"
                
                await event.respond(response)
            
            else:
                await event.respond("❌ Неизвестный тип экспорта. Доступные типы: all_pipelines")
        
        except Exception as e:
            await event.respond(f"❌ Ошибка экспорта статистики: {e}")
    
    async def list_pipelines_command(self, event):
        """Команда .pipelines_list"""
        try:
            if not self.pipeline_manager.pipelines:
                await event.respond("📋 Пайплайны не найдены")
                return
            
            response = f"📋 **Список пайплайнов** ({len(self.pipeline_manager.pipelines)})\n\n"
            
            for name, pipeline in self.pipeline_manager.pipelines.items():
                status = "✅" if pipeline.enabled else "❌"
                response += f"{status} **{name}**\n"
                response += f"   📥 Источник: {pipeline.source}\n"
                response += f"   📤 Назначения: {', '.join(pipeline.destinations)}\n"
                response += f"   📊 Обработано: {pipeline.total_processed}\n"
                response += f"   ❌ Ошибок: {pipeline.total_errors}\n\n"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения списка пайплайнов: {e}")
    
    async def list_sources_command(self, event):
        """Команда .sources_list"""
        try:
            if not self.pipeline_manager.sources:
                await event.respond("📋 Источники не найдены")
                return
            
            response = f"📋 **Список источников** ({len(self.pipeline_manager.sources)})\n\n"
            
            for name, source in self.pipeline_manager.sources.items():
                status = "✅" if source.enabled else "❌"
                response += f"{status} **{name}**\n"
                response += f"   🆔 ID: {source.id}\n"
                response += f"   📝 Тип: {source.type}\n"
                response += f"   📊 Сообщений: {source.message_count}\n"
                response += f"   ❌ Ошибок: {source.error_count}\n\n"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения списка источников: {e}")
    
    async def list_destinations_command(self, event):
        """Команда .destinations_list"""
        try:
            if not self.pipeline_manager.destinations:
                await event.respond("📋 Назначения не найдены")
                return
            
            response = f"📋 **Список назначений** ({len(self.pipeline_manager.destinations)})\n\n"
            
            for name, destination in self.pipeline_manager.destinations.items():
                status = "✅" if destination.enabled else "❌"
                response += f"{status} **{name}**\n"
                response += f"   🔧 Тип: {destination.type}\n"
                response += f"   ✅ Успешно: {destination.success_count}\n"
                response += f"   ❌ Ошибок: {destination.error_count}\n\n"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения списка назначений: {e}") 