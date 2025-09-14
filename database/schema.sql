-- Defines the cultural and historical context
CREATE TABLE Provenances (
    ProvenanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    TimePeriod TEXT,
    GeographicArea TEXT
);

-- Stores details for each author
CREATE TABLE Authors (
    AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
    FullName TEXT NOT NULL,
    KnownAs TEXT,
    ProvenanceID INTEGER,
    FOREIGN KEY (ProvenanceID) REFERENCES Provenances(ProvenanceID)
);

-- The main catalog for literary texts
CREATE TABLE Works (
    WorkID INTEGER PRIMARY KEY AUTOINCREMENT,
    OriginalTitle TEXT NOT NULL,
    EnglishTitle TEXT,
    AuthorID INTEGER,
    ProvenanceID INTEGER,
    Language TEXT,
    Content_Translation TEXT,
    FOREIGN KEY (AuthorID) REFERENCES Authors(AuthorID),
    FOREIGN KEY (ProvenanceID) REFERENCES Provenances(ProvenanceID)
);

-- Catalogs images and the objects they depict
CREATE TABLE Artifacts (
    ArtifactID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    ObjectType TEXT,
    ProvenanceID INTEGER,
    CreationDate TEXT,
    CurrentLocation TEXT,
    ImageFilePath TEXT NOT NULL,
    Description TEXT,
    FOREIGN KEY (ProvenanceID) REFERENCES Provenances(ProvenanceID)
);

-- The linking hub that creates connections
CREATE TABLE Cross_References (
    ReferenceID INTEGER PRIMARY KEY AUTOINCREMENT,
    WorkID INTEGER,
    ArtifactID INTEGER,
    Citation TEXT,
    Notes TEXT,
    FOREIGN KEY (WorkID) REFERENCES Works(WorkID),
    FOREIGN KEY (ArtifactID) REFERENCES Artifacts(ArtifactID)
);