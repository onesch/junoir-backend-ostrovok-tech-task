SELECT m.name, m.department, t.mx
FROM (
    SELECT department, max(salary) AS mx
    FROM employee
    GROUP BY department
) t
JOIN employee m 
    ON m.department = t.department 
    AND t.mx = m.salary;


SELECT DISTINCT ON (department) department, name, salary
FROM employee
ORDER BY department, salary DESC;
