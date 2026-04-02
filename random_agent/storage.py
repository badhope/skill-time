"""
持久化存储 (Persistence Storage)

提供数据持久化功能：
- JSON 文件存储
- SQLite 数据库存储
- 会话管理
- 数据导入导出
"""

import json
import sqlite3
import pickle
import time
from typing import Any, Optional, Dict, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
import shutil


@dataclass
class Session:
    """会话数据"""
    session_id: str
    created_at: float
    updated_at: float
    agent_state: Dict[str, Any]
    memory_data: List[Dict[str, Any]]
    thinking_history: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class JSONStorage:
    """
    JSON 文件存储
    
    简单的文件存储，适合小型应用
    """
    
    def __init__(self, storage_dir: str = "./data"):
        """
        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, data: Any, subdir: Optional[str] = None) -> str:
        """
        保存数据
        
        Args:
            key: 数据键
            data: 数据
            subdir: 子目录
        
        Returns:
            文件路径
        """
        if subdir:
            target_dir = self.storage_dir / subdir
        else:
            target_dir = self.storage_dir
        
        target_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = target_dir / f"{key}.json"
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(filepath)
    
    def load(self, key: str, subdir: Optional[str] = None) -> Optional[Any]:
        """
        加载数据
        
        Args:
            key: 数据键
            subdir: 子目录
        
        Returns:
            数据
        """
        if subdir:
            filepath = self.storage_dir / subdir / f"{key}.json"
        else:
            filepath = self.storage_dir / f"{key}.json"
        
        if not filepath.exists():
            return None
        
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def delete(self, key: str, subdir: Optional[str] = None) -> bool:
        """删除数据"""
        if subdir:
            filepath = self.storage_dir / subdir / f"{key}.json"
        else:
            filepath = self.storage_dir / f"{key}.json"
        
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    
    def list_keys(self, subdir: Optional[str] = None) -> List[str]:
        """列出所有键"""
        if subdir:
            target_dir = self.storage_dir / subdir
        else:
            target_dir = self.storage_dir
        
        if not target_dir.exists():
            return []
        
        return [f.stem for f in target_dir.glob("*.json")]


class SQLiteStorage:
    """
    SQLite 数据库存储
    
    适合需要查询和索引的场景
    """
    
    def __init__(self, db_path: str = "./data/random_agent.db"):
        """
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._connection: Optional[sqlite3.Connection] = None
        
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        if self._connection is None:
            self._connection = sqlite3.connect(str(self.db_path))
        return self._connection
    
    def close(self):
        """关闭数据库连接"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def __del__(self):
        """析构函数，确保连接关闭"""
        self.close()
    
    def _init_db(self):
        """初始化数据库"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at REAL,
                updated_at REAL,
                agent_state TEXT,
                memory_data TEXT,
                thinking_history TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                memory_id TEXT PRIMARY KEY,
                session_id TEXT,
                content TEXT,
                memory_type TEXT,
                importance REAL,
                created_at REAL,
                access_count INTEGER,
                metadata TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS thinking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp REAL,
                thought TEXT,
                level TEXT,
                strength REAL,
                metadata TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_created 
            ON sessions(created_at)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_memories_session 
            ON memories(session_id)
        """)
        
        conn.commit()
    
    def save_session(self, session: Session) -> bool:
        """保存会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO sessions 
                (session_id, created_at, updated_at, agent_state, 
                 memory_data, thinking_history, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.created_at,
                session.updated_at,
                json.dumps(session.agent_state),
                json.dumps(session.memory_data),
                json.dumps(session.thinking_history),
                json.dumps(session.metadata)
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"保存会话失败: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """加载会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, created_at, updated_at, agent_state,
                       memory_data, thinking_history, metadata
                FROM sessions
                WHERE session_id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            
            if row:
                return Session(
                    session_id=row[0],
                    created_at=row[1],
                    updated_at=row[2],
                    agent_state=json.loads(row[3]),
                    memory_data=json.loads(row[4]),
                    thinking_history=json.loads(row[5]),
                    metadata=json.loads(row[6])
                )
            
            return None
        except Exception as e:
            print(f"加载会话失败: {e}")
            return None
    
    def list_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT session_id, created_at, updated_at, metadata
                FROM sessions
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            
            return [
                {
                    "session_id": row[0],
                    "created_at": row[1],
                    "updated_at": row[2],
                    "metadata": json.loads(row[3])
                }
                for row in rows
            ]
        except Exception as e:
            print(f"列出会话失败: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM memories WHERE session_id = ?",
                (session_id,)
            )
            
            cursor.execute(
                "DELETE FROM thinking_history WHERE session_id = ?",
                (session_id,)
            )
            
            cursor.execute(
                "DELETE FROM sessions WHERE session_id = ?",
                (session_id,)
            )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"删除会话失败: {e}")
            return False
    
    def save_memory(
        self,
        memory_id: str,
        session_id: str,
        content: str,
        memory_type: str,
        importance: float,
        metadata: Optional[Dict] = None
    ) -> bool:
        """保存记忆"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO memories
                (memory_id, session_id, content, memory_type, 
                 importance, created_at, access_count, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_id,
                session_id,
                content,
                memory_type,
                importance,
                time.time(),
                0,
                json.dumps(metadata or {})
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"保存记忆失败: {e}")
            return False
    
    def search_memories(
        self,
        query: str,
        session_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """搜索记忆"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if session_id:
                cursor.execute("""
                    SELECT memory_id, session_id, content, memory_type,
                           importance, created_at, access_count, metadata
                    FROM memories
                    WHERE session_id = ? AND content LIKE ?
                    ORDER BY importance DESC, created_at DESC
                    LIMIT ?
                """, (session_id, f"%{query}%", limit))
            else:
                cursor.execute("""
                    SELECT memory_id, session_id, content, memory_type,
                           importance, created_at, access_count, metadata
                    FROM memories
                    WHERE content LIKE ?
                    ORDER BY importance DESC, created_at DESC
                    LIMIT ?
                """, (f"%{query}%", limit))
            
            rows = cursor.fetchall()
            
            return [
                {
                    "memory_id": row[0],
                    "session_id": row[1],
                    "content": row[2],
                    "memory_type": row[3],
                    "importance": row[4],
                    "created_at": row[5],
                    "access_count": row[6],
                    "metadata": json.loads(row[7])
                }
                for row in rows
            ]
        except Exception as e:
            print(f"搜索记忆失败: {e}")
            return []


