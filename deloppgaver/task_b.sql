BEGIN TRANSACTION;
-- Dette scriptet vil legge inn alle togrutene 

-- Insert operatoer 
INSERT INTO Operatoer VALUES("SJ"); 

-- Insert togrute 
INSERT INTO Togrute VALUES(NULL, "Dagtog TRD-BDO", "SJ"); 
INSERT INTO Togrute VALUES(NULL, "Nattog TRD-BDO", "SJ");
INSERT INTO Togrute VALUES(NULL, "Morgentog MIR-TRD", "SJ"); 

-- Insert vogntyper 
INSERT INTO VognType VALUES("SJ-sittevogn-1", "SJ"); 
INSERT INTO VognType VALUES("SJ-sovevogn-1", "SJ"); 

INSERT INTO SoveVogn VALUES("SJ-sovevogn-1", 4, 8); 
INSERT INTO SitteVogn VALUES("SJ-sittevogn-1", 12, 3); 

-- Insert dagtog, Trondheim-Bodoe
INSERT INTO KjoererDelstrekning VALUES(1, "Trondheim-Steinkjer", "07:49", "09:51"); 
INSERT INTO KjoererDelstrekning VALUES(1, "Steinkjer-Mosjoeen", "09:51", "13:20");
INSERT INTO KjoererDelstrekning VALUES(1, "Mosjoeen-Mo i Rana", "13:20", "14:31");  
INSERT INTO KjoererDelstrekning VALUES(1, "Mo i Rana-Fauske", "14:31", "16:49");  
INSERT INTO KjoererDelstrekning VALUES(1, "Fauske-Bodoe", "16:49", "17:34");  

INSERT INTO Dager VALUES(1, "Mandag"); 
INSERT INTO Dager VALUES(1, "Tirsdag"); 
INSERT INTO Dager VALUES(1, "Onsdag"); 
INSERT INTO Dager VALUES(1, "Torsdag"); 
INSERT INTO Dager VALUES(1, "Fredag"); 

INSERT INTO Vogn VALUES(1, 1, "SJ-sittevogn-1"); 
INSERT INTO Vogn VALUES(2, 1, "SJ-sittevogn-1"); 

-- Insert seter og senger til vognene
INSERT INTO Sete VALUES(1, 1, 1); 
INSERT INTO Sete VALUES(2, 1, 1); 
INSERT INTO Sete VALUES(3, 1, 1); 
INSERT INTO Sete VALUES(4, 1, 1); 
INSERT INTO Sete VALUES(5, 1, 1); 
INSERT INTO Sete VALUES(6, 1, 1); 
INSERT INTO Sete VALUES(7, 1, 1); 
INSERT INTO Sete VALUES(8, 1, 1); 
INSERT INTO Sete VALUES(9, 1, 1); 
INSERT INTO Sete VALUES(10, 1, 1); 
INSERT INTO Sete VALUES(11, 1, 1); 
INSERT INTO Sete VALUES(12, 1, 1); 

INSERT INTO Sete VALUES(1, 2, 1); 
INSERT INTO Sete VALUES(2, 2, 1); 
INSERT INTO Sete VALUES(3, 2, 1); 
INSERT INTO Sete VALUES(4, 2, 1); 
INSERT INTO Sete VALUES(5, 2, 1); 
INSERT INTO Sete VALUES(6, 2, 1); 
INSERT INTO Sete VALUES(7, 2, 1); 
INSERT INTO Sete VALUES(8, 2, 1); 
INSERT INTO Sete VALUES(9, 2, 1); 
INSERT INTO Sete VALUES(10, 2, 1); 
INSERT INTO Sete VALUES(11, 2, 1); 
INSERT INTO Sete VALUES(12, 2, 1); 

