-- ========== USUARIOS ==========
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(100) UNIQUE NOT NULL,
    email NVARCHAR(255) UNIQUE NOT NULL,
    password_hash NVARCHAR(255) NOT NULL,
    first_name NVARCHAR(100),
    last_name NVARCHAR(100),
    role NVARCHAR(50) DEFAULT 'user',
    is_active BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    last_login DATETIME
);

-- ========== POLÍGONOS ==========
CREATE TABLE polygons (
    id INT PRIMARY KEY IDENTITY(1,1),
    geopackage_id INT NULL,
    name NVARCHAR(255) NOT NULL,
    created_by INT NOT NULL,
    source_type NVARCHAR(50),
    geom_wkt NVARCHAR(MAX),
    bbox NVARCHAR(MAX),
    area_sqm FLOAT,
    properties NVARCHAR(MAX),
    is_validated BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (created_by) REFERENCES users(id)
);

-- ========== VALIDACIONES ==========
CREATE TABLE validations (
    id INT PRIMARY KEY IDENTITY(1,1),
    polygon_id INT NOT NULL,
    validator_id INT NOT NULL,
    status NVARCHAR(50),
    validation_type NVARCHAR(100),
    score FLOAT,
    notes NVARCHAR(MAX),
    metadata NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (polygon_id) REFERENCES polygons(id),
    FOREIGN KEY (validator_id) REFERENCES users(id)
);

-- ========== ANOTACIONES ==========
CREATE TABLE annotations (
    id INT PRIMARY KEY IDENTITY(1,1),
    polygon_id INT NOT NULL,
    author_id INT NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    annotation_type NVARCHAR(50),
    location NVARCHAR(MAX),
    is_resolved BIT DEFAULT 0,
    resolved_by INT,
    resolved_at DATETIME,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (polygon_id) REFERENCES polygons(id),
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (resolved_by) REFERENCES users(id)
);

-- ========== REPLIES A ANOTACIONES ==========
CREATE TABLE annotation_replies (
    id INT PRIMARY KEY IDENTITY(1,1),
    annotation_id INT NOT NULL,
    author_id INT NOT NULL,
    content NVARCHAR(MAX) NOT NULL,
    created_at DATETIME DEFAULT GETUTCDATE(),
    updated_at DATETIME DEFAULT GETUTCDATE(),
    FOREIGN KEY (annotation_id) REFERENCES annotations(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- ========== AUDITORÍA ==========
CREATE TABLE audit_logs (
    id INT PRIMARY KEY IDENTITY(1,1),
    entity_type NVARCHAR(100),
    entity_id INT,
    action NVARCHAR(50),
    user_id INT,
    changes NVARCHAR(MAX),
    old_values NVARCHAR(MAX),
    new_values NVARCHAR(MAX),
    created_at DATETIME DEFAULT GETUTCDATE()
);

-- ========== ÍNDICES ==========
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_polygons_created_by ON polygons(created_by);
CREATE INDEX idx_polygons_source_type ON polygons(source_type);
CREATE INDEX idx_validations_polygon ON validations(polygon_id);
CREATE INDEX idx_validations_validator ON validations(validator_id);
CREATE INDEX idx_annotations_polygon ON annotations(polygon_id);
CREATE INDEX idx_annotations_author ON annotations(author_id);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- ========== DATOS INICIALES (EJEMPLO) ==========
-- Insertar usuario admin
INSERT INTO users (username, email, password_hash, first_name, last_name, role)
VALUES ('admin', 'admin@example.com', '\\\', 'Admin', 'User', 'admin');
