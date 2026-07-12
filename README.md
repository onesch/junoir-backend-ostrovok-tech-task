## **Test assignment for a Junior Backend Developer position**

Source: https://solvit.space/test-tasks/30

### Task 1: What could be simpler than SQL?

You are given a PostgreSQL table containing a list of employees, their salaries, and their departments. You need to write a query that selects the employee with the highest salary from each department. You can use a [table dump](https://drive.google.com/file/d/1RycBhOBLAyet54f3oL_WaV2OJ8wTba7L/view?pli=1) as test data; here is an example schema:

```sql
postgres=# \d employee
            Table "public.employee"
   Column   |         Type          | Modifiers
------------+-----------------------+-----------
 id         | integer               | not null
 name       | character varying(30) |
 department | character varying(30) |
 salary     | integer               |
Indexes:
    "employee_pkey" PRIMARY KEY, btree (id)
```

If we need information about all employees earning the maximum salary in the department (in cases where the salary is the same):

```sql
SELECT m.name, m.department, t.mx
FROM (
    SELECT department, max(salary) AS mx
    FROM employee
    GROUP BY department
) t
JOIN employee m on m.department = t.department and t.mx = m.salary;
```

If there is sufficient information about any of the employees with the highest salary:

```sql
SELECT DISTINCT ON (department) department, name, salary
FROM employee
ORDER BY department, salary DESC;
```

Run queries, view the result:

```bash
make sql
```
