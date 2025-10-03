#!/usr/bin/env python3
"""
Python Task Manager - Main Entry Point
ระบบจัดการงานประจำวันด้วย Python

Author: Python Task Manager Team
Version: 1.0.0
"""

import sys
import os
from cli import TaskManagerCLI


def check_python_version():
    """
    ตรวจสอบเวอร์ชัน Python
    """
    if sys.version_info < (3, 6):
        print("❌ ข้อผิดพลาด: ต้องการ Python 3.6 หรือสูงกว่า")
        print(f"   เวอร์ชันปัจจุบัน: {sys.version}")
        sys.exit(1)


def display_welcome():
    """
    แสดงข้อความต้อนรับ
    """
    print("="*60)
    print("🎯 Python Task Manager")
    print("   ระบบจัดการงานประจำวันที่ใช้งานง่าย")
    print("="*60)
    print("📝 ฟีเจอร์หลัก:")
    print("   • เพิ่มงานใหม่พร้อมคำอธิบายและวันที่ครบกำหนด")
    print("   • ดูงานทั้งหมดแยกตามสถานะ")
    print("   • ทำเครื่องหมายว่างานเสร็จสิ้น")
    print("   • ลบงานที่ไม่ต้องการ")
    print("   • ค้นหางานตามคำสำคัญหรือวันที่")
    print("   • บันทึกและโหลดข้อมูลอัตโนมัติ")
    print("   • แสดงสถิติการทำงาน")
    print("="*60)


def main():
    """
    ฟังก์ชันหลักของโปรแกรม
    """
    try:
        # ตรวจสอบเวอร์ชัน Python
        check_python_version()
        
        # แสดงข้อความต้อนรับ
        display_welcome()
        
        # เริ่มต้น CLI
        cli = TaskManagerCLI()
        cli.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 ขอบคุณที่ใช้ Python Task Manager!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        print("กรุณาติดต่อผู้ดูแลระบบ")
        sys.exit(1)


if __name__ == "__main__":
    main()
