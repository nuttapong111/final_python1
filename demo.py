#!/usr/bin/env python3
"""
Python Task Manager - Demo Script
สคริปต์สาธิตการใช้งานระบบจัดการงาน
"""

from task_manager import TaskManager
from datetime import datetime, timedelta


def demo_task_manager():
    """
    สาธิตการใช้งาน TaskManager
    """
    print("🎯 Python Task Manager - Demo")
    print("=" * 50)
    
    # สร้าง TaskManager
    task_manager = TaskManager("demo_tasks.json")
    
    # เพิ่มงานตัวอย่าง
    print("\n📝 เพิ่มงานตัวอย่าง...")
    task_manager.add_task(
        "เรียน Python Programming",
        "เรียน Python สำหรับการพัฒนาแอปพลิเคชัน",
        "2024-12-31"
    )
    
    task_manager.add_task(
        "ทำโปรเจกต์ Task Manager",
        "พัฒนาโปรเจกต์สุดท้ายสำหรับวิชา Programming",
        "2024-12-25"
    )
    
    task_manager.add_task(
        "เตรียมสอบ Final",
        "ทบทวนเนื้อหาสำหรับการสอบปลายภาค",
        "2024-12-20"
    )
    
    # แสดงงานทั้งหมด
    print("\n👀 ดูงานทั้งหมด:")
    task_manager.view_tasks()
    
    # ทำเครื่องหมายว่างานเสร็จสิ้น
    print("\n✅ ทำเครื่องหมายว่างานเสร็จสิ้น...")
    if task_manager.tasks:
        first_task_id = task_manager.tasks[0].task_id
        task_manager.mark_task_completed(first_task_id)
    
    # แสดงงานหลังจากทำเครื่องหมายเสร็จสิ้น
    print("\n👀 ดูงานหลังจากทำเครื่องหมายเสร็จสิ้น:")
    task_manager.view_tasks()
    
    # ค้นหางาน
    print("\n🔍 ค้นหางานที่มีคำว่า 'Python':")
    results = task_manager.search_tasks(keyword="Python")
    task_manager.display_search_results(results)
    
    # แสดงสถิติ
    print("\n📊 สถิติงาน:")
    stats = task_manager.get_statistics()
    print(f"   งานทั้งหมด: {stats['total']} งาน")
    print(f"   งานที่เสร็จสิ้น: {stats['completed']} งาน")
    print(f"   งานที่รอดำเนินการ: {stats['pending']} งาน")
    print(f"   อัตราการเสร็จสิ้น: {stats['completion_rate']:.1f}%")
    
    print("\n✅ Demo เสร็จสิ้น!")


def demo_advanced_features():
    """
    สาธิตฟีเจอร์ขั้นสูง
    """
    print("\n🚀 Advanced Features Demo")
    print("=" * 50)
    
    task_manager = TaskManager("demo_advanced.json")
    
    # เพิ่มงานหลายงาน
    tasks_data = [
        ("ประชุมทีม", "ประชุมทีมพัฒนาโปรเจกต์", "2024-12-15"),
        ("เขียนเอกสาร", "เขียนเอกสารโปรเจกต์", "2024-12-18"),
        ("ทดสอบระบบ", "ทดสอบระบบก่อนส่ง", "2024-12-22"),
        ("ส่งโปรเจกต์", "ส่งโปรเจกต์ให้อาจารย์", "2024-12-25"),
        ("พักผ่อน", "พักผ่อนหลังส่งงาน", "2024-12-26")
    ]
    
    print("\n📝 เพิ่มงานหลายงาน...")
    for title, description, due_date in tasks_data:
        task_manager.add_task(title, description, due_date)
    
    # แสดงงานทั้งหมด
    print("\n👀 งานทั้งหมด:")
    task_manager.view_tasks()
    
    # ค้นหาตามวันที่
    print("\n🔍 ค้นหางานที่ครบกำหนดวันที่ 2024-12-25:")
    results = task_manager.search_tasks(due_date="2024-12-25")
    task_manager.display_search_results(results)
    
    # ค้นหาตามคำสำคัญ
    print("\n🔍 ค้นหางานที่มีคำว่า 'โปรเจกต์':")
    results = task_manager.search_tasks(keyword="โปรเจกต์")
    task_manager.display_search_results(results)
    
    # ทำเครื่องหมายว่างานเสร็จสิ้นหลายงาน
    print("\n✅ ทำเครื่องหมายว่างานเสร็จสิ้น...")
    for i, task in enumerate(task_manager.tasks[:3]):  # ทำเครื่องหมาย 3 งานแรก
        task_manager.mark_task_completed(task.task_id)
    
    # แสดงสถิติสุดท้าย
    print("\n📊 สถิติสุดท้าย:")
    stats = task_manager.get_statistics()
    print(f"   งานทั้งหมด: {stats['total']} งาน")
    print(f"   งานที่เสร็จสิ้น: {stats['completed']} งาน")
    print(f"   งานที่รอดำเนินการ: {stats['pending']} งาน")
    print(f"   อัตราการเสร็จสิ้น: {stats['completion_rate']:.1f}%")
    
    print("\n✅ Advanced Demo เสร็จสิ้น!")


if __name__ == "__main__":
    try:
        # รัน demo พื้นฐาน
        demo_task_manager()
        
        # รัน demo ขั้นสูง
        demo_advanced_features()
        
        print("\n🎉 การสาธิตทั้งหมดเสร็จสิ้น!")
        print("💡 ใช้ 'python main.py' เพื่อเริ่มต้นโปรแกรมจริง")
        
    except KeyboardInterrupt:
        print("\n\n👋 ยกเลิกการสาธิต")
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดในการสาธิต: {e}")
