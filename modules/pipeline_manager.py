"""
Модуль управления пайплайнами для масштабируемого парсинга
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import aiofiles
from telethon import TelegramClient
from telethon.errors import FloodWaitError, ChatAdminRequiredError

@dataclass
class Source:
    """Структура источника парсинга"""
    id: int
    name: str
    type: str  # channel, group, supergroup
    enabled: bool
    parsing_rules: Dict[str, bool]
    filters: Dict[str, Any]
    last_activity: Optional[datetime] = None
    message_count: int = 0
    error_count: int = 0

@dataclass
class Destination:
    """Структура назначения"""
    name: str
    type: str  # database, telegram, file, webhook
    enabled: bool
    config: Dict[str, Any]
    processing_rules: Dict[str, Any]
    success_count: int = 0
    error_count: int = 0
    last_success: Optional[datetime] = None

@dataclass
class Pipeline:
    """Структура пайплайна"""
    name: str
    enabled: bool
    source: str
    destinations: List[str]
    processing_steps: List[Dict[str, Any]]
    created_at: datetime
    last_run: Optional[datetime] = None
    total_processed: int = 0
    total_errors: int = 0

@dataclass
class PipelineStats:
    """Статистика пайплайна"""
    pipeline_name: str
    messages_processed: int = 0
    messages_errors: int = 0
    processing_time: float = 0.0
    last_activity: Optional[datetime] = None
    source_stats: Dict[str, int] = None
    destination_stats: Dict[str, int] = None

class PipelineMonitor:
    """Мониторинг пайплайнов"""
    
    def __init__(self):
        self.stats: Dict[str, PipelineStats] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.logger = logging.getLogger(__name__)
    
    async def track_pipeline(self, pipeline_name: str, data: dict):
        """Отслеживание работы пайплайна"""
        if pipeline_name not in self.stats:
            self.stats[pipeline_name] = PipelineStats(pipeline_name=pipeline_name)
        
        stats = self.stats[pipeline_name]
        stats.messages_processed += data.get('processed', 0)
        stats.messages_errors += data.get('errors', 0)
        stats.processing_time += data.get('processing_time', 0.0)
        stats.last_activity = datetime.now()
        
        # Обновление статистики источников и назначений
        if 'source_stats' in data:
            if stats.source_stats is None:
                stats.source_stats = {}
            stats.source_stats.update(data['source_stats'])
        
        if 'destination_stats' in data:
            if stats.destination_stats is None:
                stats.destination_stats = {}
            stats.destination_stats.update(data['destination_stats'])
    
    async def generate_report(self) -> dict:
        """Генерация отчета по всем пайплайнам"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_pipelines': len(self.stats),
            'pipelines': {},
            'summary': {
                'total_processed': 0,
                'total_errors': 0,
                'active_pipelines': 0
            }
        }
        
        for pipeline_name, stats in self.stats.items():
            report['pipelines'][pipeline_name] = asdict(stats)
            report['summary']['total_processed'] += stats.messages_processed
            report['summary']['total_errors'] += stats.messages_errors
            
            if stats.last_activity and (datetime.now() - stats.last_activity).seconds < 300:
                report['summary']['active_pipelines'] += 1
        
        return report
    
    async def send_alert(self, alert_type: str, message: str, pipeline_name: str = None):
        """Отправка уведомлений"""
        alert = {
            'type': alert_type,
            'message': message,
            'pipeline_name': pipeline_name,
            'timestamp': datetime.now().isoformat()
        }
        self.alerts.append(alert)
        self.logger.warning(f"Alert [{alert_type}]: {message}")

