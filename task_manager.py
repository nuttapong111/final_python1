#!/usr/bin/env python3
"""
Python Task Manager Application
ระบบจัดการงานประจำวันด้วย Command-Line Interface
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class Task:
    """Class สำหรับจัดการข้อมูลงานแต่ละชิ้น"""
    
    def __init__(self, title: str, description: str, due_date: str):
        self.id = str(uuid.uuid4())[:8]  # สร้าง ID แบบสุ่ม 8 หลัก
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict:
        """แปลง Task object เป็น dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """สร้าง Task object จาก dictionary"""
        task = cls(data['title'], data['description'], data['due_date'])
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = data['created_at']
        return task


class TaskManager:
    """Class หลักสำหรับจัดการงานทั้งหมด"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """โหลดข้อมูลงานจากไฟล์ JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                print(f"โหลดข้อมูลงาน {len(self.tasks)} ชิ้นเรียบร้อยแล้ว")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
                self.tasks = []
        else:
            print("ไม่พบไฟล์ข้อมูล เริ่มต้นด้วยรายการงานว่าง")
    
    def save_tasks(self) -> None:
        """บันทึกข้อมูลงานลงไฟล์ JSON"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("บันทึกข้อมูลเรียบร้อยแล้ว")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")
    
    def add_task(self, title: str, description: str, due_date: str) -> bool:
        """เพิ่มงานใหม่"""
        if not title.strip():
            print("❌ ชื่องานไม่สามารถเป็นค่าว่างได้")
            return False
        
        if not self._validate_date(due_date):
            print("❌ รูปแบบวันที่ไม่ถูกต้อง ใช้รูปแบบ YYYY-MM-DD")
            return False
        
        task = Task(title.strip(), description.strip(), due_date)
        self.tasks.append(task)
        print(f"✅ เพิ่มงานใหม่เรียบร้อยแล้ว (ID: {task.id})")
        return True
    
    def _validate_date(self, date_string: str) -> bool:
        """ตรวจสอบรูปแบบวันที่"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def view_tasks(self, show_completed: bool = True) -> None:
        """แสดงรายการงานทั้งหมด"""
        if not self.tasks:
            print("📝 ไม่มีงานในระบบ")
            return
        
        pending_tasks = [task for task in self.tasks if not task.completed]
        completed_tasks = [task for task in self.tasks if task.completed]
        
        print("\n" + "="*60)
        print("📋 รายการงานทั้งหมด")
        print("="*60)
        
        if pending_tasks:
            print(f"\n🔄 งานรอดำเนินการ ({len(pending_tasks)} ชิ้น):")
            print("-" * 40)
            for task in pending_tasks:
                status = "⏰" if self._is_overdue(task.due_date) else "📅"
                print(f"{status} ID: {task.id}")
                print(f"   📌 ชื่อ: {task.title}")
                print(f"   📝 คำอธิบาย: {task.description}")
                print(f"   📅 วันที่ครบกำหนด: {task.due_date}")
                print(f"   🕒 สร้างเมื่อ: {task.created_at}")
                print()
        
        if show_completed and completed_tasks:
            print(f"\n✅ งานเสร็จสิ้น ({len(completed_tasks)} ชิ้น):")
            print("-" * 40)
            for task in completed_tasks:
                print(f"✅ ID: {task.id}")
                print(f"   📌 ชื่อ: {task.title}")
                print(f"   📝 คำอธิบาย: {task.description}")
                print(f"   📅 วันที่ครบกำหนด: {task.due_date}")
                print()
    
    def _is_overdue(self, due_date: str) -> bool:
        """ตรวจสอบว่างานเลยกำหนดหรือไม่"""
        try:
            due = datetime.strptime(due_date, "%Y-%m-%d")
            return due.date() < datetime.now().date()
        except ValueError:
            return False
    
    def mark_completed(self, task_id: str) -> bool:
        """ทำเครื่องหมายว่างานเสร็จสิ้น"""
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"❌ ไม่พบงาน ID: {task_id}")
            return False
        
        if task.completed:
            print(f"⚠️  งาน ID: {task_id} เสร็จสิ้นแล้ว")
            return False
        
        task.completed = True
        print(f"✅ ทำเครื่องหมายว่างาน '{task.title}' เสร็จสิ้นแล้ว")
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """ลบงาน"""
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"❌ ไม่พบงาน ID: {task_id}")
            return False
        
        self.tasks.remove(task)
        print(f"🗑️  ลบงาน '{task.title}' เรียบร้อยแล้ว")
        return True
    
    def _find_task_by_id(self, task_id: str) -> Optional[Task]:
        """ค้นหางานตาม ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def search_tasks(self, keyword: str = "", due_date: str = "") -> None:
        """ค้นหางานตามคำสำคัญหรือวันที่"""
        results = []
        
        for task in self.tasks:
            match = True
            
            if keyword:
                keyword_lower = keyword.lower()
                if not (keyword_lower in task.title.lower() or 
                       keyword_lower in task.description.lower()):
                    match = False
            
            if due_date and match:
                if task.due_date != due_date:
                    match = False
            
            if match:
                results.append(task)
        
        if not results:
            print("🔍 ไม่พบงานที่ตรงกับเงื่อนไขการค้นหา")
            return
        
        print(f"\n🔍 ผลการค้นหา ({len(results)} ชิ้น):")
        print("="*50)
        for task in results:
            status = "✅" if task.completed else "🔄"
            overdue = "⏰" if not task.completed and self._is_overdue(task.due_date) else ""
            print(f"{status}{overdue} ID: {task.id}")
            print(f"   📌 ชื่อ: {task.title}")
            print(f"   📝 คำอธิบาย: {task.description}")
            print(f"   📅 วันที่ครบกำหนด: {task.due_date}")
            print()


class TaskManagerCLI:
    """Command-Line Interface สำหรับ Task Manager"""
    
    def __init__(self):
        self.task_manager = TaskManager()
    
    def display_menu(self) -> None:
        """แสดงเมนูหลัก"""
        print("\n" + "="*50)
        print("📋 Python Task Manager")
        print("="*50)
        print("1. เพิ่มงานใหม่")
        print("2. ดูงานทั้งหมด")
        print("3. ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("4. ลบงาน")
        print("5. ค้นหางาน")
        print("6. บันทึกข้อมูล")
        print("7. ออกจากโปรแกรม")
        print("="*50)
    
    def get_user_input(self, prompt: str) -> str:
        """รับข้อมูลจากผู้ใช้"""
        return input(f"{prompt}: ").strip()
    
    def add_task_interactive(self) -> None:
        """เพิ่มงานใหม่แบบโต้ตอบ"""
        print("\n📝 เพิ่มงานใหม่")
        print("-" * 30)
        
        title = self.get_user_input("ชื่องาน")
        if not title:
            print("❌ ชื่องานไม่สามารถเป็นค่าว่างได้")
            return
        
        description = self.get_user_input("คำอธิบาย (ไม่บังคับ)")
        due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD)")
        
        if self.task_manager.add_task(title, description, due_date):
            self.task_manager.save_tasks()
    
    def mark_completed_interactive(self) -> None:
        """ทำเครื่องหมายว่างานเสร็จสิ้นแบบโต้ตอบ"""
        print("\n✅ ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("-" * 40)
        
        # แสดงงานที่ยังไม่เสร็จ
        pending_tasks = [task for task in self.task_manager.tasks if not task.completed]
        if not pending_tasks:
            print("📝 ไม่มีงานรอดำเนินการ")
            return
        
        print("งานรอดำเนินการ:")
        for task in pending_tasks:
            overdue = "⏰" if self.task_manager._is_overdue(task.due_date) else "📅"
            print(f"  {overdue} {task.id}: {task.title}")
        
        task_id = self.get_user_input("\nใส่ ID ของงานที่ต้องการทำเครื่องหมายเสร็จสิ้น")
        if self.task_manager.mark_completed(task_id):
            self.task_manager.save_tasks()
    
    def delete_task_interactive(self) -> None:
        """ลบงานแบบโต้ตอบ"""
        print("\n🗑️  ลบงาน")
        print("-" * 20)
        
        if not self.task_manager.tasks:
            print("📝 ไม่มีงานในระบบ")
            return
        
        # แสดงงานทั้งหมด
        print("งานทั้งหมด:")
        for task in self.task_manager.tasks:
            status = "✅" if task.completed else "🔄"
            print(f"  {status} {task.id}: {task.title}")
        
        task_id = self.get_user_input("\nใส่ ID ของงานที่ต้องการลบ")
        confirm = self.get_user_input("ยืนยันการลบ? (y/N)")
        
        if confirm.lower() in ['y', 'yes']:
            if self.task_manager.delete_task(task_id):
                self.task_manager.save_tasks()
        else:
            print("❌ ยกเลิกการลบงาน")
    
    def search_tasks_interactive(self) -> None:
        """ค้นหางานแบบโต้ตอบ"""
        print("\n🔍 ค้นหางาน")
        print("-" * 20)
        
        keyword = self.get_user_input("คำสำคัญ (ไม่บังคับ)")
        due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD) (ไม่บังคับ)")
        
        self.task_manager.search_tasks(keyword, due_date)
    
    def run(self) -> None:
        """เริ่มต้นโปรแกรม"""
        print("🎉 ยินดีต้อนรับสู่ Python Task Manager!")
        
        while True:
            self.display_menu()
            choice = self.get_user_input("เลือกตัวเลือก (1-7)")
            
            if choice == "1":
                self.add_task_interactive()
            elif choice == "2":
                self.task_manager.view_tasks()
            elif choice == "3":
                self.mark_completed_interactive()
            elif choice == "4":
                self.delete_task_interactive()
            elif choice == "5":
                self.search_tasks_interactive()
            elif choice == "6":
                self.task_manager.save_tasks()
            elif choice == "7":
                print("👋 ขอบคุณที่ใช้ Python Task Manager!")
                break
            else:
                print("❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-7")
            
            input("\nกด Enter เพื่อดำเนินการต่อ...")


def main():
    """ฟังก์ชันหลัก"""
    try:
        cli = TaskManagerCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 โปรแกรมถูกยกเลิกโดยผู้ใช้")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
    main()
