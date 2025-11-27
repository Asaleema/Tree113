# 🌳 Tree 2D --- Graph Algorithms Visualization

**Interactive Graph Visualization & Classic Algorithms (DFS, BFS,
Dijkstra, Prim, Kruskal)**

โปรเจ็กต์นี้ช่วยให้คุณสามารถสร้างกราฟ 2
มิติและทดลองอัลกอริทึมกราฟพื้นฐานได้อย่างเข้าใจง่าย
พร้อมระบบไฮไลต์ผลลัพธ์บนกราฟแบบสวยงาม

------------------------------------------------------------------------

## ✨ Features

-   🔵 Graph Visualization\
-   🧭 DFS / BFS Spanning Tree\
-   🛣 Dijkstra Shortest Path\
-   🌐 Prim Minimum Spanning Tree\
-   🧩 Kruskal Minimum Spanning Tree\
-   🎛 เมนูใช้งานผ่าน Console\
-   🧱 รองรับ Weighted Graph

------------------------------------------------------------------------

## 📦 Installation

### 1) Clone โปรเจ็กต์

    git clone <your-repo-url>
    cd <your-project-folder>

### 2) ติดตั้ง Dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

## 🚀 Usage

รันโปรแกรม:

    python main.py

ผู้ใช้จะต้องกรอก: - จำนวนโหนด (N)\
- จำนวนเส้นเชื่อม (M)\
- เส้นเชื่อม u v w\
- จุดเริ่มต้น (source)\
- จุดปลายทาง (target)

เมนู:

    1. แสดงกราฟทั้งหมด
    2. DFS Spanning Tree
    3. BFS Spanning Tree
    4. Dijkstra Shortest Path
    5. Prim Minimum Spanning Tree
    6. Kruskal Minimum Spanning Tree
    0. ออกจากโปรแกรม

------------------------------------------------------------------------

## 🗂 Project Structure

    tree2d/
    │── main.py
    │── README.md
    │── requirements.txt

------------------------------------------------------------------------

## 🔍 Algorithms Overview

### 🔹 DFS Spanning Tree

ใช้ค้นหากราฟแบบลึกก่อน

### 🔹 BFS Spanning Tree

ค้นหาแบบกว้างก่อน เหมาะกับหาเส้นทางจำนวน edge น้อยที่สุด

### 🔹 Dijkstra

หาเส้นทางน้ำหนักต่ำสุดจาก source → target

### 🔹 Prim

สร้าง Minimum Spanning Tree โดยเริ่มจากโหนด 1

### 🔹 Kruskal

สร้าง MST ด้วยการเรียง edge + Union-Find

------------------------------------------------------------------------

## 🧪 Example Input

    5
    6
    1 2 4
    1 3 2
    2 4 5
    3 4 1
    3 5 3
    4 5 2
    1
    5

------------------------------------------------------------------------

## 🛠 Technologies

  Library      ใช้สำหรับ
  ------------ ------------------------
  NetworkX     จัดการโครงสร้างกราฟ
  Matplotlib   แสดงผลกราฟ
  PyVis        Interactive graph view
  Heapq        ใช้ใน Dijkstra/Prim
  Deque        BFS

------------------------------------------------------------------------

## 🗺 Roadmap

-   [ ] เพิ่ม GUI\
-   [ ] เพิ่ม visualization แบบ 3D\
-   [ ] Export กราฟเป็นไฟล์

------------------------------------------------------------------------
