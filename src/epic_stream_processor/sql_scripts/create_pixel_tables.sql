-- CREATE extension postgis;

-- CREATE TYPE lm_coord AS(l_coord float, m_coord float);

-- CREATE TYPE img_dim AS (x int, y int);

CREATE TABLE IF NOT EXISTS epic_pixels (
	id uuid NOT NULL,
	pixel_values FLOAT [] NOT NULL,
	pixel_coord POINT NOT NULL,
	pixel_lm POINT,
	source_names TEXT NOT NULL
);

SELECT
	AddGeometryColumn(
		'public',
		'epic_pixels',
		'pixel_skypos',
		4326,
		'POINT',
		2
	);

CREATE TABLE IF NOT EXISTS epic_img_metadata(
	id uuid PRIMARY KEY,
	img_time TIMESTAMP,
	n_chan INT,
	n_pol INT,
	chan0 FLOAT,
	chan_bw FLOAT,
	epic_version TEXT,
	img_size POINT DEFAULT '(64, 64)'
);

CREATE TABLE IF NOT EXISTS epic_watchdog(
	id SERIAL NOT NULL,
	source TEXT NOT NULL,
	event_time TIMESTAMP NOT NULL,
	ra_deg FLOAT NOT NULL,
	dec_deg FLOAT NOT NULL,
	event_type TEXT NOT NULL,
	t_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	t_end TIMESTAMP, --UTC
	watch_mode TEXT DEFAULT 'continuous',
	patch_type INT DEFAULT 5,
	reason TEXT NOT NULL,
	author TEXT NOT NULL,
	watch_status TEXT DEFAULT 'watching',
	voevent XML
);

CREATE TABLE IF NOT EXISTS epic_files_metadata(
	id SERIAL NOT NULL,
	file_name TEXT NOT NULL,
	chan_width FLOAT NOT NULL,
	nchan INT NOT NULL,
	support_size INT NOT NULL,
	gulp_len_ms FLOAT NOT NULL,
	image_len_ms FLOAT NOT NULL,
	epoch_time_s FLOAT NOT NULL,
	grid_size INT NOT NULL,
	grid_res FLOAT NOT NULL,
	cfreq_mhz FLOAT NOT NULL,
	epic_version TEXT NOT NULL
);

-- SELECT
-- 	AddGeometryColumn(
-- 		'public',
-- 		'epic_watchdog',
-- 		'event_skypos',
-- 		4326,
-- 		'POINT',
-- 		2
-- 	);
