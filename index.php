<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fuel Rates</title>
</head>
<body>

    <h1>Fuel Rates Report - Latest Month</h1>
    <table border="1">
        <tr>
            <th>Fuel Type</th>
            <th>Rate (cents per liter)</th>
            <th>Month</th>
        </tr>
        <?php
        // Set up the database connection
        $servername = "localhost";
        $username = "root";
        $password = "user";
        $dbname = "dhl_python";

        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Query to fetch the latest month's fuel rates
        $sql = "SELECT fuel_type, rate_in_cents, report_month FROM fuel_rates ORDER BY report_month";
        $result = $conn->query($sql);

        // Check if there are any results
        if ($result->num_rows > 0) {
            // Output data of each row
            while($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $row['fuel_type'] . "</td>";
                echo "<td>" . $row['rate_in_cents'] . "</td>";
                echo "<td>" . $row['report_month'] . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='3'>No data found</td></tr>";
        }

        // Close the connection
        $conn->close();
        ?>
    </table>

</body>
</html>