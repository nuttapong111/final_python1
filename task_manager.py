"""
Python Task Manager Application
ระบบจัดการงานประจำวันด้วย Python
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:
    """
    Class สำหรับจัดการงานแต่ละงาน
    """
    
    def __init__(self, title: str, description: str, due_date: str, task_id: str = None):
        """
        สร้างงานใหม่
        
        Args:
            title (str): ชื่องาน
            description (str): คำอธิบายงาน
            due_date (str): วันที่ครบกำหนด (รูปแบบ YYYY-MM-DD)
            task_id (str, optional): รหัสเฉพาะของงาน
        """
        self.task_id = task_id or self._generate_id()
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def _generate_id(self) -> str:
        """
        สร้างรหัสเฉพาะสำหรับงาน
        """
        return f"TASK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def mark_completed(self):
        """
        ทำเครื่องหมายว่างานเสร็จสิ้น
        """
        self.completed = True
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """
        แปลงงานเป็น dictionary
        """
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """
        สร้าง Task จาก dictionary
        """
        task = cls(
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            task_id=data['task_id']
        )
        task.completed = data['completed']
        task.created_at = data['created_at']
        task.updated_at = data['updated_at']
        return task
    
    def __str__(self) -> str:
        """
        แสดงข้อมูลงานในรูปแบบ string
        """
        status = "✓ เสร็จสิ้น" if self.completed else "⏳ รอดำเนินการ"
        return f"[{self.task_id}] {self.title} - {status} (ครบกำหนด: {self.due_date})"


class TaskManager:
    """
    Class สำหรับจัดการงานทั้งหมด
    """
    
    def __init__(self, data_file: str = "tasks.json"):
        """
        สร้าง TaskManager ใหม่
        
        Args:
            data_file (str): ไฟล์สำหรับเก็บข้อมูลงาน
        """
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def add_task(self, title: str, description: str, due_date: str) -> Task:
        """
        เพิ่มงานใหม่
        
        Args:
            title (str): ชื่องาน
            description (str): คำอธิบายงาน
            due_date (str): วันที่ครบกำหนด
            
        Returns:
            Task: งานที่สร้างใหม่
        """
        if not self._validate_task_data(title, due_date):
            raise ValueError("ข้อมูลงานไม่ถูกต้อง")
        
        task = Task(title, description, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """
        ดึงงานทั้งหมด
        
        Returns:
            List[Task]: รายการงานทั้งหมด
        """
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """
        ดึงงานที่รอดำเนินการ
        
        Returns:
            List[Task]: รายการงานที่รอดำเนินการ
        """
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """
        ดึงงานที่เสร็จสิ้นแล้ว
        
        Returns:
            List[Task]: รายการงานที่เสร็จสิ้นแล้ว
        """
        return [task for task in self.tasks if task.completed]
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        ดึงงานตามรหัสเฉพาะ
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            Optional[Task]: งานที่พบ หรือ None ถ้าไม่พบ
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def mark_task_completed(self, task_id: str) -> bool:
        """
        ทำเครื่องหมายว่างานเสร็จสิ้น
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            bool: True ถ้าสำเร็จ, False ถ้าไม่พบงาน
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.save_tasks()
            return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        ลบงาน
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            bool: True ถ้าสำเร็จ, False ถ้าไม่พบงาน
        """
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False
    
    def search_tasks(self, keyword: str = None, due_date: str = None) -> List[Task]:
        """
        ค้นหางาน
        
        Args:
            keyword (str, optional): คำสำคัญสำหรับค้นหา
            due_date (str, optional): วันที่ครบกำหนดสำหรับค้นหา
            
        Returns:
            List[Task]: รายการงานที่พบ
        """
        results = []
        
        for task in self.tasks:
            match = True
            
            if keyword:
                keyword_lower = keyword.lower()
                if (keyword_lower not in task.title.lower() and 
                    keyword_lower not in task.description.lower()):
                    match = False
            
            if due_date and task.due_date != due_date:
                match = False
            
            if match:
                results.append(task)
        
        return results
    
    def _validate_task_data(self, title: str, due_date: str) -> bool:
        """
        ตรวจสอบความถูกต้องของข้อมูลงาน
        
        Args:
            title (str): ชื่องาน
            due_date (str): วันที่ครบกำหนด
            
        Returns:
            bool: True ถ้าข้อมูลถูกต้อง
        """
        if not title or not title.strip():
            return False
        
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def save_tasks(self):
        """
        บันทึกงานลงไฟล์ JSON
        """
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_tasks(self):
        """
        โหลดงานจากไฟล์ JSON
        """
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tasks = [Task.from_dict(task_data) for task_data in data.get('tasks', [])]
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            self.tasks = []
    
    def display_tasks(self, tasks: List[Task] = None):
        """
        แสดงรายการงาน
        
        Args:
            tasks (List[Task], optional): รายการงานที่ต้องการแสดง
        """
        if tasks is None:
            tasks = self.tasks
        
        if not tasks:
            print("ไม่พบงาน")
            return
        
        print(f"\n{'='*60}")
        print(f"รายการงาน ({len(tasks)} งาน)")
        print(f"{'='*60}")
        
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
            if task.description:
                print(f"   คำอธิบาย: {task.description}")
            print()
    
    def display_pending_tasks(self):
        """
        แสดงงานที่รอดำเนินการ
        """
        pending_tasks = self.get_pending_tasks()
        print("\n📋 งานที่รอดำเนินการ:")
        self.display_tasks(pending_tasks)
    
    def display_completed_tasks(self):
        """
        แสดงงานที่เสร็จสิ้นแล้ว
        """
        completed_tasks = self.get_completed_tasks()
        print("\n✅ งานที่เสร็จสิ้นแล้ว:")
        self.display_tasks(completed_tasks)