-- Insert nattog Trondheim-Bodoe
INSERT INTO KjoererDelstrekning VALUES(2, "Trondheim-Steinkjer", "23:05", "00:57"); 
INSERT INTO KjoererDelstrekning VALUES(2, "Steinkjer-Mosjoeen", "00:57", "04:41");
INSERT INTO KjoererDelstrekning VALUES(2, "Mosjoeen-Mo i Rana", "04:41", "05:55");  
INSERT INTO KjoererDelstrekning VALUES(2, "Mo i Rana-Fauske", "05:55", "08:19");  
INSERT INTO KjoererDelstrekning VALUES(2, "Fauske-Bodoe", "08:19", "09:05");  

INSERT INTO Dager VALUES(2, "Mandag"); 
INSERT INTO Dager VALUES(2, "Tirsdag"); 
INSERT INTO Dager VALUES(2, "Onsdag"); 
INSERT INTO Dager VALUES(2, "Torsdag"); 
INSERT INTO Dager VALUES(2, "Fredag"); 
INSERT INTO Dager VALUES(2, "Loerdag");
INSERT INTO Dager VALUES(2, "Soendag");

INSERT INTO Vogn VALUES(1, 2, "SJ-sittevogn-1"); 
INSERT INTO Vogn VALUES(2, 2, "SJ-sovevogn-1"); 

-- Insert seter og senger til vognene
INSERT INTO Sete VALUES(1, 1, 2); 
INSERT INTO Sete VALUES(2, 1, 2); 
INSERT INTO Sete VALUES(3, 1, 2); 
INSERT INTO Sete VALUES(4, 1, 2); 
INSERT INTO Sete VALUES(5, 1, 2); 
INSERT INTO Sete VALUES(6, 1, 2); 
INSERT INTO Sete VALUES(7, 1, 2); 
INSERT INTO Sete VALUES(8, 1, 2); 
INSERT INTO Sete VALUES(9, 1, 2); 
INSERT INTO Sete VALUES(10, 1, 2); 
INSERT INTO Sete VALUES(11, 1, 2); 
INSERT INTO Sete VALUES(12, 1, 2); 

INSERT INTO Seng VALUES(1, 2, 2, 1); 
INSERT INTO Seng VALUES(2, 2, 2, 1); 
INSERT INTO Seng VALUES(3, 2, 2, 2); 
INSERT INTO Seng VALUES(4, 2, 2, 2); 
INSERT INTO Seng VALUES(5, 2, 2, 3); 
INSERT INTO Seng VALUES(6, 2, 2, 3); 
INSERT INTO Seng VALUES(7, 2, 2, 4); 
INSERT INTO Seng VALUES(8, 2, 2, 4); 

-- Insert morgentog Mo i Rana-Trondheim
INSERT INTO KjoererDelstrekning VALUES(3, "Mo i Rana-Mosjoeen", "08:11", "09:14"); 
INSERT INTO KjoererDelstrekning VALUES(3, "Mosjoeen-Steinkjer", "09:14", "12:31");
INSERT INTO KjoererDelstrekning VALUES(3, "Steinkjer-Trondheim", "12:31", "14:31");  

INSERT INTO Dager VALUES(3, "Mandag");
INSERT INTO Dager VALUES(3, "Tirsdag");
INSERT INTO Dager VALUES(3, "Onsdag");
INSERT INTO Dager VALUES(3, "Torsdag");
INSERT INTO Dager VALUES(3, "Fredag");

INSERT INTO Vogn VALUES(1, 3, "SJ-sittevogn-1");

-- Insert seter og senger til vognene
INSERT INTO Sete VALUES(1, 1, 3); 
INSERT INTO Sete VALUES(2, 1, 3); 
INSERT INTO Sete VALUES(3, 1, 3); 
INSERT INTO Sete VALUES(4, 1, 3); 
INSERT INTO Sete VALUES(5, 1, 3); 
INSERT INTO Sete VALUES(6, 1, 3); 
INSERT INTO Sete VALUES(7, 1, 3); 
INSERT INTO Sete VALUES(8, 1, 3); 
INSERT INTO Sete VALUES(9, 1, 3); 
INSERT INTO Sete VALUES(10, 1, 3); 
INSERT INTO Sete VALUES(11, 1, 3); 
INSERT INTO Sete VALUES(12, 1, 3); 

COMMIT; 

