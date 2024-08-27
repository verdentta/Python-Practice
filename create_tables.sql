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

CREATE TABLE monthly_km_by_fuel_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fuel_type VARCHAR(50),
    route VARCHAR(50),
    km_driven INT,
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


INSERT INTO converted_fuel_rates (fuel_type, rate_in_cents, report_month) VALUES
('Gasoline', 1.30, '2024-06-01'),
('Diesel', 1.20, '2024-06-01'),
('Gasoline', 1.35, '2024-07-01'),
('Diesel', 1.25, '2024-07-01'),
('Gasoline', 1.40, '2024-08-01'),
('Diesel', 1.30, '2024-08-01');

INSERT INTO monthly_km_by_fuel_type (fuel_type, route, km_driven, report_month) VALUES
('Gasoline', 'YHM1A', 4500, '2024-06-01'),
('Diesel', 'YHM2B', 3200, '2024-06-01'),
('Gasoline', 'YHM1A', 4600, '2024-07-01'),
('Diesel', 'YHM2B', 3300, '2024-07-01'),
('Gasoline', 'YHM1A', 4700, '2024-08-01'),
('Diesel', 'YHM2B', 3400, '2024-08-01'),
('Gasoline', 'YHM1A', 4800, '2024-09-01'),
('Diesel', 'YHM2B', 3500, '2024-09-01');