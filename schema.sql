-- Inicialização do Banco de Dados SQLite

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'pais',
    is_active BOOLEAN DEFAULT 1
);

-- Usuário Admin Padrão (Senha: admin@123)
-- Hash gerado via bcrypt
INSERT OR IGNORE INTO users (email, hashed_password, full_name, role, is_active)
VALUES (
    'admin@admin.com', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxwKc.6IygDceKmKF.x6uoXq9kyix', 
    'Administrador', 
    'admin', 
    1
);
