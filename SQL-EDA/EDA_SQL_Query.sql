SELECT COUNT(*) FROM HousesTable;
SELECT COUNT(DISTINCT Neighborhood) FROM HousesTable;
SELECT COUNT(DISTINCT City) FROM HousesTable;

WITH stats AS (
    SELECT
        MIN(Price) AS MinPrice,
        MAX(Price) AS MaxPrice,
        AVG(Price) AS AveragePrice
    FROM HousesTable
)
SELECT
    stats.*,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY Price)
        OVER() AS MedianPrice
FROM HousesTable
CROSS JOIN stats;

/* Here I found that there is SQM < 40 and it's prices where very high so i deleted them all

SELECT DISTINCT [Area SQM], Price
FROM HousesTable
ORDER BY [Area SQM]

DELETE FROM HousesTable
WHERE [Area SQM] < 40;
*/

/* Getting Average Price For Every City And Neighborhood  */
SELECT
	Governorate,
	AVG(Price) AS AveragePrice,
	COUNT(*) AS Listings
FROM HousesTable
GROUP BY Governorate
ORDER BY AveragePrice
SELECT
	Neighborhood,
	AVG(Price) AS AveragePrice,
	COUNT(*) AS Listings
FROM HousesTable
GROUP BY Neighborhood
ORDER BY AveragePrice

SELECT
	Neighborhood,
	AVG(Price / NULLIF([Area SQM], 0)) AS AvgPricePerSQM
FROM HousesTable
Group BY Neighborhood
ORDER BY AvgPricePerSQM

SELECT 
    [Number Of Bedrooms],
    AVG(Price) AS AvgPrice,
    COUNT(*) AS Listings
FROM HousesTable
GROUP BY [Number Of Bedrooms]
ORDER BY [Number Of Bedrooms];
SELECT
	[Number Of Bathrooms],
	AVG(Price) AS AvgPrice,
	COUNT(*) AS Listings
FROM HousesTable
GROUP BY [Number Of Bathrooms]
ORDER BY [Number Of Bathrooms]

SELECT
	[Area SQM],
	AVG(Price) AS AvgPrice,
	COUNT(*) AS Listings
FROM HousesTable
GROUP BY [Area SQM]
ORDER BY AvgPrice


SELECT 
    City,
    AVG(Price) AS AvgPrice,
    COUNT(*) AS Listings
FROM HousesTable
GROUP BY City
ORDER BY AvgPrice DESC;

SELECT 
    Type,
    COUNT(*) AS TotalListings
FROM HousesTable
GROUP BY Type; 

SELECT 
    Type,
    AVG(Price) AS AvgPrice,
    AVG([Area SQM]) AS AvgArea
FROM HousesTable
WHERE [Area SQM] >= 40
GROUP BY Type
ORDER BY AvgPrice DESC;

SELECT DISTINCT(Governorate)
FROM HousesTable


SELECT TOP 10
	Type,
	AVG(Price) AS AvgPrice
FROM HousesTable
WHERE Governorate = 'Cairo'
GROUP BY Type
ORDER BY AvgPrice DESC
SELECT TOP 10
	Type,
	AVG(Price) AS AvgPrice
FROM HousesTable
WHERE Governorate = 'Giza'
GROUP BY Type
ORDER BY AvgPrice DESC