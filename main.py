#!/usr/bin/env python3
"""
Python Task Manager - Command Line Interface
แอปพลิเคชันจัดการงานประจำวันด้วย Python
"""

import sys
from datetime import datetime
from task_manager import TaskManager


class TaskManagerCLI:
    """
    Command Line Interface สำหรับ Task Manager
    """
    
    def __init__(self):
        """
        สร้าง CLI ใหม่
        """
        self.task_manager = TaskManager()
        self.running = True
    
    def display_menu(self):
        """
        แสดงเมนูหลัก
        """
        print("\n" + "="*50)
        print("📋 Python Task Manager")
        print("="*50)
        print("1. เพิ่มงานใหม่")
        print("2. ดูงานทั้งหมด")
        print("3. ดูงานที่รอดำเนินการ")
        print("4. ดูงานที่เสร็จสิ้นแล้ว")
        print("5. ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("6. ลบงาน")
        print("7. ค้นหางาน")
        print("8. ออกจากโปรแกรม")
        print("="*50)
    
    def get_user_input(self, prompt: str) -> str:
        """
        รับข้อมูลจากผู้ใช้
        
        Args:
            prompt (str): ข้อความที่แสดงให้ผู้ใช้
            
        Returns:
            str: ข้อมูลที่ผู้ใช้ป้อน
        """
        return input(f"{prompt}: ").strip()
    
    def add_task(self):
        """
        เพิ่มงานใหม่
        """
        print("\n📝 เพิ่มงานใหม่")
        print("-" * 30)
        
        title = self.get_user_input("ชื่องาน")
        if not title:
            print("❌ ชื่องานไม่สามารถเป็นค่าว่างได้")
            return
        
        description = self.get_user_input("คำอธิบายงาน (ไม่บังคับ)")
        due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD)")
        
        try:
            task = self.task_manager.add_task(title, description, due_date)
            print(f"✅ เพิ่มงานสำเร็จ! รหัสงาน: {task.task_id}")
        except ValueError as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
    
    def view_all_tasks(self):
        """
        ดูงานทั้งหมด
        """
        print("\n📋 งานทั้งหมด")
        print("-" * 30)
        self.task_manager.display_tasks()
    
    def view_pending_tasks(self):
        """
        ดูงานที่รอดำเนินการ
        """
        self.task_manager.display_pending_tasks()
    
    def view_completed_tasks(self):
        """
        ดูงานที่เสร็จสิ้นแล้ว
        """
        self.task_manager.display_completed_tasks()
    
    def mark_task_completed(self):
        """
        ทำเครื่องหมายว่างานเสร็จสิ้น
        """
        print("\n✅ ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("-" * 40)
        
        # แสดงงานที่รอดำเนินการ
        pending_tasks = self.task_manager.get_pending_tasks()
        if not pending_tasks:
            print("❌ ไม่มีงานที่รอดำเนินการ")
            return
        
        print("งานที่รอดำเนินการ:")
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task}")
        
        task_id = self.get_user_input("\nรหัสงานที่ต้องการทำเครื่องหมายเสร็จสิ้น")
        
        if self.task_manager.mark_task_completed(task_id):
            print("✅ ทำเครื่องหมายว่างานเสร็จสิ้นสำเร็จ!")
        else:
            print("❌ ไม่พบงานที่ระบุ")
    
    def delete_task(self):
        """
        ลบงาน
        """
        print("\n🗑️ ลบงาน")
        print("-" * 20)
        
        # แสดงงานทั้งหมด
        all_tasks = self.task_manager.get_all_tasks()
        if not all_tasks:
            print("❌ ไม่มีงานในระบบ")
            return
        
        print("งานทั้งหมด:")
        for i, task in enumerate(all_tasks, 1):
            print(f"{i}. {task}")
        
        task_id = self.get_user_input("\nรหัสงานที่ต้องการลบ")
        
        if self.task_manager.delete_task(task_id):
            print("✅ ลบงานสำเร็จ!")
        else:
            print("❌ ไม่พบงานที่ระบุ")
    
    def search_tasks(self):
        """
        ค้นหางาน
        """
        print("\n🔍 ค้นหางาน")
        print("-" * 20)
        
        keyword = self.get_user_input("คำสำคัญ (ไม่บังคับ)")
        due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD) (ไม่บังคับ)")
        
        # แปลงค่าว่างเป็น None
        keyword = keyword if keyword else None
        due_date = due_date if due_date else None
        
        results = self.task_manager.search_tasks(keyword, due_date)
        
        if results:
            print(f"\nพบ {len(results)} งาน:")
            self.task_manager.display_tasks(results)
        else:
            print("❌ ไม่พบงานที่ตรงกับเงื่อนไขการค้นหา")
    
    def run(self):
        """
        เริ่มต้นการทำงานของ CLI
        """
        print("🎉 ยินดีต้อนรับสู่ Python Task Manager!")
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("เลือกตัวเลือก (1-8)")
                
                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.view_all_tasks()
                elif choice == "3":
                    self.view_pending_tasks()
                elif choice == "4":
                    self.view_completed_tasks()
                elif choice == "5":
                    self.mark_task_completed()
                elif choice == "6":
                    self.delete_task()
                elif choice == "7":
                    self.search_tasks()
                elif choice == "8":
                    print("👋 ขอบคุณที่ใช้ Python Task Manager!")
                    self.running = False
                else:
                    print("❌ กรุณาเลือกตัวเลือกที่ถูกต้อง (1-8)")
                
                if self.running:
                    input("\nกด Enter เพื่อดำเนินการต่อ...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ขอบคุณที่ใช้ Python Task Manager!")
                self.running = False
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")
                input("กด Enter เพื่อดำเนินการต่อ...")


def main():
    """
    ฟังก์ชันหลัก
    """
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
