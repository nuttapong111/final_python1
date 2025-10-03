"""
Python Task Manager Application
ระบบจัดการงานประจำวันด้วย Python
"""

import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional


class Task:
    """
    Class สำหรับจัดการงานแต่ละงาน
    """
    
    def __init__(self, task_id: str, title: str, description: str, due_date: str):
        """
        สร้างงานใหม่
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            title (str): ชื่องาน
            description (str): คำอธิบายงาน
            due_date (str): วันที่ครบกำหนด (รูปแบบ YYYY-MM-DD)
        """
        self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """
        แปลงงานเป็น dictionary สำหรับการบันทึก JSON
        
        Returns:
            Dict: ข้อมูลงานในรูปแบบ dictionary
        """
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """
        สร้างงานจาก dictionary
        
        Args:
            data (Dict): ข้อมูลงานในรูปแบบ dictionary
            
        Returns:
            Task: วัตถุงาน
        """
        task = cls(
            task_id=data['task_id'],
            title=data['title'],
            description=data['description'],
            due_date=data['due_date']
        )
        task.completed = data['completed']
        task.created_at = data['created_at']
        return task
    
    def mark_completed(self):
        """ทำเครื่องหมายว่างานเสร็จสิ้น"""
        self.completed = True
    
    def __str__(self) -> str:
        """แสดงข้อมูลงานในรูปแบบ string"""
        status = "✓ เสร็จสิ้น" if self.completed else "⏳ รอดำเนินการ"
        return f"[{self.task_id}] {self.title} - {status} (ครบกำหนด: {self.due_date})"


