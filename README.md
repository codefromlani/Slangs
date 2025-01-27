Slangs (Abbreviation Website)

This project is a full-stack application where users can search, view and submit abbreviations with their meanings. The backend is built using FastAPI and connects to a database to store and manage abbreviations. The frontend allows users to interact with the system through search functionality, viewing approved abbreviations, and submitting new ones.

Technologies Used:

- Backend: FastAPI
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript
- Database ORM: SQLAlchemy
- Authentication (JWT): Admin-only access 

Features:

- Search Abbreviations: Users can search for abbreviations and view their meanings (only approved abbreviations are displayed).
- Submit New Abbreviations: Users can submit new abbreviations and their meanings.
- Approve/Reject Abbreviations: Admin users can approve or reject user-submitted abbreviations.

Endpoints:

- POST /abbreviations/:
 Submit a new abbreviation with its meaning. The abbreviation will be in a "pending" status until reviewed by an admin.

- GET /abbreviations/{abbr}:
 Retrieve an abbreviation by its name, but only if it has been approved

- GET /abbreviations/:
 Retrieve all abbreviations with pagination (e.g., limit=20, skip=0).

- PUT /abbreviations/{abbr_id}/approve/:
 Admins can approve or reject an abbreviation. It will change its status accordingly.

- DELETE /abbreviations/{abbr_id}/:
 Delete an abbreviation from the database.

 Setting Up the Project Locally:

1. Clone the repository:
git clone https://github.com/codefromlani/Slangs.git
2. Install dependencies:
pip install -r requirements.txt
3. Set up the database:
Ensure that your database (PostgreSQL) is configured and that the appropriate environment variables (if any) are set.
4. Run the FastAPI server:
uvicorn main:app --reload

Contributions:

If you’d like to contribute to the project, please fork the repository and submit a pull request with your changes.