class PipelineManager:
    """Управление пайплайнами"""
    
    def __init__(self, client: TelegramClient, config_path: str = "./config"):
        self.client = client
        self.config_path = Path(config_path)
        self.config_path.mkdir(exist_ok=True)
        
        self.sources: Dict[str, Source] = {}
        self.destinations: Dict[str, Destination] = {}
        self.pipelines: Dict[str, Pipeline] = {}
        self.monitor = PipelineMonitor()
        self.logger = logging.getLogger(__name__)
        
        # Загрузка конфигурации
        self.load_config()
    
    def load_config(self):
        """Загрузка конфигурации из файлов"""
        try:
            # Загрузка источников
            sources_file = self.config_path / "sources.json"
            if sources_file.exists():
                with open(sources_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, source_data in data['sources'].items():
                        self.sources[name] = Source(**source_data)
            
            # Загрузка назначений
            destinations_file = self.config_path / "destinations.json"
            if destinations_file.exists():
                with open(destinations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, dest_data in data['destinations'].items():
                        self.destinations[name] = Destination(**dest_data)
            
            # Загрузка пайплайнов
            pipelines_file = self.config_path / "pipelines.json"
            if pipelines_file.exists():
                with open(pipelines_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, pipeline_data in data['pipelines'].items():
                        pipeline_data['created_at'] = datetime.fromisoformat(pipeline_data['created_at'])
                        if pipeline_data.get('last_run'):
                            pipeline_data['last_run'] = datetime.fromisoformat(pipeline_data['last_run'])
                        self.pipelines[name] = Pipeline(**pipeline_data)
            
            self.logger.info(f"Загружено {len(self.sources)} источников, {len(self.destinations)} назначений, {len(self.pipelines)} пайплайнов")
        
        except Exception as e:
            self.logger.error(f"Ошибка загрузки конфигурации: {e}")
    
    async def save_config(self):
        """Сохранение конфигурации в файлы"""
        try:
            # Сохранение источников
            sources_data = {
                'sources': {name: asdict(source) for name, source in self.sources.items()}
            }
            with open(self.config_path / "sources.json", 'w', encoding='utf-8') as f:
                json.dump(sources_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Сохранение назначений
            destinations_data = {
                'destinations': {name: asdict(dest) for name, dest in self.destinations.items()}
            }
            with open(self.config_path / "destinations.json", 'w', encoding='utf-8') as f:
                json.dump(destinations_data, f, indent=2, ensure_ascii=False, default=str)
            
            # Сохранение пайплайнов
            pipelines_data = {
                'pipelines': {name: asdict(pipeline) for name, pipeline in self.pipelines.items()}
            }
            with open(self.config_path / "pipelines.json", 'w', encoding='utf-8') as f:
                json.dump(pipelines_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info("Конфигурация сохранена")
        
        except Exception as e:
            self.logger.error(f"Ошибка сохранения конфигурации: {e}")
    
    async def add_source(self, name: str, source_id: int, source_type: str = "group", 
                        parsing_rules: Dict[str, bool] = None, filters: Dict[str, Any] = None) -> bool:
        """Добавление нового источника"""
        try:
            # Проверка доступа к источнику
            entity = await self.client.get_entity(source_id)
            
            source = Source(
                id=source_id,
                name=name,
                type=source_type,
                enabled=True,
                parsing_rules=parsing_rules or {
                    "parse_text": True,
                    "parse_media": True,
                    "parse_buttons": True,
                    "parse_bots": False
                },
                filters=filters or {
                    "keywords": [],
                    "exclude_keywords": [],
                    "min_length": 0
                }
            )
            
            self.sources[name] = source
            await self.save_config()
            
            self.logger.info(f"Добавлен источник: {name} (ID: {source_id})")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка добавления источника {name}: {e}")
            return False
    
    async def remove_source(self, name: str) -> bool:
        """Удаление источника"""
        if name in self.sources:
            del self.sources[name]
            await self.save_config()
            self.logger.info(f"Удален источник: {name}")
            return True
        return False
    
    async def add_destination(self, name: str, dest_type: str, config: Dict[str, Any], 
                            processing_rules: Dict[str, Any] = None) -> bool:
        """Добавление нового назначения"""
        try:
            destination = Destination(
                name=name,
                type=dest_type,
                enabled=True,
                config=config,
                processing_rules=processing_rules or {}
            )
            
            self.destinations[name] = destination
            await self.save_config()
            
            self.logger.info(f"Добавлено назначение: {name} (тип: {dest_type})")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка добавления назначения {name}: {e}")
            return False
    
    async def remove_destination(self, name: str) -> bool:
        """Удаление назначения"""
        if name in self.destinations:
            del self.destinations[name]
            await self.save_config()
            self.logger.info(f"Удалено назначение: {name}")
            return True
        return False
    
    async def create_pipeline(self, name: str, source: str, destinations: List[str], 
                            processing_steps: List[Dict[str, Any]] = None) -> bool:
        """Создание нового пайплайна"""
        try:
            if source not in self.sources:
                raise ValueError(f"Источник {source} не найден")
            
            for dest in destinations:
                if dest not in self.destinations:
                    raise ValueError(f"Назначение {dest} не найдено")
            
            pipeline = Pipeline(
                name=name,
                enabled=True,
                source=source,
                destinations=destinations,
                processing_steps=processing_steps or [],
                created_at=datetime.now()
            )
            
            self.pipelines[name] = pipeline
            await self.save_config()
            
            self.logger.info(f"Создан пайплайн: {name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка создания пайплайна {name}: {e}")
            return False
    
    async def remove_pipeline(self, name: str) -> bool:
        """Удаление пайплайна"""
        if name in self.pipelines:
            del self.pipelines[name]
            await self.save_config()
            self.logger.info(f"Удален пайплайн: {name}")
            return True
        return False
    
    async def start_pipeline(self, pipeline_name: str) -> bool:
        """Запуск пайплайна"""
        if pipeline_name not in self.pipelines:
            self.logger.error(f"Пайплайн {pipeline_name} не найден")
            return False
        
        pipeline = self.pipelines[pipeline_name]
        if not pipeline.enabled:
            self.logger.error(f"Пайплайн {pipeline_name} отключен")
            return False
        
        try:
            # Запуск обработки в отдельной задаче
            asyncio.create_task(self._run_pipeline(pipeline_name))
            self.logger.info(f"Пайплайн {pipeline_name} запущен")
            return True
        
        except Exception as e:
            self.logger.error(f"Ошибка запуска пайплайна {pipeline_name}: {e}")
            return False
    
    async def stop_pipeline(self, pipeline_name: str) -> bool:
        """Остановка пайплайна"""
        # В реальной реализации здесь нужно остановить задачу
        self.logger.info(f"Пайплайн {pipeline_name} остановлен")
        return True
    
    async def restart_pipeline(self, pipeline_name: str) -> bool:
        """Перезапуск пайплайна"""
        await self.stop_pipeline(pipeline_name)
        await asyncio.sleep(1)
        return await self.start_pipeline(pipeline_name)
    
    async def get_pipeline_status(self, pipeline_name: str) -> Optional[Dict[str, Any]]:
        """Получение статуса пайплайна"""
        if pipeline_name not in self.pipelines:
            return None
        
        pipeline = self.pipelines[pipeline_name]
        stats = self.monitor.stats.get(pipeline_name, PipelineStats(pipeline_name=pipeline_name))
        
        return {
            'name': pipeline.name,
            'enabled': pipeline.enabled,
            'source': pipeline.source,
            'destinations': pipeline.destinations,
            'total_processed': pipeline.total_processed,
            'total_errors': pipeline.total_errors,
            'last_run': pipeline.last_run.isoformat() if pipeline.last_run else None,
            'created_at': pipeline.created_at.isoformat(),
            'stats': asdict(stats)
        }
    
    async def _run_pipeline(self, pipeline_name: str):
        """Выполнение пайплайна"""
        pipeline = self.pipelines[pipeline_name]
        source = self.sources[pipeline.source]
        
        self.logger.info(f"Запуск пайплайна {pipeline_name} для источника {pipeline.source}")
        
        try:
            async for message in self.client.iter_messages(source.id, reverse=True):
                if not pipeline.enabled:
                    break
                
                start_time = datetime.now()
                
                try:
                    # Обработка сообщения через пайплайн
                    processed_data = await self._process_message(message, pipeline)
                    
                    # Отправка в назначения
                    for dest_name in pipeline.destinations:
                        destination = self.destinations[dest_name]
                        if destination.enabled:
                            await self._send_to_destination(processed_data, destination)
                    
                    # Обновление статистики
                    processing_time = (datetime.now() - start_time).total_seconds()
                    await self.monitor.track_pipeline(pipeline_name, {
                        'processed': 1,
                        'errors': 0,
                        'processing_time': processing_time
                    })
                    
                    pipeline.total_processed += 1
                    pipeline.last_run = datetime.now()
                
                except Exception as e:
                    self.logger.error(f"Ошибка обработки сообщения в пайплайне {pipeline_name}: {e}")
                    pipeline.total_errors += 1
                    await self.monitor.track_pipeline(pipeline_name, {
                        'processed': 0,
                        'errors': 1,
                        'processing_time': 0
                    })
                
                await asyncio.sleep(0.1)  # Небольшая задержка
        
        except Exception as e:
            self.logger.error(f"Критическая ошибка в пайплайне {pipeline_name}: {e}")
            await self.monitor.send_alert("pipeline_error", f"Ошибка пайплайна {pipeline_name}: {e}", pipeline_name)
    
    async def _process_message(self, message, pipeline: Pipeline) -> Dict[str, Any]:
        """Обработка сообщения через пайплайн"""
        processed_data = {
            'message_id': message.id,
            'text': message.text or "",
            'sender_id': message.sender_id,
            'date': message.date.isoformat(),
            'source': pipeline.source,
            'pipeline': pipeline.name
        }
        
        # Применение шагов обработки
        for step in pipeline.processing_steps:
            step_type = step.get('type')
            step_config = step.get('config', {})
            
            if step_type == 'filter':
                if not await self._apply_filter(processed_data, step_config):
                    return None  # Сообщение отфильтровано
            
            elif step_type == 'formatter':
                processed_data = await self._apply_formatter(processed_data, step_config)
            
            elif step_type == 'classifier':
                processed_data = await self._apply_classifier(processed_data, step_config)
        
        return processed_data
    
    async def _apply_filter(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Применение фильтра"""
        text = data.get('text', '').lower()
        
        # Фильтр по ключевым словам
        if 'keywords' in config:
            keywords = config['keywords']
            if keywords and not any(keyword in text for keyword in keywords):
                return False
        
        # Фильтр по исключающим словам
        if 'exclude_keywords' in config:
            exclude_keywords = config['exclude_keywords']
            if any(keyword in text for keyword in exclude_keywords):
                return False
        
        # Фильтр по длине
        if 'min_length' in config and len(text) < config['min_length']:
            return False
        
        return True
    
    async def _apply_formatter(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Применение форматирования"""
        if config.get('add_timestamps'):
            data['processed_at'] = datetime.now().isoformat()
        
        if config.get('add_source_info'):
            data['source_info'] = {
                'pipeline': data.get('pipeline'),
                'source': data.get('source')
            }
        
        if config.get('normalize_text'):
            data['text'] = data.get('text', '').strip()
        
        return data
    
    async def _apply_classifier(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Применение классификации"""
        text = data.get('text', '').lower()
        
        if 'urgency_keywords' in config:
            urgency_keywords = config['urgency_keywords']
            priority_levels = config.get('priority_levels', ['low', 'medium', 'high', 'critical'])
            
            urgency_count = sum(1 for keyword in urgency_keywords if keyword in text)
            
            if urgency_count >= 3:
                data['priority'] = priority_levels[3]  # critical
            elif urgency_count >= 2:
                data['priority'] = priority_levels[2]  # high
            elif urgency_count >= 1:
                data['priority'] = priority_levels[1]  # medium
            else:
                data['priority'] = priority_levels[0]  # low
        
        return data
    
    async def _send_to_destination(self, data: Dict[str, Any], destination: Destination):
        """Отправка данных в назначение"""
        try:
            if destination.type == 'telegram':
                await self._send_to_telegram(data, destination)
            elif destination.type == 'file':
                await self._send_to_file(data, destination)
            elif destination.type == 'database':
                await self._send_to_database(data, destination)
            
            destination.success_count += 1
            destination.last_success = datetime.now()
        
        except Exception as e:
            self.logger.error(f"Ошибка отправки в назначение {destination.name}: {e}")
            destination.error_count += 1
    
    async def _send_to_telegram(self, data: Dict[str, Any], destination: Destination):
        """Отправка в Telegram"""
        chat_id = destination.config.get('chat_id')
        if not chat_id:
            return
        
        text = data.get('text', '')
        if destination.config.get('format') == 'markdown':
            # Форматирование для markdown
            formatted_text = f"**Сообщение из {data.get('source')}**\n\n{text}"
        else:
            formatted_text = f"Сообщение из {data.get('source')}:\n\n{text}"
        
        await self.client.send_message(chat_id, formatted_text)
    
    async def _send_to_file(self, data: Dict[str, Any], destination: Destination):
        """Отправка в файл"""
        import aiofiles
        
        file_path = destination.config.get('path', './data/exports/')
        file_format = destination.config.get('format', 'json')
        
        Path(file_path).mkdir(parents=True, exist_ok=True)
        
        if file_format == 'json':
            filename = f"{file_path}/export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            async with aiofiles.open(filename, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    async def _send_to_database(self, data: Dict[str, Any], destination: Destination):
        """Отправка в базу данных"""
        # Здесь должна быть реализация для конкретной БД
        # Например, PostgreSQL, MySQL, SQLite
        pass
    
    async def get_all_statuses(self) -> Dict[str, Any]:
        """Получение статуса всех пайплайнов"""
        statuses = {}
        for pipeline_name in self.pipelines:
            status = await self.get_pipeline_status(pipeline_name)
            if status:
                statuses[pipeline_name] = status
        return statuses
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Получение общей статистики"""
        report = await self.monitor.generate_report()
        
        return {
            'report': report,
            'sources_count': len(self.sources),
            'destinations_count': len(self.destinations),
            'pipelines_count': len(self.pipelines),
            'active_sources': len([s for s in self.sources.values() if s.enabled]),
            'active_destinations': len([d for d in self.destinations.values() if d.enabled]),
            'active_pipelines': len([p for p in self.pipelines.values() if p.enabled])
        } 