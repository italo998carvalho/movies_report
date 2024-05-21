CREATE TABLE tmdb_movie (
  tmdb_id INT PRIMARY KEY UNIQUE,
  report_title VARCHAR NOT NULL UNIQUE,
  tmdb_title VARCHAR,
  budget NUMERIC(12,2),
  release_date_streaming DATE,
  release_date_theater DATE,
  revenue NUMERIC(12,2)
);

CREATE TABLE imdb_movie (
  tmdb_id INT NOT NULL,
  imdb_id VARCHAR NOT NULL UNIQUE,
  imdb_title VARCHAR,
  rating FLOAT,
  budget NUMERIC(12,2),
  gross_worldwide NUMERIC(12,2),
  gross_us_canada NUMERIC(12,2),
  openning_week_us_canada NUMERIC(12,2),
  CONSTRAINT fk_tmdb_id
      FOREIGN KEY(tmdb_id)
      REFERENCES tmdb_movie(tmdb_id)
);

CREATE TABLE rt_movie (
  tmdb_id INT NOT NULL,
  tomatometer FLOAT,
  audience_score FLOAT,
  CONSTRAINT fk_tmdb_id
      FOREIGN KEY(tmdb_id)
      REFERENCES tmdb_movie(tmdb_id)
);

ALTER TABLE imdb_movie ALTER COLUMN budget TYPE VARCHAR;
ALTER TABLE imdb_movie ALTER COLUMN gross_worldwide TYPE VARCHAR;
ALTER TABLE imdb_movie ALTER COLUMN gross_us_canada TYPE VARCHAR;
ALTER TABLE imdb_movie ALTER COLUMN openning_week_us_canada TYPE VARCHAR;