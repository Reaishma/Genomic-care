-- Create the Users table
CREATE TABLE Users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Create the Projects table
CREATE TABLE Projects (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  project_name VARCHAR(100) NOT NULL,
  description TEXT,
  FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Create the Datasets table
CREATE TABLE Datasets (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_id INT NOT NULL,
  dataset_name VARCHAR(100) NOT NULL,
  file_type VARCHAR(50) NOT NULL,
  file_data BLOB,
  FOREIGN KEY (project_id) REFERENCES Projects(id)
);

-- Create the Analyses table
CREATE TABLE Analyses (
  id INT PRIMARY KEY AUTO_INCREMENT,
  project_id INT NOT NULL,
  analysis_type VARCHAR(50) NOT NULL,
  parameters TEXT,
  results TEXT,
  FOREIGN KEY (project_id) REFERENCES Projects(id)
);

-- Create the Results table
CREATE TABLE Results (
  id INT PRIMARY KEY AUTO_INCREMENT,
  analysis_id INT NOT NULL,
  result_type VARCHAR(50) NOT NULL,
  result_data TEXT,
  FOREIGN KEY (analysis_id) REFERENCES Analyses(id)
);
-- Insert sample data into the Users table
INSERT INTO Users (username, email, password) 
VALUES ('john_doe', 'john.doe@example.com', 'password123'),
       ('jane_doe', 'jane.doe@example.com', 'password456');

-- Insert sample data into the Projects table
INSERT INTO Projects (user_id, project_name, description) 
VALUES (1, 'Genetic Analysis Project', 'This project involves analyzing genetic data'),
       (2, 'Phylogenetic Analysis Project', 'This project involves constructing phylogenetic trees');

-- Insert sample data into the Datasets table
INSERT INTO Datasets (project_id, dataset_name, file_type, file_data) 
VALUES (1, 'Genetic Data', 'FASTA', 'sample_data'),
       (2, 'Phylogenetic Data', 'GenBank', 'sample_data');

-- Insert sample data into the Analyses table
INSERT INTO Analyses (project_id, analysis_type, parameters, results) 
VALUES (1, 'Sequence Alignment', ' MUSCLE algorithm', 'aligned_sequences'),
       (2, 'Phylogenetic Analysis', 'Maximum Likelihood method', 'phylogenetic_tree');

-- Insert sample data into the Results table
INSERT INTO Results (analysis_id, result_type, result_data) 
VALUES (1, 'Aligned Sequences', 'aligned_sequences_data'),
       (2, 'Phylogenetic Tree', 'phylogenetic_tree_data');
SELECT * FROM Projects WHERE user_id = 1;
SELECT * FROM Analyses WHERE project_id = 1;
-- Display all data from the Users table
SELECT * FROM Users;

-- Display all data from the Projects table
SELECT * FROM Projects;

-- Display all data from the Datasets table
SELECT * FROM Datasets;

-- Display all data from the Analyses table
SELECT * FROM Analyses;

-- Display all data from the Results table
SELECT * FROM Results;
