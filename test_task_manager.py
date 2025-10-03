"""
Test file for Task Manager Application
ไฟล์ทดสอบสำหรับ Task Manager
"""

import unittest
import tempfile
import os
from datetime import datetime
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    """Test cases for Task class"""
    
    def test_task_creation(self):
        """Test basic task creation"""
        task = Task("Test Task", "Test Description", "2024-01-15")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.due_date, "2024-01-15")
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.task_id)
        self.assertTrue(task.task_id.startswith("TASK_"))
    
    def test_task_mark_completed(self):
        """Test marking task as completed"""
        task = Task("Test Task", "Test Description", "2024-01-15")
        self.assertFalse(task.completed)
        
        task.mark_completed()
        self.assertTrue(task.completed)
    
    def test_task_to_dict(self):
        """Test task serialization to dictionary"""
        task = Task("Test Task", "Test Description", "2024-01-15")
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['description'], "Test Description")
        self.assertEqual(task_dict['due_date'], "2024-01-15")
        self.assertFalse(task_dict['completed'])
        self.assertIn('task_id', task_dict)
        self.assertIn('created_at', task_dict)
        self.assertIn('updated_at', task_dict)
    
    def test_task_from_dict(self):
        """Test task creation from dictionary"""
        task_data = {
            'task_id': 'TASK_123',
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': '2024-01-15',
            'completed': True,
            'created_at': '2024-01-15T10:00:00',
            'updated_at': '2024-01-15T10:00:00'
        }
        
        task = Task.from_dict(task_data)
        
        self.assertEqual(task.task_id, 'TASK_123')
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.due_date, '2024-01-15')
        self.assertTrue(task.completed)


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.task_manager = TaskManager(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a new task"""
        task = self.task_manager.add_task("Test Task", "Test Description", "2024-01-15")
        
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(len(self.task_manager.tasks), 1)
    
    def test_add_task_invalid_data(self):
        """Test adding task with invalid data"""
        with self.assertRaises(ValueError):
            self.task_manager.add_task("", "Test Description", "2024-01-15")
        
        with self.assertRaises(ValueError):
            self.task_manager.add_task("Test Task", "Test Description", "invalid-date")
    
    def test_get_task_by_id(self):
        """Test getting task by ID"""
        task = self.task_manager.add_task("Test Task", "Test Description", "2024-01-15")
        task_id = task.task_id
        
        found_task = self.task_manager.get_task_by_id(task_id)
        self.assertEqual(found_task, task)
        
        not_found = self.task_manager.get_task_by_id("NONEXISTENT")
        self.assertIsNone(not_found)
    
    def test_mark_task_completed(self):
        """Test marking task as completed"""
        task = self.task_manager.add_task("Test Task", "Test Description", "2024-01-15")
        task_id = task.task_id
        
        result = self.task_manager.mark_task_completed(task_id)
        self.assertTrue(result)
        self.assertTrue(task.completed)
        
        result = self.task_manager.mark_task_completed("NONEXISTENT")
        self.assertFalse(result)
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = self.task_manager.add_task("Test Task", "Test Description", "2024-01-15")
        task_id = task.task_id
        
        result = self.task_manager.delete_task(task_id)
        self.assertTrue(result)
        self.assertEqual(len(self.task_manager.tasks), 0)
        
        result = self.task_manager.delete_task("NONEXISTENT")
        self.assertFalse(result)
    
    def test_search_tasks(self):
        """Test searching tasks"""
        self.task_manager.add_task("Python Task", "Learn Python", "2024-01-15")
        self.task_manager.add_task("Java Task", "Learn Java", "2024-01-16")
        self.task_manager.add_task("Python Project", "Build Python app", "2024-01-15")
        
        # Search by keyword
        results = self.task_manager.search_tasks(keyword="Python")
        self.assertEqual(len(results), 2)
        
        # Search by date
        results = self.task_manager.search_tasks(due_date="2024-01-15")
        self.assertEqual(len(results), 2)
        
        # Search by both keyword and date
        results = self.task_manager.search_tasks(keyword="Python", due_date="2024-01-15")
        self.assertEqual(len(results), 2)
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks"""
        # Add some tasks
        self.task_manager.add_task("Task 1", "Description 1", "2024-01-15")
        self.task_manager.add_task("Task 2", "Description 2", "2024-01-16")
        
        # Create new task manager and load tasks
        new_task_manager = TaskManager(self.temp_file.name)
        
        self.assertEqual(len(new_task_manager.tasks), 2)
        self.assertEqual(new_task_manager.tasks[0].title, "Task 1")
        self.assertEqual(new_task_manager.tasks[1].title, "Task 2")


if __name__ == '__main__':
    unittest.main()
