BEGIN TRANSACTION; 
-- Dette scriptet vil legge inn Nordlandsbanen, med tilhoerende stasjoner og delstrekninger

-- Insert togstasjoner
INSERT INTO Togstasjon VALUES("Bodoe", 4.1); 
INSERT INTO Togstasjon VALUES("Fauske", 34); 
INSERT INTO Togstasjon VALUES("Mo i Rana", 3.5); 
INSERT INTO Togstasjon VALUES("Mosjoeen", 6.8); 
INSERT INTO Togstasjon VALUES("Steinkjer", 3.6); 
INSERT INTO Togstasjon VALUES("Trondheim", 5.1); 

-- Insert banestrekninger 
INSERT INTO Banestrekning VALUES("Nordlandsbanen", "Diesel", "Trondheim", "Bodoe"); 

-- Insert delstrekninger 
INSERT INTO Delstrekning VALUES("Trondheim-Steinkjer", 120, 2, "Nordlandsbanen", NULL, "Trondheim", "Steinkjer"); 
INSERT INTO Delstrekning VALUES("Steinkjer-Trondheim", 120, 2, NULL, "Nordlandsbanen", "Steinkjer", "Trondheim"); 
INSERT INTO Delstrekning VALUES("Steinkjer-Mosjoeen", 280, 1, "Nordlandsbanen", NULL, "Steinkjer", "Mosjoeen"); 
INSERT INTO Delstrekning VALUES("Mosjoeen-Steinkjer", 280, 1, NULL, "Nordlandsbanen", "Mosjoeen", "Steinkjer"); 
INSERT INTO Delstrekning VALUES("Mosjoeen-Mo i Rana", 90, 1, "Nordlandsbanen", NULL, "Mosjoeen", "Mo i Rana"); 
INSERT INTO Delstrekning VALUES("Mo i Rana-Mosjoeen", 90, 1, NULL, "Nordlandsbanen", "Mo i Rana", "Mosjoeen"); 
INSERT INTO Delstrekning VALUES("Mo i Rana-Fauske", 170, 1, "Nordlandsbanen", NULL, "Mo i Rana", "Fauske"); 
INSERT INTO Delstrekning VALUES("Fauske-Mo i Rana", 170, 1, NULL, "Nordlandsbanen", "Fauske", "Mo i Rana"); 
INSERT INTO Delstrekning VALUES("Fauske-Bodoe", 60, 1, "Nordlandsbanen", NULL, "Fauske", "Bodoe"); 
INSERT INTO Delstrekning VALUES("Bodoe-Fauske", 60, 1, NULL, "Nordlandsbanen", "Bodoe", "Fauske"); 

COMMIT;