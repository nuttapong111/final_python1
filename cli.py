"""
Command-Line Interface สำหรับ Python Task Manager
"""

from task_manager import TaskManager
from datetime import datetime


class TaskManagerCLI:
    """
    Class สำหรับจัดการ Command-Line Interface
    """
    
    def __init__(self):
        """เริ่มต้น CLI"""
        self.task_manager = TaskManager()
        self.running = True
    
    def display_menu(self):
        """แสดงเมนูหลัก"""
        print("\n" + "="*60)
        print("📋 Python Task Manager")
        print("="*60)
        print("1. ➕ เพิ่มงานใหม่")
        print("2. 👀 ดูงานทั้งหมด")
        print("3. ✅ ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("4. 🗑️  ลบงาน")
        print("5. 🔍 ค้นหางาน")
        print("6. 📊 แสดงสถิติ")
        print("7. ❌ ออกจากโปรแกรม")
        print("="*60)
    
    def get_user_input(self, prompt: str) -> str:
        """
        รับข้อมูลจากผู้ใช้
        
        Args:
            prompt (str): ข้อความแสดงให้ผู้ใช้ป้อนข้อมูล
            
        Returns:
            str: ข้อมูลที่ผู้ใช้ป้อน
        """
        return input(f"{prompt}: ").strip()
    
    def add_task_interactive(self):
        """เพิ่มงานใหม่แบบโต้ตอบ"""
        print("\n➕ เพิ่มงานใหม่")
        print("-" * 30)
        
        title = self.get_user_input("ชื่องาน")
        if not title:
            print("❌ ชื่องานไม่สามารถเป็นค่าว่างได้")
            return
        
        description = self.get_user_input("คำอธิบาย (ไม่บังคับ)")
        
        while True:
            due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD)")
            if self.task_manager._is_valid_date(due_date):
                break
            print("❌ รูปแบบวันที่ไม่ถูกต้อง กรุณาใช้รูปแบบ YYYY-MM-DD")
        
        self.task_manager.add_task(title, description, due_date)
    
    def view_tasks_interactive(self):
        """ดูงานทั้งหมดแบบโต้ตอบ"""
        print("\n👀 ดูงานทั้งหมด")
        print("-" * 30)
        
        show_completed = self.get_user_input("แสดงงานที่เสร็จสิ้นด้วยหรือไม่? (y/n)").lower()
        show_completed = show_completed in ['y', 'yes', 'ใช่']
        
        self.task_manager.view_tasks(show_completed)
    
    def mark_task_completed_interactive(self):
        """ทำเครื่องหมายว่างานเสร็จสิ้นแบบโต้ตอบ"""
        print("\n✅ ทำเครื่องหมายว่างานเสร็จสิ้น")
        print("-" * 30)
        
        # แสดงงานที่ยังไม่เสร็จ
        pending_tasks = [task for task in self.task_manager.tasks if not task.completed]
        if not pending_tasks:
            print("📝 ไม่มีงานที่รอดำเนินการ")
            return
        
        print("งานที่รอดำเนินการ:")
        for task in pending_tasks:
            print(f"  {task}")
        
        task_id = self.get_user_input("\nกรุณาใส่รหัสงานที่ต้องการทำเครื่องหมายเสร็จสิ้น")
        self.task_manager.mark_task_completed(task_id)
    
    def delete_task_interactive(self):
        """ลบงานแบบโต้ตอบ"""
        print("\n🗑️  ลบงาน")
        print("-" * 30)
        
        if not self.task_manager.tasks:
            print("📝 ไม่มีงานใดๆ ในระบบ")
            return
        
        # แสดงงานทั้งหมด
        self.task_manager.view_tasks()
        
        task_id = self.get_user_input("กรุณาใส่รหัสงานที่ต้องการลบ")
        
        # ยืนยันการลบ
        confirm = self.get_user_input(f"คุณแน่ใจหรือไม่ว่าต้องการลบงาน {task_id}? (y/n)").lower()
        if confirm in ['y', 'yes', 'ใช่']:
            self.task_manager.delete_task(task_id)
        else:
            print("❌ ยกเลิกการลบงาน")
    
    def search_tasks_interactive(self):
        """ค้นหางานแบบโต้ตอบ"""
        print("\n🔍 ค้นหางาน")
        print("-" * 30)
        
        keyword = self.get_user_input("คำสำคัญสำหรับค้นหา (ไม่บังคับ)")
        due_date = self.get_user_input("วันที่ครบกำหนด (YYYY-MM-DD) (ไม่บังคับ)")
        
        # ตรวจสอบรูปแบบวันที่
        if due_date and not self.task_manager._is_valid_date(due_date):
            print("❌ รูปแบบวันที่ไม่ถูกต้อง")
            return
        
        results = self.task_manager.search_tasks(keyword, due_date)
        self.task_manager.display_search_results(results)
    
    def show_statistics(self):
        """แสดงสถิติ"""
        print("\n📊 สถิติงาน")
        print("-" * 30)
        
        stats = self.task_manager.get_statistics()
        print(f"📈 งานทั้งหมด: {stats['total']} งาน")
        print(f"✅ งานที่เสร็จสิ้น: {stats['completed']} งาน")
        print(f"⏳ งานที่รอดำเนินการ: {stats['pending']} งาน")
        print(f"📊 อัตราการเสร็จสิ้น: {stats['completion_rate']:.1f}%")
    
    def run(self):
        """เริ่มต้นการทำงานของ CLI"""
        print("🎉 ยินดีต้อนรับสู่ Python Task Manager!")
        
        while self.running:
            try:
                self.display_menu()
                choice = self.get_user_input("กรุณาเลือกตัวเลือก (1-7)")
                
                if choice == "1":
                    self.add_task_interactive()
                elif choice == "2":
                    self.view_tasks_interactive()
                elif choice == "3":
                    self.mark_task_completed_interactive()
                elif choice == "4":
                    self.delete_task_interactive()
                elif choice == "5":
                    self.search_tasks_interactive()
                elif choice == "6":
                    self.show_statistics()
                elif choice == "7":
                    print("👋 ขอบคุณที่ใช้ Python Task Manager!")
                    self.running = False
                else:
                    print("❌ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1-7")
                
                if self.running:
                    input("\nกด Enter เพื่อดำเนินการต่อ...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ขอบคุณที่ใช้ Python Task Manager!")
                self.running = False
            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาด: {e}")
                input("กด Enter เพื่อดำเนินการต่อ...")


def main():
    """ฟังก์ชันหลัก"""
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
