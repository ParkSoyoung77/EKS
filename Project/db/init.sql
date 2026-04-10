CREATE TABLE board_table (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '고유 번호',
    list_num INT NOT NULL DEFAULT 1 COMMENT '1: 게시판, 2: 방명록',
    author_name VARCHAR(50) NOT NULL COMMENT '작성자 이름',
    password VARCHAR(255) COMMENT '게시글 비밀번호(방명록은 선택 가능)', -- NOT NULL 제거
    title VARCHAR(200) COMMENT '글 제목(게시판 전용)',                -- NOT NULL 제거
    content TEXT NOT NULL COMMENT '글 본문',
    view_count INT DEFAULT 0 COMMENT '조회수',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '작성일'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;