import asyncpg
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("employee")

NEON_DB_URL = "postgresql://neondb_owner:*******************@ep-wispy-sun-a1n6mwse-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

async def fetch_rows(query: str, *args):
    try:
        conn = await asyncpg.connect(NEON_DB_URL)
        rows = await conn.fetch(query, *args)
        await conn.close()
        return rows
    except Exception as e:
        print(f"Database error: {e}")
        return None

@mcp.tool()
async def get_all_employees() -> str:
    """Get all employees directly from Neon PostgreSQL."""
    query = "SELECT id, firstName, lastName, email, salary, age, location, hireDate FROM employee"
    rows = await fetch_rows(query)

    if not rows:
        return "No employees found or failed to fetch."

    employees = []
    for row in rows:
        employee_info = f"""
        ID: {row['id']}
        Name: {row['firstname']} {row['lastname']}
        Email: {row['email']}
        Salary: LKR {float(row['salary']):,.2f}
        Age: {row['age']}
        Location: {row['location']}
        Hire Date: {row['hiredate']}
        """
        employees.append(employee_info)

    return "\n---\n".join(employees)


@mcp.tool()
async def get_employee_by_id(employee_id: int) -> str:
    """Get a specific employee by ID directly from Neon."""
    query = "SELECT * FROM employee WHERE id = $1"
    rows = await fetch_rows(query, employee_id)

    if not rows:
        return f"No employee found with ID {employee_id}."

    row = rows[0]
    return f"""
    ID: {row['id']}
    Name: {row['firstname']} {row['lastname']}
    Email: {row['email']}
    Salary: LKR {float(row['salary']):,.2f}
    Age: {row['age']}
    Location: {row['location']}
    Hire Date: {row['hiredate']}
    """

if __name__ == "__main__":
    mcp.run(transport="stdio")