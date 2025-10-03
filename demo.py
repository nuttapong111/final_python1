"""
Demo script for Python Task Manager
สคริปต์สาธิตการใช้งาน Task Manager
"""

from task_manager import TaskManager
from datetime import datetime, timedelta


def demo_task_manager():
    """
    สาธิตการใช้งาน Task Manager
    """
    print("🎯 Python Task Manager Demo")
    print("=" * 50)
    
    # สร้าง TaskManager
    tm = TaskManager("demo_tasks.json")
    
    # เพิ่มงานตัวอย่าง
    print("\n📝 เพิ่มงานตัวอย่าง...")
    
    # งานที่ 1
    task1 = tm.add_task(
        "ประชุมทีมพัฒนา",
        "ประชุมรายสัปดาห์เพื่ออัปเดตความคืบหน้าโปรเจกต์",
        (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    )
    print(f"✅ เพิ่มงาน: {task1.title}")
    
    # งานที่ 2
    task2 = tm.add_task(
        "เขียนเอกสาร API",
        "เขียนเอกสาร API สำหรับระบบ Task Manager",
        (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    )
    print(f"✅ เพิ่มงาน: {task2.title}")
    
    # งานที่ 3
    task3 = tm.add_task(
        "ทดสอบระบบ",
        "ทำการทดสอบระบบ Task Manager อย่างครอบคลุม",
        (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    )
    print(f"✅ เพิ่มงาน: {task3.title}")
    
    # งานที่ 4 (เสร็จแล้ว)
    task4 = tm.add_task(
        "ออกแบบ UI",
        "ออกแบบ User Interface สำหรับ Task Manager",
        (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    )
    task4.mark_completed()
    print(f"✅ เพิ่มงาน: {task4.title} (เสร็จแล้ว)")
    
    # แสดงงานทั้งหมด
    print("\n📋 งานทั้งหมด:")
    tm.display_tasks()
    
    # แสดงงานที่รอดำเนินการ
    print("\n⏳ งานที่รอดำเนินการ:")
    tm.display_tasks(tm.get_pending_tasks())
    
    # แสดงงานที่เสร็จสิ้นแล้ว
    print("\n✅ งานที่เสร็จสิ้นแล้ว:")
    tm.display_tasks(tm.get_completed_tasks())
    
    # ทดสอบการค้นหา
    print("\n🔍 ค้นหางานที่มีคำว่า 'ระบบ':")
    search_results = tm.search_tasks(keyword="ระบบ")
    tm.display_tasks(search_results)
    
    # ทดสอบการทำเครื่องหมายเสร็จสิ้น
    print(f"\n✅ ทำเครื่องหมายว่างาน '{task1.title}' เสร็จสิ้น:")
    tm.mark_task_completed(task1.task_id)
    
    # แสดงสถานะหลังการอัปเดต
    print("\n📊 สถานะหลังการอัปเดต:")
    print(f"งานทั้งหมด: {len(tm.get_all_tasks())}")
    print(f"งานที่รอดำเนินการ: {len(tm.get_pending_tasks())}")
    print(f"งานที่เสร็จสิ้นแล้ว: {len(tm.get_completed_tasks())}")
    
    # ทดสอบการลบงาน
    print(f"\n🗑️ ลบงาน '{task3.title}':")
    tm.delete_task(task3.task_id)
    
    # แสดงสถานะสุดท้าย
    print("\n📊 สถานะสุดท้าย:")
    print(f"งานทั้งหมด: {len(tm.get_all_tasks())}")
    print(f"งานที่รอดำเนินการ: {len(tm.get_pending_tasks())}")
    print(f"งานที่เสร็จสิ้นแล้ว: {len(tm.get_completed_tasks())}")
    
    print("\n🎉 Demo เสร็จสิ้น! ข้อมูลถูกบันทึกใน demo_tasks.json")


if __name__ == "__main__":
    demo_task_manager()
