
-- LEAFVISION
-- Esquema inicial de la base de datos

CREATE DATABASE IF NOT EXISTS leafvision
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE leafvision;


-- Tabla de usuarios

CREATE TABLE IF NOT EXISTS users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Tabla de identificaciones de plantas

CREATE TABLE IF NOT EXISTS analyses (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    class_id VARCHAR(100) NOT NULL,
    common_name VARCHAR(150) NOT NULL,
    scientific_name VARCHAR(200) NOT NULL,
    confidence DECIMAL(7,6) NOT NULL,
    reference_image VARCHAR(500),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_analyses_user
        FOREIGN KEY (user_id)
        REFERENCES users(id),

    CONSTRAINT chk_confidence
        CHECK (confidence BETWEEN 0 AND 1),

    INDEX idx_analyses_user_date (user_id, created_at)
);