class SessionManager:
    """
    会话管理器
    
    管理智能体的会话状态
    """
    
    def __init__(self, storage: Optional[SQLiteStorage] = None):
        self.storage = storage or SQLiteStorage()
        self._current_session: Optional[Session] = None
    
    def create_session(
        self,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Session:
        """创建新会话"""
        import uuid
        
        session = Session(
            session_id=session_id or str(uuid.uuid4()),
            created_at=time.time(),
            updated_at=time.time(),
            agent_state={},
            memory_data=[],
            thinking_history=[],
            metadata=metadata or {}
        )
        
        self.storage.save_session(session)
        self._current_session = session
        
        return session
    
    def get_current_session(self) -> Optional[Session]:
        """获取当前会话"""
        return self._current_session
    
    def load_session(self, session_id: str) -> Optional[Session]:
        """加载会话"""
        session = self.storage.load_session(session_id)
        if session:
            self._current_session = session
        return session
    
    def save_current_session(self):
        """保存当前会话"""
        if self._current_session:
            self._current_session.updated_at = time.time()
            self.storage.save_session(self._current_session)
    
    def update_agent_state(self, state: Dict[str, Any]):
        """更新智能体状态"""
        if self._current_session:
            self._current_session.agent_state = state
            self.save_current_session()
    
    def add_thinking(self, thought: Dict[str, Any]):
        """添加思考记录"""
        if self._current_session:
            self._current_session.thinking_history.append(thought)
            self.save_current_session()
    
    def add_memory(self, memory: Dict[str, Any]):
        """添加记忆"""
        if self._current_session:
            self._current_session.memory_data.append(memory)
            self.save_current_session()
    
    def list_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出所有会话"""
        return self.storage.list_sessions(limit)
    
    def delete_session(self, session_id: str) -> bool:
        """删除会话"""
        if self._current_session and self._current_session.session_id == session_id:
            self._current_session = None
        
        return self.storage.delete_session(session_id)


def export_session(session: Session, filepath: str, format: str = "json"):
    """
    导出会话
    
    Args:
        session: 会话对象
        filepath: 文件路径
        format: 格式 (json/pickle)
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(session), f, ensure_ascii=False, indent=2)
    elif format == "pickle":
        with open(path, "wb") as f:
            pickle.dump(session, f)
    else:
        raise ValueError(f"不支持的格式: {format}")


def import_session(filepath: str, format: str = "json") -> Session:
    """
    导入会话
    
    Args:
        filepath: 文件路径
        format: 格式 (json/pickle)
    
    Returns:
        会话对象
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    if format == "json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Session(**data)
    elif format == "pickle":
        with open(path, "rb") as f:
            return pickle.load(f)
    else:
        raise ValueError(f"不支持的格式: {format}")
