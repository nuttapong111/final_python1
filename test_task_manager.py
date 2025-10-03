"""
Unit Tests for Python Task Manager
การทดสอบหน่วยสำหรับระบบจัดการงาน
"""

import unittest
import os
import tempfile
from datetime import datetime
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """ทดสอบ Task class"""
    
    def setUp(self):
        """ตั้งค่าสำหรับการทดสอบ"""
        self.task = Task("TASK001", "Test Task", "Test Description", "2024-12-31")
    
    def test_task_creation(self):
        """ทดสอบการสร้างงาน"""
        self.assertEqual(self.task.task_id, "TASK001")
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.due_date, "2024-12-31")
        self.assertFalse(self.task.completed)
    
    def test_mark_completed(self):
        """ทดสอบการทำเครื่องหมายเสร็จสิ้น"""
        self.assertFalse(self.task.completed)
        self.task.mark_completed()
        self.assertTrue(self.task.completed)
    
    def test_to_dict(self):
        """ทดสอบการแปลงเป็น dictionary"""
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict['task_id'], "TASK001")
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['completed'], False)
    
    def test_from_dict(self):
        """ทดสอบการสร้างจาก dictionary"""
        task_data = {
            'task_id': 'TASK002',
            'title': 'Another Task',
            'description': 'Another Description',
            'due_date': '2024-12-25',
            'completed': True,
            'created_at': '2024-01-01 10:00:00'
        }
        task = Task.from_dict(task_data)
        self.assertEqual(task.task_id, "TASK002")
        self.assertEqual(task.title, "Another Task")
        self.assertTrue(task.completed)


class TestTaskManager(unittest.TestCase):
    """ทดสอบ TaskManager class"""
    
    def setUp(self):
        """ตั้งค่าสำหรับการทดสอบ"""
        # สร้างไฟล์ชั่วคราวสำหรับการทดสอบ
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_manager = TaskManager(self.temp_file.name)
    
    def tearDown(self):
        """ทำความสะอาดหลังการทดสอบ"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_generate_task_id(self):
        """ทดสอบการสร้างรหัสงาน"""
        # เริ่มต้นไม่มีงาน
        task_id = self.task_manager.generate_task_id()
        self.assertEqual(task_id, "TASK001")
        
        # เพิ่มงานหนึ่งงาน
        self.task_manager.add_task("Test Task", "Test Description", "2024-12-31")
        task_id = self.task_manager.generate_task_id()
        self.assertEqual(task_id, "TASK002")
    
    def test_add_task_valid(self):
        """ทดสอบการเพิ่มงานที่ถูกต้อง"""
        result = self.task_manager.add_task("Test Task", "Test Description", "2024-12-31")
        self.assertTrue(result)
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, "Test Task")
    
    def test_add_task_invalid_title(self):
        """ทดสอบการเพิ่มงานด้วยชื่องานว่าง"""
        result = self.task_manager.add_task("", "Test Description", "2024-12-31")
        self.assertFalse(result)
        self.assertEqual(len(self.task_manager.tasks), 0)
    
    def test_add_task_invalid_date(self):
        """ทดสอบการเพิ่มงานด้วยวันที่ไม่ถูกต้อง"""
        result = self.task_manager.add_task("Test Task", "Test Description", "invalid-date")
        self.assertFalse(result)
        self.assertEqual(len(self.task_manager.tasks), 0)
    
    def test_mark_task_completed(self):
        """ทดสอบการทำเครื่องหมายเสร็จสิ้น"""
        self.task_manager.add_task("Test Task", "Test Description", "2024-12-31")
        task_id = self.task_manager.tasks[0].task_id
        
        result = self.task_manager.mark_task_completed(task_id)
        self.assertTrue(result)
        self.assertTrue(self.task_manager.tasks[0].completed)
    
    def test_mark_task_completed_invalid_id(self):
        """ทดสอบการทำเครื่องหมายเสร็จสิ้นด้วยรหัสที่ไม่ถูกต้อง"""
        result = self.task_manager.mark_task_completed("INVALID_ID")
        self.assertFalse(result)
    
    def test_delete_task(self):
        """ทดสอบการลบงาน"""
        self.task_manager.add_task("Test Task", "Test Description", "2024-12-31")
        task_id = self.task_manager.tasks[0].task_id
        
        result = self.task_manager.delete_task(task_id)
        self.assertTrue(result)
        self.assertEqual(len(self.task_manager.tasks), 0)
    
    def test_delete_task_invalid_id(self):
        """ทดสอบการลบงานด้วยรหัสที่ไม่ถูกต้อง"""
        result = self.task_manager.delete_task("INVALID_ID")
        self.assertFalse(result)
    
    def test_search_tasks_by_keyword(self):
        """ทดสอบการค้นหางานตามคำสำคัญ"""
        self.task_manager.add_task("Python Task", "Learn Python", "2024-12-31")
        self.task_manager.add_task("Java Task", "Learn Java", "2024-12-25")
        
        results = self.task_manager.search_tasks(keyword="Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Task")
    
    def test_search_tasks_by_date(self):
        """ทดสอบการค้นหางานตามวันที่"""
        self.task_manager.add_task("Task 1", "Description 1", "2024-12-31")
        self.task_manager.add_task("Task 2", "Description 2", "2024-12-25")
        
        results = self.task_manager.search_tasks(due_date="2024-12-31")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 1")
    
    def test_get_statistics(self):
        """ทดสอบการรับสถิติ"""
        # ไม่มีงาน
        stats = self.task_manager.get_statistics()
        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['completed'], 0)
        self.assertEqual(stats['pending'], 0)
        
        # เพิ่มงานที่เสร็จสิ้น
        self.task_manager.add_task("Task 1", "Description 1", "2024-12-31")
        self.task_manager.tasks[0].mark_completed()
        
        # เพิ่มงานที่รอดำเนินการ
        self.task_manager.add_task("Task 2", "Description 2", "2024-12-25")
        
        stats = self.task_manager.get_statistics()
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['completed'], 1)
        self.assertEqual(stats['pending'], 1)
        self.assertEqual(stats['completion_rate'], 50.0)
    
    def test_save_and_load_tasks(self):
        """ทดสอบการบันทึกและโหลดงาน"""
        # เพิ่มงาน
        self.task_manager.add_task("Task 1", "Description 1", "2024-12-31")
        self.task_manager.tasks[0].mark_completed()
        self.task_manager.add_task("Task 2", "Description 2", "2024-12-25")
        
        # สร้าง TaskManager ใหม่และโหลดข้อมูล
        new_task_manager = TaskManager(self.temp_file.name)
        
        self.assertEqual(len(new_task_manager.tasks), 2)
        self.assertTrue(new_task_manager.tasks[0].completed)
        self.assertFalse(new_task_manager.tasks[1].completed)


if __name__ == '__main__':
    # รันการทดสอบ
    unittest.main(verbosity=2)
