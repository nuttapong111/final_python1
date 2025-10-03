# GitHub Setup Instructions

คำแนะนำการตั้งค่า GitHub Repository สำหรับ Python Task Manager

## 🚀 การตั้งค่า GitHub Repository

### 1. สร้าง Repository บน GitHub

1. ไปที่ [GitHub.com](https://github.com) และเข้าสู่ระบบ
2. คลิก "New repository" หรือ "+" ด้านบนขวา
3. ตั้งชื่อ repository: `python-task-manager`
4. เลือก "Public" เพื่อให้ทุกคนเข้าถึงได้
5. **อย่า** เลือก "Add a README file" (เรามีอยู่แล้ว)
6. **อย่า** เลือก "Add .gitignore" (เรามีอยู่แล้ว)
7. คลิก "Create repository"

### 2. เชื่อมต่อ Local Repository กับ GitHub

```bash
# เพิ่ม remote origin
git remote add origin https://github.com/YOUR_USERNAME/python-task-manager.git

# ตั้งค่า branch หลัก
git branch -M main

# Push ไปยัง GitHub
git push -u origin main
```

### 3. ตรวจสอบการตั้งค่า

```bash
# ตรวจสอบ remote
git remote -v

# ตรวจสอบ status
git status

# ดู log
git log --oneline
```

## 📋 การสร้าง Pull Request

### 1. สร้าง Feature Branch ใหม่

```bash
# สร้าง branch ใหม่สำหรับ feature
git checkout -b feature/improve-ui

# ทำการเปลี่ยนแปลง (ตัวอย่าง)
# แก้ไขไฟล์ main.py เพื่อปรับปรุง UI

# Add และ commit การเปลี่ยนแปลง
git add .
git commit -m "Improve CLI user interface

- Add better formatting for task display
- Improve menu layout and readability
- Add color coding for task status
- Enhance user experience with better prompts"
```

### 2. Push Branch ไปยัง GitHub

```bash
git push origin feature/improve-ui
```

### 3. สร้าง Pull Request

1. ไปที่ GitHub repository
2. คลิก "Compare & pull request" ที่ปรากฏขึ้น
3. ตั้งชื่อ PR: "Improve CLI user interface"
4. เขียนคำอธิบาย:
   ```
   ## Changes
   - Enhanced CLI user interface with better formatting
   - Added color coding for task status indicators
   - Improved menu layout and readability
   - Better user prompts and error messages
   
   ## Testing
   - [x] Tested all menu options
   - [x] Verified task display formatting
   - [x] Confirmed error handling works correctly
   
   ## Screenshots
   (ถ้ามี)
   ```
5. คลิก "Create pull request"

### 4. Merge Pull Request

1. ตรวจสอบ PR และทดสอบ
2. คลิก "Merge pull request"
3. คลิก "Confirm merge"
4. ลบ feature branch (optional)

## 🔧 การจัดการ Repository

### การอัปเดต README

```bash
# แก้ไข README.md
# Add และ commit
git add README.md
git commit -m "Update README with new features and examples"

# Push การเปลี่ยนแปลง
git push origin main
```

### การเพิ่ม Tags สำหรับ Releases

```bash
# สร้าง tag สำหรับ version
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag ไปยัง GitHub
git push origin v1.0.0
```

### การสร้าง Issues

1. ไปที่ GitHub repository
2. คลิก "Issues" tab
3. คลิก "New issue"
4. ตั้งชื่อและอธิบายปัญหา
5. ใช้ labels เพื่อจัดหมวดหมู่

## 📊 การติดตาม Progress

### GitHub Insights

1. ไปที่ "Insights" tab ใน repository
2. ดู "Contributors" เพื่อดูการมีส่วนร่วม
3. ดู "Traffic" เพื่อดูการเข้าชม
4. ดู "Commits" เพื่อดูประวัติการพัฒนา

### การใช้ GitHub Actions (Optional)

สร้างไฟล์ `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest test_task_manager.py -v
```

## 🎯 Best Practices

### Commit Messages

- ใช้ present tense: "Add feature" ไม่ใช่ "Added feature"
- เริ่มต้นด้วย verb: "Fix bug", "Update documentation"
- ใช้ bullet points สำหรับรายละเอียด

### Branch Naming

- `feature/description`: สำหรับ feature ใหม่
- `bugfix/description`: สำหรับแก้ไข bug
- `hotfix/description`: สำหรับแก้ไขด่วน

### Pull Request

- ตั้งชื่อที่ชัดเจน
- เขียนคำอธิบายที่ครบถ้วน
- ใช้ checklist สำหรับการทดสอบ
- ใส่ screenshots ถ้าจำเป็น

## 🔗 Links ที่มีประโยชน์

- [GitHub Documentation](https://docs.github.com/)
- [Git Best Practices](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Python Project Structure](https://docs.python-guide.org/writing/structure/)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
