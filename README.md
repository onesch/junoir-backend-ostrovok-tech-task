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

### Task 2: Smashing Wallpaper Downloader.

There is a great website called Smashing Magazine that publishes excellent desktop wallpapers every month. Checking the website every month to see what is new is not the most productive task, so let's try to automate it.

The goal is to write a CLI utility that downloads all wallpapers in the required resolution for a specified month and year into the user's current directory.

All wallpapers can be found [here](https://www.smashingmagazine.com/category/wallpapers/), and wallpapers for May 2017 can be found [here](https://www.smashingmagazine.com/2017/04/desktop-wallpaper-calendars-may-2017/).


## Requirements:

* Python 3.5+
* Any third-party libraries are allowed
* Follow PEP8 style guidelines
* If you have time, you can cover the utility with tests using `py.test` (:

## Environment setup and running:

Prepare the environment and install dependencies (opens a console inside the container):

```bash
make getwallpapers_env
```

Run the wallpaper download script from the previously opened console:

```bash
./getwallpapers.py 022018 640x480
```

Run tests:

```bash
make getwallpapers_test
```

## Features:

* If wallpapers are available in both versions (with a calendar and without a calendar), the utility should download both versions.
* Not all wallpapers are available in all resolutions. If a specific wallpaper does not have the requested resolution, the utility should skip it.