class TaskManager:
    """
    Class หลักสำหรับจัดการงานทั้งหมด
    """
    
    def __init__(self, data_file: str = "tasks.json"):
        """
        เริ่มต้น TaskManager
        
        Args:
            data_file (str): ไฟล์สำหรับเก็บข้อมูลงาน
        """
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def generate_task_id(self) -> str:
        """
        สร้างรหัสเฉพาะสำหรับงานใหม่
        
        Returns:
            str: รหัสเฉพาะของงาน
        """
        if not self.tasks:
            return "TASK001"
        
        # หาเลขที่มากที่สุดในรหัสงานที่มีอยู่
        max_num = 0
        for task in self.tasks:
            if task.task_id.startswith("TASK"):
                try:
                    num = int(task.task_id[4:])
                    max_num = max(max_num, num)
                except ValueError:
                    continue
        
        return f"TASK{max_num + 1:03d}"
    
    def add_task(self, title: str, description: str, due_date: str) -> bool:
        """
        เพิ่มงานใหม่
        
        Args:
            title (str): ชื่องาน
            description (str): คำอธิบายงาน
            due_date (str): วันที่ครบกำหนด
            
        Returns:
            bool: True หากเพิ่มสำเร็จ, False หากไม่สำเร็จ
        """
        # ตรวจสอบความถูกต้องของข้อมูล
        if not title.strip():
            print("❌ ข้อผิดพลาด: ชื่องานไม่สามารถเป็นค่าว่างได้")
            return False
        
        if not self._is_valid_date(due_date):
            print("❌ ข้อผิดพลาด: รูปแบบวันที่ไม่ถูกต้อง (ควรเป็น YYYY-MM-DD)")
            return False
        
        # สร้างงานใหม่
        task_id = self.generate_task_id()
        task = Task(task_id, title.strip(), description.strip(), due_date)
        self.tasks.append(task)
        
        print(f"✅ เพิ่มงานสำเร็จ: {task}")
        self.save_tasks()
        return True
    
    def _is_valid_date(self, date_string: str) -> bool:
        """
        ตรวจสอบความถูกต้องของรูปแบบวันที่
        
        Args:
            date_string (str): วันที่ในรูปแบบ string
            
        Returns:
            bool: True หากรูปแบบถูกต้อง, False หากไม่ถูกต้อง
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def view_tasks(self, show_completed: bool = True):
        """
        แสดงงานทั้งหมด
        
        Args:
            show_completed (bool): แสดงงานที่เสร็จสิ้นหรือไม่
        """
        if not self.tasks:
            print("📝 ไม่มีงานใดๆ ในระบบ")
            return
        
        pending_tasks = [task for task in self.tasks if not task.completed]
        completed_tasks = [task for task in self.tasks if task.completed]
        
        print("\n" + "="*60)
        print("📋 รายการงานทั้งหมด")
        print("="*60)
        
        # แสดงงานที่รอดำเนินการ
        if pending_tasks:
            print(f"\n⏳ งานที่รอดำเนินการ ({len(pending_tasks)} งาน):")
            print("-" * 40)
            for task in pending_tasks:
                print(f"  {task}")
                if task.description:
                    print(f"    📝 คำอธิบาย: {task.description}")
                print()
        else:
            print("\n✅ ไม่มีงานที่รอดำเนินการ")
        
        # แสดงงานที่เสร็จสิ้น
        if show_completed and completed_tasks:
            print(f"\n✅ งานที่เสร็จสิ้น ({len(completed_tasks)} งาน):")
            print("-" * 40)
            for task in completed_tasks:
                print(f"  {task}")
                if task.description:
                    print(f"    📝 คำอธิบาย: {task.description}")
                print()
        elif show_completed:
            print("\n📝 ไม่มีงานที่เสร็จสิ้น")
    
    def mark_task_completed(self, task_id: str) -> bool:
        """
        ทำเครื่องหมายว่างานเสร็จสิ้น
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            bool: True หากทำเครื่องหมายสำเร็จ, False หากไม่พบงาน
        """
        task = self.find_task_by_id(task_id)
        if task:
            if task.completed:
                print(f"ℹ️  งาน {task_id} ได้ทำเครื่องหมายเสร็จสิ้นแล้ว")
            else:
                task.mark_completed()
                print(f"✅ ทำเครื่องหมายงาน {task_id} เสร็จสิ้นแล้ว")
                self.save_tasks()
            return True
        else:
            print(f"❌ ไม่พบงานที่มีรหัส {task_id}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """
        ลบงาน
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            bool: True หากลบสำเร็จ, False หากไม่พบงาน
        """
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            print(f"🗑️  ลบงาน {task_id} เรียบร้อยแล้ว")
            self.save_tasks()
            return True
        else:
            print(f"❌ ไม่พบงานที่มีรหัส {task_id}")
            return False
    
    def find_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        ค้นหางานตามรหัสเฉพาะ
        
        Args:
            task_id (str): รหัสเฉพาะของงาน
            
        Returns:
            Optional[Task]: วัตถุงานหากพบ, None หากไม่พบ
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def search_tasks(self, keyword: str = "", due_date: str = "") -> List[Task]:
        """
        ค้นหางานตามคำสำคัญหรือวันที่ครบกำหนด
        
        Args:
            keyword (str): คำสำคัญสำหรับค้นหา
            due_date (str): วันที่ครบกำหนดสำหรับค้นหา
            
        Returns:
            List[Task]: รายการงานที่ตรงกับเงื่อนไข
        """
        results = []
        
        for task in self.tasks:
            match = True
            
            # ค้นหาตามคำสำคัญ
            if keyword:
                keyword_lower = keyword.lower()
                if (keyword_lower not in task.title.lower() and 
                    keyword_lower not in task.description.lower()):
                    match = False
            
            # ค้นหาตามวันที่ครบกำหนด
            if due_date and task.due_date != due_date:
                match = False
            
            if match:
                results.append(task)
        
        return results
    
    def display_search_results(self, results: List[Task]):
        """
        แสดงผลการค้นหา
        
        Args:
            results (List[Task]): รายการงานที่ค้นหาได้
        """
        if not results:
            print("🔍 ไม่พบงานที่ตรงกับเงื่อนไขการค้นหา")
            return
        
        print(f"\n🔍 ผลการค้นหา ({len(results)} งาน):")
        print("-" * 50)
        for task in results:
            print(f"  {task}")
            if task.description:
                print(f"    📝 คำอธิบาย: {task.description}")
            print()
    
    def save_tasks(self):
        """บันทึกงานทั้งหมดลงไฟล์ JSON"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการบันทึกไฟล์: {e}")
    
    def load_tasks(self):
        """โหลดงานทั้งหมดจากไฟล์ JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการโหลดไฟล์: {e}")
            self.tasks = []
    
    def get_statistics(self) -> Dict:
        """
        รับสถิติของงาน
        
        Returns:
            Dict: สถิติของงาน
        """
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
