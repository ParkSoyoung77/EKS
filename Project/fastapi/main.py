from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pymysql

app = FastAPI()

# 1. 데이터베이스 설정 (VPC-1 RDS Proxy 참조)
DB_CONFIG = {
    'host': '',
    'user': 'admin',
    'password': '',
    'db': 'company',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# --- [ 서비스 페이지 영역 ] ---

# A. 게시판 페이지 (VPC-2 담당)
@app.get("/board", response_class=HTMLResponse)
async def get_board():
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SY의 AWS 게시판</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; text-align: center; background: #f8f9fa; padding: 20px; }
        nav { background: #333; padding: 10px; margin-bottom: 20px; border-radius: 10px; }
        nav a { color: white; margin: 0 15px; text-decoration: none; font-weight: bold; }
        .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; table-layout: fixed; } 
        th, td { border: 1px solid #ddd; padding: 12px; word-wrap: break-word; } 
        th { background: #009639; color: white; }
        .write-box { background: #eee; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: left; }
        .write-box input, .write-box textarea { width: 98%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box; }
        .btn { background: #009639; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%; font-weight: bold; }
    </style>
</head>
<body>
    <nav>
        <a href="/">메인</a>
        <a href="/company">회사소개</a>
        <a href="/board">게시판</a>
        <a href="/guest">방명록</a>
    </nav>
    <div class="container">
        <h1>SY의 실시간 AWS 게시판</h1>
        <div id="board-list">목록 로딩 중...</div>
        <div class="write-box">
            <h3>비회원 글쓰기</h3>
            <input type="text" id="author" placeholder="작성자 이름">
            <input type="password" id="pw" placeholder="비밀번호">
            <input type="text" id="title" placeholder="제목">
            <textarea id="content" rows="4" placeholder="내용을 입력하세요"></textarea>
            <button class="btn" onclick="writePost()">게시글 등록</button>
        </div>
    </div>
    <script>
        function escape(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        function loadList() {
            fetch('/api/list')
                .then(res => res.json())
                .then(data => {
                    if(!data || data.length === 0) {
                        document.getElementById('board-list').innerHTML = "<p>게시글이 없습니다.</p>";
                        return;
                    }
                    let html = '<table><tr><th style="width: 50px;">번호</th><th>제목</th><th style="width: 100px;">작성자</th><th>내용</th><th style="width: 110px;">작성일</th></tr>';
                    data.forEach(item => {
                        html += `<tr>
                            <td>${item.id}</td>
                            <td>${escape(item.title)}</td>
                            <td>${escape(item.author_name)}</td>
                            <td>${escape(item.content)}</td>
                            <td>${item.created_at ? item.created_at.substring(0, 10) : ''}</td>
                        </tr>`;
                    });
                    html += '</table>';
                    document.getElementById('board-list').innerHTML = html;
                });
        }
        function writePost() {
            const payload = {
                author_name: document.getElementById('author').value,
                password: document.getElementById('pw').value,
                title: document.getElementById('title').value,
                content: document.getElementById('content').value,
                list_num: 1
            };
            fetch('/api/write', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(() => {
                alert('등록되었습니다!');
                location.reload();
            });
        }
        loadList();
    </script>
</body>
</html>
    """

# B. 방명록 페이지 (VPC-3 담당)
@app.get("/guestbook", response_class=HTMLResponse)
async def get_guestbook():
    return """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>SY의 AWS 방명록</title>
<style>
    body { font-family: 'Segoe UI', sans-serif; text-align: center; background: #fff5e6; padding: 20px; }
    nav { background: #333; padding: 10px; margin-bottom: 20px; border-radius: 10px; }
    nav a { color: white; margin: 0 15px; text-decoration: none; font-weight: bold; }
    .container { max-width: 700px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .msg-box { background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 15px; text-align: left; }
    .input-area { background: #eee; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: left; }
    input, textarea { width: 98%; margin-bottom: 10px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; box-sizing: border-box; }
    .btn-orange { background: #e67e22; color: white; border: none; padding: 12px; width: 100%; border-radius: 5px; cursor: pointer; font-weight: bold; }
</style>
</head>
<body>
    <nav>
        <a href="/">메인</a> 
        <a href="/company">회사소개</a> 
        <a href="/board">게시판</a> 
        <a href="/guest">방명록</a>
    </nav>
    <div class="container">
        <h1>SY의 실시간 방명록</h1>
        <div id="guest-list">목록 로딩 중...</div>
        <div class="input-area">
            <h3>방명록 남기기</h3>
            <input type="text" id="g-name" placeholder="작성자">
            <textarea id="g-msg" rows="3" placeholder="메시지를 입력하세요"></textarea>
            <button class="btn-orange" onclick="writeGuest()">방명록 등록</button>
        </div>
    </div>
    <script>
        function loadGuest() {
            fetch('/api/guest-list')
                .then(res => res.json())
                .then(data => {
                    let html = '';
                    data.forEach(item => {
                        html += `<div class="msg-box"><strong>${item.author_name}:</strong> ${item.content} <br><small style="color:gray;">${item.created_at}</small></div>`;
                    });
                    document.getElementById('guest-list').innerHTML = html || '<p>방명록이 비어있습니다.</p>';
                });
        }
        function writeGuest() {
            const payload = {
                author_name: document.getElementById('g-name').value,
                password: 'none',
                title: '방명록 메시지',
                content: document.getElementById('g-msg').value,
                list_num: 2
            };
            fetch('/api/write', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            }).then(() => {
                alert('방명록이 등록되었습니다!');
                location.reload();
            });
        }
        loadGuest();
    </script>
</body>
</html>
    """

# --- [ API 데이터 처리 영역 ] ---

# 1. 공통 글쓰기 API (게시판/방명록 공용)
@app.post("/api/write")
async def write_post(request: Request):
    data = await request.json()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO board_table (list_num, author_name, password, title, content) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (data['list_num'], data['author_name'], data['password'], data['title'], data['content']))
            conn.commit()
            return {"status": "success"}
    finally:
        conn.close()

# 2. 게시판 목록 API
@app.get("/api/list")
async def list_posts():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, title, author_name, content, created_at FROM board_table WHERE list_num = 1 ORDER BY id DESC")
            return cursor.fetchall()
    finally:
        conn.close()

# 3. 방명록 목록 API
@app.get("/api/guest-list")
async def list_guests():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT author_name, content, created_at FROM board_table WHERE list_num = 2 ORDER BY id DESC")
            return cursor.fetchall()
    finally:
        conn.close()