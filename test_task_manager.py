#!/usr/bin/env python3
"""
Test script for Python Task Manager
ทดสอบฟังก์ชันการทำงานของ Task Manager
"""

import os
import tempfile
import json
from task_manager import Task, TaskManager


def test_task_creation():
    """ทดสอบการสร้าง Task"""
    print("🧪 Testing Task Creation...")
    
    task = Task("Test Task", "This is a test task", "2024-01-15")
    
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.due_date == "2024-01-15"
    assert task.completed == False
    assert len(task.id) == 8
    
    print("✅ Task creation test passed!")


def test_task_serialization():
    """ทดสอบการแปลง Task เป็น dictionary และกลับ"""
    print("🧪 Testing Task Serialization...")
    
    task = Task("Test Task", "This is a test task", "2024-01-15")
    task_dict = task.to_dict()
    
    # ตรวจสอบว่า dictionary มีข้อมูลครบ
    assert 'id' in task_dict
    assert 'title' in task_dict
    assert 'description' in task_dict
    assert 'due_date' in task_dict
    assert 'completed' in task_dict
    assert 'created_at' in task_dict
    
    # สร้าง Task ใหม่จาก dictionary
    new_task = Task.from_dict(task_dict)
    assert new_task.title == task.title
    assert new_task.description == task.description
    assert new_task.due_date == task.due_date
    assert new_task.completed == task.completed
    assert new_task.id == task.id
    
    print("✅ Task serialization test passed!")


def test_task_manager():
    """ทดสอบ TaskManager"""
    print("🧪 Testing TaskManager...")
    
    # ใช้ไฟล์ชั่วคราวสำหรับทดสอบ
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # สร้าง TaskManager ใหม่
        tm = TaskManager(temp_file)
        
        # ทดสอบการเพิ่มงาน
        assert tm.add_task("Test Task 1", "Description 1", "2024-01-15") == True
        assert tm.add_task("Test Task 2", "Description 2", "2024-01-20") == True
        assert len(tm.tasks) == 2
        
        # ทดสอบการค้นหางาน
        task = tm._find_task_by_id(tm.tasks[0].id)
        assert task is not None
        assert task.title == "Test Task 1"
        
        # ทดสอบการทำเครื่องหมายเสร็จสิ้น
        assert tm.mark_completed(tm.tasks[0].id) == True
        assert tm.tasks[0].completed == True
        
        # ทดสอบการลบงาน
        initial_count = len(tm.tasks)
        assert tm.delete_task(tm.tasks[0].id) == True
        assert len(tm.tasks) == initial_count - 1
        
        # ทดสอบการบันทึกและโหลด
        tm.save_tasks()
        
        # สร้าง TaskManager ใหม่และโหลดข้อมูล
        tm2 = TaskManager(temp_file)
        assert len(tm2.tasks) == 1
        assert tm2.tasks[0].title == "Test Task 2"
        
        print("✅ TaskManager test passed!")
        
    finally:
        # ลบไฟล์ชั่วคราว
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_validation():
    """ทดสอบการตรวจสอบข้อมูล"""
    print("🧪 Testing Input Validation...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        tm = TaskManager(temp_file)
        
        # ทดสอบการเพิ่มงานด้วยชื่อว่าง
        assert tm.add_task("", "Description", "2024-01-15") == False
        
        # ทดสอบการเพิ่มงานด้วยวันที่ไม่ถูกต้อง
        assert tm.add_task("Valid Task", "Description", "invalid-date") == False
        
        # ทดสอบการเพิ่มงานที่ถูกต้อง
        assert tm.add_task("Valid Task", "Description", "2024-01-15") == True
        
        print("✅ Input validation test passed!")
        
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def run_all_tests():
    """รันการทดสอบทั้งหมด"""
    print("🚀 Starting Task Manager Tests...")
    print("=" * 50)
    
    try:
        test_task_creation()
        test_task_serialization()
        test_task_manager()
        test_validation()
        
        print("=" * 50)
        print("🎉 All tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
