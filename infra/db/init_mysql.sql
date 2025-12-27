CREATE DATABASE IF NOT EXISTS roadsense;
USE roadsense;

CREATE TABLE IF NOT EXISTS videos (
    id CHAR(36) PRIMARY KEY,
    filename TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_type TEXT,
    duration_seconds NUMERIC
);

CREATE TABLE IF NOT EXISTS frames (
    id CHAR(36) PRIMARY KEY,
    video_id CHAR(36),
    frame_index INT,
    timestamp_ms BIGINT,
    image_path TEXT,
    gps_lat DOUBLE,
    gps_lon DOUBLE,
    gps_alt DOUBLE,
    imu_yaw DOUBLE,
    imu_pitch DOUBLE,
    imu_roll DOUBLE,
    FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detections (
    id CHAR(36) PRIMARY KEY,
    frame_id CHAR(36),
    model_name TEXT,
    class_label TEXT,
    confidence NUMERIC,
    bbox_xmin NUMERIC,
    bbox_ymin NUMERIC,
    bbox_xmax NUMERIC,
    bbox_ymax NUMERIC,
    mask_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (frame_id) REFERENCES frames(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS road_segments (
    id CHAR(36) PRIMARY KEY,
    osm_id BIGINT,
    name TEXT,
    importance TEXT,
    geom TEXT -- Storing as WKT or similar for simplicity if needed, or just unused
);

CREATE TABLE IF NOT EXISTS defects (
    id CHAR(36) PRIMARY KEY,
    detection_id CHAR(36),
    segment_id CHAR(36),
    location_lat DOUBLE,
    location_lon DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (detection_id) REFERENCES detections(id) ON DELETE CASCADE,
    FOREIGN KEY (segment_id) REFERENCES road_segments(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS severity_scores (
    id CHAR(36) PRIMARY KEY,
    defect_id CHAR(36),
    severity_score NUMERIC,
    severity_class TEXT,
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (defect_id) REFERENCES defects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS damages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_id TEXT NOT NULL,
    score FLOAT,
    priorite TEXT,
    damage_type TEXT,
    confidence FLOAT,
    severity INT,
    priority TEXT,
    latitude DOUBLE,
    longitude DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
