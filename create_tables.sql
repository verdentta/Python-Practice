-- Table to store fuel rates in Canadian dollars (cents)
CREATE TABLE fuel_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fuel_type VARCHAR(50),
    rate_in_cents INT,
    report_month DATE
);

-- Table to store converted fuel rates in Euros
CREATE TABLE converted_fuel_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fuel_type VARCHAR(50),
    rate_in_euros DECIMAL(10, 2),
    report_month DATE
);

-- Sample data for fuel rates in Canadian cents
INSERT INTO fuel_rates (fuel_type, rate_in_cents, report_month) VALUES
('Gasoline', 130, '2024-06-01'),
('Diesel', 120, '2024-06-01'),
('Gasoline', 135, '2024-07-01'),
('Diesel', 125, '2024-07-01'),
('Gasoline', 140, '2024-08-01'),
('Diesel', 130, '2024-08-01');